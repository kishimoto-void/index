"""
Index Hybrid — Connect Core (experimental skeleton)
=================================================

Purpose
-------
A small, standard-library-only connection layer for experimental modules:
- WASHAWASHA Chase / observable-state diffs
- thought-branch tracking
- identity / continuity checks
- provenance and revision history
- future Learning / Exploration / Evaluation adapters

Design stance
-------------
This is an experimental scaffold, not a finished framework.
The core stores and connects observations; it does not decide whether a claim
is true, infer hidden model state, or require one specific analysis method.

Python: 3.10+
License: choose / add a project license before distribution.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Optional, Protocol, Sequence
from uuid import uuid4


CORE_VERSION = "0.1.0"


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def canonical_json(value: Any) -> str:
    """Stable JSON representation for hashing and comparisons."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def content_hash(value: Any) -> str:
    """Hash a JSON-compatible value. This is a comparison aid, not proof of truth."""
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


class RecordKind(str, Enum):
    ISSUE = "issue"
    HYPOTHESIS = "hypothesis"
    OBSERVATION = "observation"
    EXPERIMENT = "experiment"
    BRANCH = "branch"
    REFERENCE = "reference"
    NOTE = "note"
    UNKNOWN = "unknown"


class EpistemicStatus(str, Enum):
    UNKNOWN = "unknown"
    UNVERIFIED = "unverified"
    HYPOTHESIS = "hypothesis"
    OBSERVED = "observed"
    SUPPORTED = "supported"
    CONFIRMED = "confirmed"
    CONTRADICTED = "contradicted"
    REJECTED = "rejected"


@dataclass
class Provenance:
    """Where a record came from; fields may be left unknown."""
    source: str = "unspecified"
    actor: str = "unspecified"
    method: str = "manual"
    source_record_id: Optional[str] = None
    notes: str = ""


@dataclass
class IndexRecord:
    """
    Portable record passed between modules.

    `payload` is intentionally open-ended. The core validates only the
    common envelope and does not impose a universal analysis schema.
    """
    kind: str
    title: str
    payload: dict[str, Any] = field(default_factory=dict)
    record_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = EpistemicStatus.UNKNOWN.value
    relations: list[dict[str, str]] = field(default_factory=list)
    provenance: Provenance = field(default_factory=Provenance)
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    revision: int = 1
    extensions: dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> dict[str, Any]:
        """Return a detached JSON-compatible snapshot."""
        return json.loads(canonical_json(asdict(self)))

    def fingerprint(self, include_mutable_metadata: bool = False) -> str:
        """
        Compare semantic content.

        By default timestamps/revision are excluded so metadata-only updates
        do not masquerade as content changes.
        """
        data = self.snapshot()
        if not include_mutable_metadata:
            for key in ("updated_at", "revision"):
                data.pop(key, None)
        return content_hash(data)


@dataclass
class RevisionEvent:
    event_id: str
    record_id: str
    revision: int
    event_type: str
    timestamp: str
    before_hash: Optional[str]
    after_hash: str
    changed_fields: list[str]
    actor: str = "connect_core"
    note: str = ""


@dataclass
class IdentityResult:
    same_identity: Optional[bool]
    confidence: str
    reasons: list[str]
    left_id: Optional[str] = None
    right_id: Optional[str] = None


@dataclass
class DiffItem:
    path: str
    change: str
    before: Any = None
    after: Any = None


@dataclass
class StateSnapshot:
    """A visible state captured for external change tracking."""
    snapshot_id: str
    subject_id: str
    label: str
    state: dict[str, Any]
    state_hash: str
    timestamp: str = field(default_factory=utc_now)
    source: str = "manual"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChaseResult:
    subject_id: str
    before_snapshot_id: Optional[str]
    after_snapshot_id: str
    changed: bool
    diff: list[DiffItem]
    summary: dict[str, Any] = field(default_factory=dict)


@dataclass
class Branch:
    branch_id: str = field(default_factory=lambda: str(uuid4()))
    parent_branch_id: Optional[str] = None
    forked_from_record_id: Optional[str] = None
    label: str = "branch"
    purpose: str = ""
    status: str = "open"
    record_ids: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)


class ConnectModule(Protocol):
    """Minimal contract for pluggable modules."""

    name: str

    def process(self, records: Sequence[IndexRecord], context: Mapping[str, Any]) -> Any:
        """Return a proposal/result; mutation of core records is not implicit."""
        ...


def _diff_values(before: Any, after: Any, prefix: str = "") -> list[DiffItem]:
    """Recursively diff JSON-like values, preserving paths and unknown fields."""
    if isinstance(before, Mapping) and isinstance(after, Mapping):
        result: list[DiffItem] = []
        keys = sorted(set(before.keys()) | set(after.keys()), key=str)
        for key in keys:
            path = f"{prefix}.{key}" if prefix else str(key)
            if key not in before:
                result.append(DiffItem(path=path, change="added", after=after[key]))
            elif key not in after:
                result.append(DiffItem(path=path, change="removed", before=before[key]))
            else:
                result.extend(_diff_values(before[key], after[key], path))
        return result
    if isinstance(before, list) and isinstance(after, list):
        if before == after:
            return []
        # Lists are compared as values in v0.1; element-level identity is ambiguous.
        return [DiffItem(path=prefix or "$", change="changed", before=before, after=after)]
    if before != after:
        return [DiffItem(path=prefix or "$", change="changed", before=before, after=after)]
    return []


class ConnectCore:
    """
    Minimal connection and observation core.

    Current scope:
      - record registration and explicit updates
      - revision events
      - observable-state snapshots and WASHAWASHA-style chase
      - conservative identity checks
      - explicit branch graph
      - module registration / proposal execution
      - JSON export

    Intentionally not included yet:
      - persistent database
      - semantic search / embeddings
      - automatic truth verification
      - implicit merging of similar records
      - hidden chain-of-thought access
    """

    def __init__(self, project_id: str = "default") -> None:
        self.project_id = project_id
        self.records: dict[str, IndexRecord] = {}
        self.revisions: list[RevisionEvent] = []
        self.snapshots: dict[str, list[StateSnapshot]] = {}
        self.branches: dict[str, Branch] = {}
        self.modules: dict[str, ConnectModule] = {}

    # ---------- Records / revision ----------

    def add_record(self, record: IndexRecord, *, actor: str = "user", note: str = "") -> IndexRecord:
        if record.record_id in self.records:
            raise ValueError(f"record_id already exists: {record.record_id}")
        record.created_at = record.created_at or utc_now()
        record.updated_at = utc_now()
        record.revision = max(1, record.revision)
        self.records[record.record_id] = record
        self.revisions.append(
            RevisionEvent(
                event_id=str(uuid4()),
                record_id=record.record_id,
                revision=record.revision,
                event_type="created",
                timestamp=utc_now(),
                before_hash=None,
                after_hash=record.fingerprint(),
                changed_fields=["*"],
                actor=actor,
                note=note,
            )
        )
        return record

    def get_record(self, record_id: str) -> IndexRecord:
        try:
            return self.records[record_id]
        except KeyError as exc:
            raise KeyError(f"unknown record_id: {record_id}") from exc

    def update_record(
        self,
        record_id: str,
        changes: Mapping[str, Any],
        *,
        actor: str = "user",
        note: str = "",
    ) -> IndexRecord:
        """
        Apply an explicit patch and append a revision event.
        Unknown keys are rejected at the envelope level; put custom data in payload/extensions.
        """
        record = self.get_record(record_id)
        allowed = {
            "kind", "title", "payload", "status", "relations",
            "provenance", "tags", "extensions",
        }
        invalid = sorted(set(changes.keys()) - allowed)
        if invalid:
            raise ValueError(
                f"unsupported top-level fields: {invalid}; "
                "use payload/extensions for custom fields"
            )

        before = record.snapshot()
        before_hash = record.fingerprint()
        for key, value in changes.items():
            if key == "provenance" and isinstance(value, Mapping):
                value = Provenance(**value)
            setattr(record, key, value)

        record.updated_at = utc_now()
        record.revision += 1
        after = record.snapshot()
        changed_fields = [
            key for key in changes
            if before.get(key) != after.get(key)
        ]
        if before.get("updated_at") != after.get("updated_at"):
            changed_fields.append("updated_at")
        self.revisions.append(
            RevisionEvent(
                event_id=str(uuid4()),
                record_id=record_id,
                revision=record.revision,
                event_type="updated",
                timestamp=utc_now(),
                before_hash=before_hash,
                after_hash=record.fingerprint(),
                changed_fields=sorted(set(changed_fields)),
                actor=actor,
                note=note,
            )
        )
        return record

    # ---------- Identity ----------

    def check_identity(
        self,
        left: IndexRecord | str,
        right: IndexRecord | str,
        *,
        explicit_same_identity: Optional[bool] = None,
    ) -> IdentityResult:
        """
        Conservative identity check, not semantic equivalence detection.

        Exact same ID => same identity.
        Different IDs => not automatically the same entity, even if content matches.
        Similar content is reported as a clue, never as an automatic merge.
        """
        a = self.get_record(left) if isinstance(left, str) else left
        b = self.get_record(right) if isinstance(right, str) else right

        if a.record_id == b.record_id:
            return IdentityResult(True, "high", ["identical record_id"], a.record_id, b.record_id)
        if explicit_same_identity is True:
            return IdentityResult(True, "explicit", ["caller explicitly linked identity"], a.record_id, b.record_id)
        if explicit_same_identity is False:
            return IdentityResult(False, "explicit", ["caller explicitly distinguished identities"], a.record_id, b.record_id)

        same_fingerprint = a.fingerprint() == b.fingerprint()
        reasons = ["different record_id"]
        if same_fingerprint:
            reasons.append("same fingerprint; may be duplicate content, not proof of same identity")
            return IdentityResult(None, "low", reasons, a.record_id, b.record_id)
        return IdentityResult(False, "low", reasons + ["content differs; semantic identity remains unresolved"], a.record_id, b.record_id)

    # ---------- Observable-state snapshots / Chase ----------

    def observe(
        self,
        subject_id: str,
        state: Mapping[str, Any],
        *,
        label: str = "observation",
        source: str = "manual",
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> StateSnapshot:
        """Store an externally visible state; does not inspect hidden internal state."""
        state_copy = json.loads(canonical_json(dict(state)))
        snap = StateSnapshot(
            snapshot_id=str(uuid4()),
            subject_id=subject_id,
            label=label,
            state=state_copy,
            state_hash=content_hash(state_copy),
            source=source,
            metadata=dict(metadata or {}),
        )
        self.snapshots.setdefault(subject_id, []).append(snap)
        return snap

    def diff_snapshots(
        self,
        before: StateSnapshot | str,
        after: StateSnapshot | str,
    ) -> list[DiffItem]:
        a = self._get_snapshot(before)
        b = self._get_snapshot(after)
        return _diff_values(a.state, b.state)

    def chase(
        self,
        subject_id: str,
        *,
        before_snapshot_id: Optional[str] = None,
        after_snapshot_id: Optional[str] = None,
    ) -> ChaseResult:
        """
        Compare two visible snapshots for a subject.
        If IDs are omitted, compare the latest two snapshots.
        """
        history = self.snapshots.get(subject_id, [])
        if after_snapshot_id is not None:
            after = self._get_snapshot(after_snapshot_id)
        elif history:
            after = history[-1]
        else:
            raise ValueError(f"no snapshots for subject_id: {subject_id}")

        if before_snapshot_id is not None:
            before = self._get_snapshot(before_snapshot_id)
        else:
            candidates = [s for s in history if s.snapshot_id != after.snapshot_id]
            before = candidates[-1] if candidates else None

        if before is None:
            return ChaseResult(
                subject_id=subject_id,
                before_snapshot_id=None,
                after_snapshot_id=after.snapshot_id,
                changed=True,
                diff=[DiffItem(path="$", change="initial_observation", after=after.state)],
                summary={"added_paths": 1, "removed_paths": 0, "changed_paths": 0, "initial": True},
            )

        diff = _diff_values(before.state, after.state)
        summary = {
            "added_paths": sum(item.change == "added" for item in diff),
            "removed_paths": sum(item.change == "removed" for item in diff),
            "changed_paths": sum(item.change == "changed" for item in diff),
            "initial": False,
        }
        return ChaseResult(
            subject_id=subject_id,
            before_snapshot_id=before.snapshot_id,
            after_snapshot_id=after.snapshot_id,
            changed=bool(diff),
            diff=diff,
            summary=summary,
        )

    def _get_snapshot(self, snapshot: StateSnapshot | str) -> StateSnapshot:
        if isinstance(snapshot, StateSnapshot):
            return snapshot
        for history in self.snapshots.values():
            for candidate in history:
                if candidate.snapshot_id == snapshot:
                    return candidate
        raise KeyError(f"unknown snapshot_id: {snapshot}")

    # ---------- Thought branches ----------

    def create_branch(
        self,
        label: str,
        *,
        parent_branch_id: Optional[str] = None,
        forked_from_record_id: Optional[str] = None,
        purpose: str = "",
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> Branch:
        if parent_branch_id is not None and parent_branch_id not in self.branches:
            raise KeyError(f"unknown parent_branch_id: {parent_branch_id}")
        if forked_from_record_id is not None and forked_from_record_id not in self.records:
            raise KeyError(f"unknown forked_from_record_id: {forked_from_record_id}")
        branch = Branch(
            parent_branch_id=parent_branch_id,
            forked_from_record_id=forked_from_record_id,
            label=label,
            purpose=purpose,
            metadata=dict(metadata or {}),
        )
        self.branches[branch.branch_id] = branch
        return branch

    def attach_record_to_branch(self, branch_id: str, record_id: str) -> None:
        if branch_id not in self.branches:
            raise KeyError(f"unknown branch_id: {branch_id}")
        if record_id not in self.records:
            raise KeyError(f"unknown record_id: {record_id}")
        branch = self.branches[branch_id]
        if record_id not in branch.record_ids:
            branch.record_ids.append(record_id)

    def compare_branches(self, left_branch_id: str, right_branch_id: str) -> dict[str, Any]:
        """Compare explicit membership; does not judge which branch is better."""
        left = self.branches[left_branch_id]
        right = self.branches[right_branch_id]
        left_ids, right_ids = set(left.record_ids), set(right.record_ids)
        return {
            "left_branch_id": left_branch_id,
            "right_branch_id": right_branch_id,
            "shared_record_ids": sorted(left_ids & right_ids),
            "left_only_record_ids": sorted(left_ids - right_ids),
            "right_only_record_ids": sorted(right_ids - left_ids),
            "same_parent": left.parent_branch_id == right.parent_branch_id,
            "same_fork_point": left.forked_from_record_id == right.forked_from_record_id,
        }

    # ---------- Pluggable modules ----------

    def register_module(self, module: ConnectModule) -> None:
        if not getattr(module, "name", None):
            raise ValueError("module must expose a non-empty `name`")
        if module.name in self.modules:
            raise ValueError(f"module already registered: {module.name}")
        if not callable(getattr(module, "process", None)):
            raise TypeError("module must implement process(records, context)")
        self.modules[module.name] = module

    def run_module(
        self,
        module_name: str,
        record_ids: Iterable[str],
        *,
        context: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        """
        Run a module on selected records.
        The module returns a proposal/result; it does not automatically mutate Core.
        """
        module = self.modules[module_name]
        records = [self.get_record(record_id) for record_id in record_ids]
        return module.process(records, dict(context or {}))

    # ---------- Export ----------

    def export_dict(self) -> dict[str, Any]:
        return {
            "core_version": CORE_VERSION,
            "project_id": self.project_id,
            "records": [record.snapshot() for record in self.records.values()],
            "revisions": [asdict(event) for event in self.revisions],
            "snapshots": {
                subject_id: [asdict(snapshot) for snapshot in history]
                for subject_id, history in self.snapshots.items()
            },
            "branches": [asdict(branch) for branch in self.branches.values()],
        }

    def export_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.export_dict(), ensure_ascii=False, indent=indent)


# ---------- Tiny smoke test / example ----------

if __name__ == "__main__":
    core = ConnectCore(project_id="instant-index-experiment")

    issue = core.add_record(
        IndexRecord(
            kind=RecordKind.ISSUE.value,
            title="Does the answer drift between runs?",
            status=EpistemicStatus.UNVERIFIED.value,
            payload={"question": "Track externally visible changes across runs."},
            provenance=Provenance(source="manual test", actor="user", method="smoke_test"),
        ),
        actor="user",
        note="initial experiment record",
    )

    # Observable snapshots can record labels, answer summaries, branch counts,
    # assumptions, or any other public/visible features chosen by the experiment.
    core.observe(
        subject_id="probe-01",
        label="run-1",
        source="manual",
        state={"answer_summary": "A", "assumptions": ["x"], "branches": 1},
    )
    core.observe(
        subject_id="probe-01",
        label="run-2",
        source="manual",
        state={"answer_summary": "B", "assumptions": ["x", "y"], "branches": 2},
    )
    chase_result = core.chase("probe-01")

    left = core.create_branch("hypothesis-A", forked_from_record_id=issue.record_id)
    right = core.create_branch("hypothesis-B", forked_from_record_id=issue.record_id)
    core.attach_record_to_branch(left.branch_id, issue.record_id)

    print("Chase changed:", chase_result.changed)
    print("Chase summary:", chase_result.summary)
    print("Branch comparison:", core.compare_branches(left.branch_id, right.branch_id))
    print("Identity self-check:", core.check_identity(issue, issue))
    # Uncomment to inspect the portable serialized structure:
    # print(core.export_json())
