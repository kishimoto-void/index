# Index Hybrid — Specification

- **Specification version:** 1.0.0
- **Status:** Draft
- **Scope:** Shared data contract, record semantics, module boundaries, and conformance expectations

The terms **MUST**, **MUST NOT**, **SHOULD**, and **MAY** express normative requirements.

## 1. Purpose

Index Hybrid is a portable context-indexing framework for preserving project state, observations, hypotheses, experiments, and proposed next actions across sessions and tools.

The architecture separates:

1. **Core Contract** — stable shared semantics and integrity rules.
2. **Replaceable Modules** — learning, exploration, and evaluation strategies.
3. **Adapters** — storage, retrieval, LLM, and local-harness integrations.

The Core Contract is stable during ordinary operation. It MAY change through an explicitly versioned specification update with documented migration and compatibility behavior. Modules MUST NOT silently redefine core semantics.

## 2. Design principles

Conforming implementations MUST preserve these principles:

- **Identity:** each record has a stable, unique identifier within its index namespace.
- **Provenance:** source information MUST NOT be silently fabricated or erased.
- **Uncertainty:** unknown, untested, and inconclusive information MUST remain representable.
- **Revision:** accepted changes MUST be traceable to a prior revision or explicit creation event.
- **Controlled mutation:** module outputs are proposals until validated and accepted by the core or an authorized user.
- **Isolation:** extension fields MUST NOT silently change core meanings.
- **Portability:** the model MUST be representable in machine-readable form and SHOULD have a human-readable representation.
- **Project separation:** records from different projects MUST be distinguishable and linkable without requiring them to be merged.

## 3. Architecture

### 3.1 Core Contract

The core defines record identity, required metadata, type and status semantics, provenance, relationships, evidence references, revision rules, extension boundaries, and validation behavior.

### 3.2 Replaceable modules

Standard module categories:

- **Learning Module:** proposes record revisions from observations, evidence, and differences between expectations and outcomes.
- **Exploration Module:** proposes alternative hypotheses, branches, questions, and cross-domain analogies.
- **Evaluation Module:** assesses records or proposals against explicit criteria and reports results and limitations.

An implementation MAY add modules. Each module MUST declare its identifier, version, supported schema versions, input requirements, output contract, capabilities, and failure behavior.

### 3.3 Adapters

Adapters connect the shared model to storage, retrieval, LLMs, user interfaces, or external systems. An adapter MUST preserve core-field semantics. If it cannot represent a field, it MUST report the limitation rather than silently discard meaning.

### 3.4 Standard processing flow

```text
LOAD → INSPECT → PROPOSE → VALIDATE → ACCEPT / REJECT / DEFER → COMMIT
```

- **LOAD:** retrieve records needed for the task.
- **INSPECT:** identify objective, state, evidence, uncertainty, and constraints.
- **PROPOSE:** create an explicit proposal or diff.
- **VALIDATE:** check schema, invariants, references, and applicable evaluation rules.
- **ACCEPT / REJECT / DEFER:** record a decision or leave it pending.
- **COMMIT:** persist accepted changes and revision metadata.

A proposal MUST NOT be represented as committed before commit succeeds. If write access is unavailable, an implementation SHOULD emit a patch and state that it was not committed.

## 4. Standard three-layer view

The three-layer model is a standard logical view, not a mandatory storage hierarchy.

### L1 — Issue / Objective

Represents what is being addressed: issue, question, objective, scope, constraints, success criteria, and target outcome.

### L2 — Current State / Analysis

Represents current understanding: observations, sourced claims, hypotheses, contradictions, unknowns, missing evidence, and proposed next questions.

### L3 — Experience / Experiments

Represents what was attempted and observed: setup, conditions, inputs, outputs, failures, deviations from expectations, and reproducibility information.

A record MAY be related to multiple issues or layers. Implementations SHOULD reference one canonical record by ID rather than duplicate it and allow copies to drift.

## 5. Record model

A standard record is a JSON-compatible object with these core fields:

| Field | Requirement | Meaning |
|---|---|---|
| `schema_version` | MUST | Version of the record schema |
| `index_id` | MUST | Stable, unique record identifier |
| `kind` | MUST | Semantic record type |
| `title` | MUST | Short human-readable label |
| `content` | MUST | Human-readable record body |
| `status` | MUST | Workflow state |
| `relations` | MUST | Array of typed links; may be empty |
| `evidence` | MUST | Array of evidence references; may be empty |
| `provenance` | MUST | Source metadata |
| `created_at` | MUST | Creation timestamp |
| `updated_at` | MUST | Last accepted update timestamp |
| `revision` | MUST | Positive integer revision number |
| `extensions` | MUST | Object for optional namespaced fields |

### 5.1 Field semantics

- `schema_version` MUST identify the schema used to interpret the record.
- `index_id` MUST NOT be reused for a different logical record.
- `kind` MUST be a non-empty string. Standard kinds are listed in §6.1. Unknown kinds MUST remain readable and MUST NOT be silently reinterpreted.
- `title` and `content` MUST be strings.
- `status` MUST use a recognized core status or an explicitly namespaced extension status.
- `relations` MUST be an array of typed references. Each reference MUST identify a target and relation type.
- `evidence` MUST be an array. Each evidence item SHOULD identify a source, observation, or record supporting a statement.
- `provenance` MUST identify the source category. Unknown details MUST be represented as unknown or null, not invented.
- `created_at` and `updated_at` MUST use RFC 3339 timestamps with a timezone offset. UTC timestamps ending in `Z` are RECOMMENDED.
- `revision` MUST be an integer greater than or equal to 1. Each accepted update MUST increment it.
- `extensions` MUST be an object. Extension keys SHOULD be namespaced to avoid collisions.

### 5.2 Example record

Timestamp values are illustrative, not claims about an actual record's creation time.

```json
{
  "schema_version": "1.0.0",
  "index_id": "idx_example_001",
  "kind": "hypothesis",
  "title": "Does changing condition X affect outcome Y?",
  "content": "A testable statement with a defined scope.",
  "status": "proposed",
  "relations": [],
  "evidence": [],
  "provenance": {
    "source_type": "user",
    "source_id": null
  },
  "created_at": "2026-10-12T00:00:00Z",
  "updated_at": "2026-10-12T00:00:00Z",
  "revision": 1,
  "extensions": {}
}
```

## 6. Types, statuses, and epistemic distinctions

### 6.1 Standard kinds

Recommended standard kinds:

`issue`, `objective`, `observation`, `claim`, `hypothesis`, `experiment`, `result`, `conclusion`, `analogy`, `question`, `action`, `decision`, `note`.

Implementations MAY define additional kinds without changing existing meanings.

### 6.2 Workflow status

Core statuses:

- `draft` — incomplete working record.
- `proposed` — proposed for consideration; not yet accepted as an active task or change.
- `active` — currently being investigated or acted upon.
- `reviewed` — reviewed for a stated purpose; not necessarily true or successful.
- `on_hold` — intentionally paused.
- `rejected` — a proposal or hypothesis was rejected for a stated reason.
- `archived` — retained for history and not currently active.

Status describes workflow, not truth. `reviewed` MUST NOT be interpreted as factually true. `rejected` MUST NOT imply that a record should be deleted.

### 6.3 Epistemic state

Epistemic state MUST be represented separately from workflow status when material. Implementations SHOULD distinguish states such as confirmed observation, sourced claim, hypothesis, untested proposal, inconclusive result, unknown, contradicted, and rejected by evidence.

A failed experiment is a result, not necessarily a rejected record. Unknown is not a negative result. A generated answer is not an observation unless it is independently observed and recorded as such.

## 7. Provenance, evidence, and relationships

### 7.1 Provenance

A provenance object MUST include `source_type` and MAY include `source_id` and additional metadata.

Recommended source types include `user`, `observation`, `external_source`, `experiment`, `module`, `llm_output`, and `unknown`. Source type identifies origin; it does not establish correctness.

### 7.2 Evidence

Evidence SHOULD preserve enough information to locate or reconstruct the basis of a claim, such as a source URL, experiment ID, observation ID, timestamp, or excerpt reference. Missing evidence MUST NOT be fabricated.

### 7.3 Relations

Each relation SHOULD include:

- `target_id` — target record identifier;
- `relation_type` — meaning of the relationship;
- optional `note` — explanation or scope.

Recommended relation types include `supports`, `contradicts`, `derived_from`, `tests`, `refines`, `related_to`, and `analogous_to`.

A missing target MUST be reported as unresolved. Implementations MUST NOT silently replace it with an unrelated record.

## 8. Analogy model

An analogy is a structured, revisable claim about a mapping between concepts or relationships across domains. Similarity alone MUST NOT be treated as proof that mechanisms or outcomes are identical.

An analogy record SHOULD preserve:

- source and target record IDs or domain references;
- explicit mappings between source and target elements;
- supporting evidence;
- scope conditions;
- non-mappings or known differences;
- counterexamples;
- validation state;
- unresolved questions.

Recommended validation states:

- `candidate` — relationship proposed;
- `mapped` — correspondence made explicit;
- `tested` — one or more tests performed;
- `supported` — supported within a stated scope;
- `rejected` — rejected for a stated reason;
- `inconclusive` — evidence does not settle the question;
- `unverified` — not yet tested.

Implementations MAY use a more detailed model but MUST preserve the distinction between candidate generation and validation. Changes MUST be recorded as a revision or a new linked record, not silently substituted for the earlier claim.

## 9. Module contract

Each module MUST declare:

- `module_id`;
- `module_version`;
- supported schema versions;
- required inputs;
- output contract;
- declared capabilities;
- failure behavior.

A module MUST return a proposal or a defined result. It MUST NOT bypass core validation to mutate the canonical store.

### 9.1 Learning Module

Proposes revisions based on observations, evidence, prior hypotheses, and differences between expected and observed outcomes.

A proposal SHOULD identify the affected record, proposed change, supporting evidence, uncertainty, and unresolved issues. A model-generated revision alone MUST NOT cause a record to be marked confirmed.

### 9.2 Exploration Module

Proposes alternative hypotheses, branches, questions, and cross-domain analogies.

A proposal SHOULD explain its relationship to the current objective and identify assumptions or scope limits. Novelty alone MUST NOT be treated as utility or correctness.

### 9.3 Evaluation Module

Evaluates records, proposals, modules, or experiments against explicit criteria.

An evaluation SHOULD include target, criteria, metrics, evidence, limitations, and evaluation version. A score MUST NOT be presented without defining what it measures.

### 9.4 Module replacement

A module MAY be replaced or disabled without changing the core schema. Replacement MUST NOT silently rewrite previous results. Re-evaluation of historical data MUST create identifiable new results, including module version and relevant settings.

### 9.5 Failure behavior

On malformed input, missing dependencies, unsupported schema versions, or internal errors, a module MUST fail explicitly or return a typed failure result. It MUST NOT fabricate success to hide a failure. Partial results MUST be marked as partial.

## 10. Controlled mutation and revision history

1. Modules produce proposed changes; they do not directly alter canonical records.
2. The core validates fields, statuses, identity, references, and applicable invariants.
3. A proposal MAY be accepted, rejected, or deferred.
4. An accepted update MUST increment the revision and update `updated_at`.
5. Implementations SHOULD preserve the prior record or a diff sufficient to reconstruct the change.
6. Failed validation MUST NOT partially commit a change.
7. If persistence fails, the system MUST NOT claim the update was saved.
8. Destructive changes SHOULD be explicit and auditable. Deleting a record referenced elsewhere SHOULD be surfaced.

Human approval is a valid implementation of the decision gate.

## 11. Retrieval and context efficiency

Retrieval policy is implementation-defined. A conforming implementation SHOULD:

- prioritize the current objective and relevant linked records;
- include constraints, unresolved questions, and material counterevidence;
- avoid loading unrelated projects by default;
- preserve enough provenance to distinguish facts from hypotheses;
- report when relevant records are unavailable or truncated;
- avoid claiming that omitted context was considered.

Token budgets, ranking algorithms, embedding models, and caches are module or adapter concerns, not Core Contract fields.

## 12. Persistence and portability

The logical record model MUST be serializable to JSON-compatible data. A human-readable Markdown representation MAY be used alongside it.

Storage adapters MUST document lossy conversions or unsupported fields. Moving data between adapters SHOULD preserve IDs, statuses, provenance, relationships, timestamps, revision numbers, and extension payloads.

No particular database or repository layout is required.

## 13. Security and responsible use

Implementations SHOULD treat imported documents and model-generated text as data rather than executable instructions. Instructions contained in a record MUST NOT automatically override host security rules or the user's explicit intent.

Credentials, access tokens, and other secrets SHOULD NOT be stored in ordinary index records. External actions with material consequences SHOULD require authorization appropriate to the deployment.

Index Hybrid is an information framework, not a guarantee that a proposed action is safe, lawful, or correct.

## 14. Conformance tests

A conforming implementation MUST test applicable requirements. The initial suite SHOULD include:

| Test ID | Test | Expected behavior |
|---|---|---|
| C-001 | Required fields | Reject missing required fields or invalid types |
| C-002 | Identity uniqueness | Reject accidental ID reuse for a different record |
| C-003 | Provenance preservation | Preserve source category and unknown details |
| C-004 | Unknown preservation | Do not convert unknown or untested into confirmed or failed |
| C-005 | Revision increment | Accepted update increments revision |
| C-006 | Atomic validation | Invalid proposal does not partially commit |
| C-007 | Module isolation | Module cannot silently change core semantics |
| C-008 | Analogy uncertainty | Candidate analogy remains unverified until tested |
| C-009 | Missing reference | Report unresolved relation targets |
| C-010 | Persistence failure | Do not claim a failed write was committed |
| C-011 | Module replacement | Historical outputs remain attributable to their producing module version |
| C-012 | Retrieval boundaries | Unrelated project context is not silently merged into the active project |

Passing these tests does not prove factual accuracy or general reasoning quality. Those require separate benchmarks.

### 14.1 Evaluation metrics

Implementations MAY benchmark retrieval fidelity, objective retention, provenance traceability, unsupported-certainty rate, information loss across revisions, task success under a defined protocol, token and latency cost, and compatibility across module versions.

Metrics MUST have defined measurement procedures. Target thresholds SHOULD be set after establishing a baseline.

## 15. Versioning and compatibility

The specification uses `MAJOR.MINOR.PATCH`:

- **MAJOR:** incompatible changes to core semantics or required fields.
- **MINOR:** backward-compatible additions to the core contract.
- **PATCH:** clarifications or corrections that do not change intended semantics.

Implementations MUST identify the schema version used by each record. A reader that does not support a record's schema version MUST report the limitation and MUST NOT silently reinterpret the record.

A migration SHOULD document source version, target version, transformation, and any information that cannot be preserved. Core changes require an update to this specification and relevant conformance tests.

## 16. Non-goals

Index Hybrid does not prescribe a particular LLM, hidden model reasoning, an automatic truth oracle, a single learning or analogy algorithm, a mandatory database or UI, automatic real-world action execution, or guaranteed persistent memory for an LLM.

## 17. Implementation backlog

- Publish machine-validated JSON Schemas for records and analogy objects.
- Define canonical schemas for evidence and relation objects.
- Define deterministic serialization if content hashing or reproducible snapshots are required.
- Implement a reference validator and revision store.
- Create valid, invalid, unknown, and contradictory test fixtures.
- Benchmark retrieval quality and context cost on representative tasks.
- Document migration behavior before declaring the specification stable.

## 18. Summary

Index Hybrid has one stable contract and many replaceable ways to use it.

The core preserves identity, provenance, uncertainty, relationships, and revision history. Learning proposes updates; exploration proposes new paths and analogies; evaluation tests them; adapters connect the system to storage and tools. Accepted changes pass through a validation and commit boundary.

**The goal is not to freeze thought. It is to preserve the meaning of records while allowing methods of thinking, learning, and exploring to change.**
