"""Sequential external answer-flow protocol for Index Hybrid experiments."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Mapping, Optional, Protocol, Sequence
from uuid import uuid4
from datetime import datetime, timezone
from hashlib import sha256
import json

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

def canonical_json(x: Any) -> str:
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)

def stable_hash(x: Any) -> str:
    return sha256(canonical_json(x).encode("utf-8")).hexdigest()

class AnswerMode(str, Enum):
    GENERAL_ANSWER = "general_answer"
    BOUNDARY_EXPLORATION = "boundary_exploration"
    BOTH = "both"
    UNDECIDED = "undecided"

class Stage(str, Enum):
    INPUT = "INPUT"
    SCOPE = "SCOPE"
    DECOMPOSE = "DECOMPOSE"
    BRANCH = "BRANCH"
    CHECK = "CHECK"
    ANSWER = "ANSWER"

DEFAULT_STAGE_ORDER = (
    Stage.INPUT, Stage.SCOPE, Stage.DECOMPOSE,
    Stage.BRANCH, Stage.CHECK, Stage.ANSWER,
)

@dataclass
class StageArtifact:
    run_id: str
    stage: str
    sequence: int
    content: dict[str, Any]
    content_hash: str
    created_at: str = field(default_factory=utc_now)
    previous_artifact_hash: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FlowRun:
    run_id: str
    task: str
    mode: str
    stage_order: list[str]
    artifacts: list[StageArtifact] = field(default_factory=list)
    status: str = "created"
    created_at: str = field(default_factory=utc_now)
    completed_at: Optional[str] = None
    errors: list[str] = field(default_factory=list)
    def export_dict(self) -> dict[str, Any]:
        return asdict(self)

class StageGenerator(Protocol):
    def generate_stage(self, *, stage: str, task: str, answer_mode: str,
                       prior_artifacts: Sequence[StageArtifact],
                       requirements: Mapping[str, Any]) -> Mapping[str, Any]: ...

class FlowValidationError(ValueError): pass

_REQUIRED = {
    Stage.INPUT: (["problem_statement", "constraints", "unknowns"],
                  "Restate the task and preserve ambiguity; do not solve it yet."),
    Stage.SCOPE: (["answer_mode", "goal", "scope", "stop_condition"],
                  "Declare answer policy and scope."),
    Stage.DECOMPOSE: (["subquestions", "assumptions", "knowns", "unknowns"],
                      "Decompose into externally checkable elements."),
    Stage.BRANCH: (["branches", "branching_rationale"],
                   "List useful paths; empty is valid when no meaningful branch is needed."),
    Stage.CHECK: (["checks", "unresolved_items", "boundary_status"],
                  "Check consistency; report only boundary tests actually performed."),
    Stage.ANSWER: (["answer", "answer_mode", "scope_statement", "limitations"],
                   "Compose from committed prior artifacts; do not invent unperformed checks."),
}

def stage_requirements(stage: Stage, mode: AnswerMode) -> dict[str, Any]:
    required, instruction = _REQUIRED[stage]
    result = {
        "required_fields": list(required),
        "instruction": instruction,
        "answer_mode": mode.value,
        "return_json_object": True,
        "use_prior_committed_artifacts": True,
        "do_not_claim_hidden_reasoning_access": True,
    }
    if stage == Stage.BRANCH:
        result["branching_policy"] = {
            AnswerMode.GENERAL_ANSWER: "Consider useful alternatives; do not force exhaustive edge exploration.",
            AnswerMode.BOUNDARY_EXPLORATION: "Prioritize edge cases, counterexamples, and limits.",
            AnswerMode.BOTH: "Include useful ordinary paths and boundary/counterexample paths.",
            AnswerMode.UNDECIDED: "Do not silently choose a mode; record ambiguity or clarification behavior.",
        }[mode]
    if stage == Stage.CHECK:
        result["check_policy"] = {
            AnswerMode.GENERAL_ANSWER: "Check adequacy within ordinary scope.",
            AnswerMode.BOUNDARY_EXPLORATION: "Check tested limits and state whether exploration is non-exhaustive.",
            AnswerMode.BOTH: "Check ordinary answer and boundary exploration separately.",
            AnswerMode.UNDECIDED: "Flag unresolved policy; not a clean comparison condition.",
        }[mode]
    return result

class SequentialAnswerRunner:
    """Commit each visible stage artifact before invoking the next stage.

    This audits external dependencies, not hidden token-level reasoning.
    """
    def __init__(self, generator: StageGenerator, stage_order: Sequence[Stage] = DEFAULT_STAGE_ORDER):
        order = tuple(stage_order)
        if not order or order[0] != Stage.INPUT or order[-1] != Stage.ANSWER:
            raise ValueError("stage order must begin with INPUT and end with ANSWER")
        if len(set(order)) != len(order):
            raise ValueError("stage order cannot contain duplicate stages")
        dependencies = [(Stage.INPUT, Stage.SCOPE), (Stage.SCOPE, Stage.DECOMPOSE),
                        (Stage.DECOMPOSE, Stage.BRANCH), (Stage.BRANCH, Stage.CHECK),
                        (Stage.CHECK, Stage.ANSWER)]
        if any(order.index(a) >= order.index(b) for a, b in dependencies):
            raise ValueError("stage order violates sequential dependencies")
        self.generator, self.stage_order = generator, order

    def run(self, task: str, mode: AnswerMode | str) -> FlowRun:
        mode = mode if isinstance(mode, AnswerMode) else AnswerMode(str(mode))
        run = FlowRun(str(uuid4()), task, mode.value, [s.value for s in self.stage_order], status="running")
        previous_hash = None
        try:
            for seq, stage in enumerate(self.stage_order, 1):
                req = stage_requirements(stage, mode)
                # Only committed artifacts from earlier stages are passed forward.
                generated = self.generator.generate_stage(
                    stage=stage.value, task=task, answer_mode=mode.value,
                    prior_artifacts=tuple(run.artifacts), requirements=req)
                if not isinstance(generated, Mapping):
                    raise FlowValidationError(f"{stage.value}: generator must return a mapping")
                content = dict(generated)
                missing = [k for k in req["required_fields"] if k not in content]
                if stage == Stage.ANSWER and content.get("answer_mode") != mode.value:
                    missing.append("answer_mode must match selected mode")
                if missing:
                    raise FlowValidationError(f"{stage.value}: missing/invalid fields: {missing}")
                digest = stable_hash(content)
                run.artifacts.append(StageArtifact(
                    run_id=run.run_id, stage=stage.value, sequence=seq,
                    content=content, content_hash=digest,
                    previous_artifact_hash=previous_hash,
                    metadata={"requirements_hash": stable_hash(req),
                              "committed_before_next_stage": True}))
                previous_hash = digest
            run.status = "completed"
        except Exception as exc:
            run.status = "failed"
            run.errors.append(f"{type(exc).__name__}: {exc}")
            # Preserve partial artifacts for analysis; never erase failed runs.
        run.completed_at = utc_now()
        return run

    @staticmethod
    def validate_run(run: FlowRun) -> dict[str, Any]:
        observed = [a.stage for a in run.artifacts]
        return {
            "run_id": run.run_id, "status": run.status,
            "expected_stage_order": run.stage_order, "observed_stage_order": observed,
            "ordered_prefix_valid": observed == run.stage_order[:len(observed)],
            "hash_links_valid": all(
                a.previous_artifact_hash == (run.artifacts[i-1].content_hash if i else None)
                for i, a in enumerate(run.artifacts)),
            "completed_all_stages": observed == run.stage_order and run.status == "completed",
            "errors": list(run.errors),
        }
