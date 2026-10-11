# Index Hybrid

**A small, extensible index for carrying context across projects, experiments, and LLM sessions.**

Index Hybrid formalizes the original **Instant Index** idea: record what matters, retrieve only what is relevant, ask an AI or another tool for a useful next action, then append the observed result.

> **Keep the shared data contract stable; make learning, exploration, and evaluation replaceable.**

The project is intended to be easy to copy, personalize, and modify. It does not require a particular LLM, programming language, database, directory layout, or paid service.

## Why Index?

Project context is often scattered across conversations, notes, experiments, and assumptions. Repeating that context wastes time and tokens; merging it carelessly can erase uncertainty or mix unrelated projects.

Index is a **proposal memory**: record experience, consult the next action, act, then append the result.

It helps users:

- preserve the current issue and objective;
- distinguish observations, claims, hypotheses, experiments, and unknowns;
- record what was tried and what actually happened;
- retain failures, differences, and unresolved questions;
- explore analogies across domains without treating resemblance as proof;
- provide an AI with the smallest useful context for the next decision.

## Core loop

```text
INPUT → INDEX → RETRIEVAL → REASONING → PROPOSAL
  ↑                                      ↓
  └──────── OBSERVATION ← ACTION ←───────┘
```

1. **Input** — Record an issue, question, observation, constraint, or result.
2. **Index** — Store it with an identifier, type, status, source, and relationships.
3. **Retrieval** — Select only the context needed for the current task.
4. **Reasoning** — A person, LLM, or replaceable module analyzes that context.
5. **Proposal** — Produce a next action, alternative, or experiment with rationale.
6. **Action** — A person or external system decides whether to carry it out.
7. **Observation** — Record the actual outcome, including failure or uncertainty.

A proposal is not an executed action. An executed action is not automatically a successful result.

## Standard three-layer view

The layers are a **logical view**, not a required physical storage hierarchy.

| Layer | Purpose | Typical contents |
|---|---|---|
| **L1 — Issue / Objective** | Keep the target visible | Issue, objective, scope, constraints, success criteria |
| **L2 — Current State / Analysis** | Describe current understanding | Facts, claims, hypotheses, contradictions, unknowns, next questions |
| **L3 — Experience / Experiments** | Preserve what happened | Conditions, inputs, outputs, observations, differences, failures, reproducibility |

Entries can be linked across layers and reused by multiple issues. Prefer references to one canonical entry over independent copies that may drift apart.

## Stable core, replaceable modules

```text
                   INDEX HYBRID
                        │
              ┌─────────┴─────────┐
              │   Core Contract   │
              │ identity          │
              │ provenance        │
              │ status / revision │
              │ validation        │
              └─────────┬─────────┘
                        │
           ┌────────────┼────────────┐
           │            │            │
        Learning    Exploration   Evaluation
        update      analogy       tests / metrics
        proposals   branching     comparisons
           └────────────┼────────────┘
                        │
                 Storage adapters
              Markdown / JSON / DB
                        │
                 LLM / local harness
```

- **Core Contract** — Defines shared record semantics and integrity rules. Ordinary modules cannot silently redefine it.
- **Learning** — Proposes revisions based on evidence and differences between expectations and observations.
- **Exploration** — Proposes branches, alternative hypotheses, and cross-domain analogies.
- **Evaluation** — Checks consistency, evidence, reproducibility, task performance, and context efficiency.
- **Adapters** — Connect the shared model to files, databases, LLMs, or local harnesses.

Modules propose changes; the core validates them; storage commits accepted changes. Replacing a module must not silently rewrite historical results.

## Analogy without overclaiming

A fishing experiment and an LLM prompt experiment might share a broad pattern:

```text
change a condition → observe a response → revise a hypothesis
```

That resemblance can be useful, but it does not prove that the underlying mechanisms are identical. An analogy should preserve its proposed mappings, evidence, scope conditions, non-matching parts, counterexamples, and validation state.

Exploration should be free to propose surprising connections. Evaluation should be free to reject them.

## Minimal record

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

This is an illustrative record. See [SPECIFICATION.md](SPECIFICATION.md) for the normative field definitions. Markdown is sufficient for a simple human workflow; JSON is useful when a local harness needs predictable parsing and validation.

## Principles

1. **Preserve provenance.** Distinguish user input, observation, external source, inference, and generated proposal.
2. **Keep uncertainty visible.** Unknown, untested, and inconclusive are valid states.
3. **Record differences, not only conclusions.** Preserve the prior state, observed result, and meaningful revision.
4. **Keep projects separable.** Use explicit IDs and relations instead of merging unrelated context.
5. **Separate proposal from execution.** Never report an action or test as completed unless it actually was.
6. **Do not equate analogy with evidence.** Similarity is a hypothesis to test.
7. **Keep the core small.** Put domain-specific fields in extensions or replaceable modules.
8. **Minimize context.** Retrieve only information relevant to the current task.
9. **Prefer inspectable records.** Human-readable Markdown and portable JSON are good starting points.
10. **Support user freedom.** Personalization and local modification are expected.

## What Index does not promise

- It is not automatic or guaranteed persistent memory for an LLM.
- Storing a record does not guarantee that it is true.
- It does not require access to private model reasoning.
- It does not make an analogy valid merely because two patterns look alike.
- It does not require a specific toolchain, model, or storage service.
- It does not autonomously execute real-world actions unless a separate system implements that capability.

A local harness can enforce schema validation, revision handling, retrieval, and commit rules more reliably than prompt instructions alone.

## Getting started

1. Read [SPECIFICATION.md](SPECIFICATION.md).
2. Create one entry for a current issue or objective.
3. Add only the facts, hypotheses, and prior experiences needed for the task.
4. Ask an AI or module to propose a next action and explain its rationale.
5. Decide whether to perform the action.
6. Append the actual result, including uncertainty or failure.
7. Repeat from the updated index.

Start with Markdown. Add JSON schemas, local retrieval, or module code only when there is a concrete need.

## Repository map

- `README.md` — purpose, concepts, and quick start.
- `SPECIFICATION.md` — core contract and module boundaries.
- `プロジェクトエギング/` — a domain-specific example project, kept separate from the general framework.

## Status

**Specification status: Draft 1.0.0.**

This document describes the intended design. A written specification is not evidence of a working implementation. Schema validation, mutation controls, compatibility behavior, and benchmarks must be tested before claiming implementation conformance.

## Contributing

Personalization and experimentation are welcome. For proposed changes to the shared contract, explain the problem, compatibility impact, migration behavior, and tests. Domain-specific ideas should generally begin as examples, extensions, or modules rather than expanding the core prematurely.
