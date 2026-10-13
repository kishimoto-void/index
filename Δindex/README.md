Δ-index — Thinking Circuit

Version: v0.1-draft
Project: Instant Index
Layer: L2 — State / Difference / Hypothesis
Related: γ-index / Experimentis / CHAIN

---

1. Overview

Δ-index is a framework for organizing issues, hypotheses, evidence, uncertainty, and adoption states.

It does not assume that an input can immediately be classified as true or false.

Instead, it treats a problem as a potentially bounded range of possibilities, tracks differences between observations, and updates the current classification through repeated checks.

The objective is not to force every unknown into a FACT.

The objective is to identify:

- What can currently be used.
- What can be provisionally adopted.
- What has a hypothesis but requires verification.
- What remains unknown.
- What evidence is required for a state transition.

Core principle:

«A classification is a current assessment, not an irreversible declaration of truth.»

This design is intended to make the author's own research and debugging easier. It is not presented as a universal model of reasoning.

2. Position in Instant Index

L1: γ-index
    Entry / Reference
         |
         v
L2: Δ-index
    State / Difference / Hypothesis
         |
         v
L3: Experimentis
    Experiments / Evidence / Rejection History

CHAIN connects the relevant issues, documents, observations, and experiments.

Component| Responsibility
γ-index| Locate the entry point and relevant references
Δ-index| Organize states, differences, hypotheses, and verification requirements
Experimentis| Record experiments, evidence, outcomes, and rejection history
CHAIN| Connect references and preserve traceable relationships

Δ-index does not replace experimentation or evidence collection. It identifies what needs to be checked and what conditions would justify changing the current state.

3. Four Δ classifications

Each Δ is assigned one of four current states.

3.1 FACTΔ（実用）

Operationally usable within a defined scope.

The available evidence and verification results are sufficient for the intended use.

Expected conditions may include:

- A defined target and scope.
- Traceable supporting evidence.
- Adequate independence of observations.
- An acceptable tolerance or bounded range.
- Reproducibility appropriate to the intended use.
- No unresolved contradiction that invalidates that use.

FACTΔ（実用） does not mean universally or permanently true.

Its applicability is limited to the conditions under which it was verified.

3.2 FACTΔ（仮採用）

Provisionally adopted for use or continued analysis.

There is sufficient support to proceed provisionally, but one or more verification conditions remain unresolved.

Examples include:

- The evidence supports the hypothesis, but independent confirmation is incomplete.
- The expected range has not been fully established.
- Reproducibility remains uncertain.
- The result is usable for a limited purpose but not yet sufficiently verified for broader application.

The unresolved conditions must remain visible.

3.3 unknownΔ（仮説アリ）

A hypothesis exists, but adoption requirements have not been met.

Possible explanations or candidate models have been identified, but the available evidence is insufficient to justify FACTΔ status.

The next step is to identify what would discriminate between the hypothesis and its alternatives.

Examples:

- Two observations suggest a relationship, but do not adequately bound its range.
- A proposed explanation fits current observations, but competing explanations remain.
- A pattern appears in a test, but independent replication is missing.

A plausible explanation is not automatically a FACT.

3.4 unknownΔ（不明）

The issue cannot currently be classified with sufficient support.

A usable hypothesis may not yet exist, or the observations, definitions, and comparison conditions may be insufficient.

The next step may be to:

- Clarify the question.
- Define the comparison target.
- Collect observations.
- Identify missing variables.
- Generate testable hypotheses.

Unknown is an acceptable state. It does not need to be eliminated artificially.

4. Thinking circuit

[INPUT]
    |
    v
[Define issue and target]
    |
    v
[Identify observations and differences]
    |
    v
[Assign current Δ classification]
    |
    v
[Identify uncertainty and missing evidence]
    |
    v
[Design next check]
    |
    v
[Experimentis: test and record]
    |
    v
[Compare result with expectations]
    |
    v
[Human + LLM review]
    |
    v
[Update current classification]
    |
    +----> Promote
    |
    +----> Maintain
    |
    +----> Demote
    |
    +----> Return to unknown
    |
    +----> Split or revise the hypothesis

The circuit is iterative rather than strictly linear.

A new observation can change the question itself, reveal an overlooked branch, or invalidate the assumptions used by a previous check.

The system must preserve these changes instead of silently rewriting the history.

5. Repeated verification and state transitions

Δ-index uses repeated checks to determine whether the current classification should change.

However, the number of checks alone does not determine the classification.

Repeatedly examining the same evidence does not create new independent evidence.

Each check should clarify at least one of the following:

- Evidence quality.
- Independence of observations.
- Reproducibility.
- The applicable scope.
- The tolerance or bounded range.
- Alternative explanations.
- Contradictions.
- Conditions required for adoption.

Transition principles

Current state| Possible transition| Required justification
unknownΔ（不明）| unknownΔ（仮説アリ）| A testable hypothesis is formed
unknownΔ（仮説アリ）| FACTΔ（仮採用）| Evidence satisfies provisional adoption criteria
FACTΔ（仮採用）| FACTΔ（実用）| Applicable verification requirements are satisfied
Any state| Lower-confidence state| New evidence reveals unresolved contradictions or invalid assumptions
Any state| Revised or split hypotheses| The original issue contains multiple cases or incompatible explanations

These are possible transitions, not guaranteed progression steps.

A hypothesis may remain unknown indefinitely. A provisional classification may be retained when further checks provide no meaningful new information.

Promotion is conditional

A state transition should record:

1. The previous classification.
2. The new classification.
3. The evidence considered.
4. The reason for the transition.
5. Remaining uncertainties.
6. The conditions for subsequent review.

A classification must not be promoted merely because the reasoning sounds convincing.

6. Δ as a range rather than a point

A key design assumption is that a problem may need to be represented as a range of possibilities instead of a single point.

For example, a claim might have several observations supporting it, but the available evidence may not establish a sufficiently narrow range for practical use.

The system therefore distinguishes between:

- Observing a difference.
- Proposing an explanation for that difference.
- Establishing a bounded range.
- Demonstrating that the range is suitable for the intended use.

Example: tolerance

Suppose a numerical result is intended to be accepted within ±0.1.

The system must first define:

- The reference value.
- The measurement or calculation method.
- The meaning of the tolerance.
- The evidence supporting the bound.
- Whether the observations are independent.
- The conditions under which the bound remains valid.

The ±0.1 value is an example, not a universal threshold.

Likewise, a proposed minimum number of independent observations is a verification policy that must be justified for the particular problem.

A sample count by itself cannot establish validity.

Mathematical example

For the equation (1+1=2), mathematical proof within a specified formal system provides a different kind of justification from repeated empirical measurement.

Δ-index should therefore record the type of claim and the appropriate verification method rather than applying one evidence-count rule to every domain.

7. Scope and uncertainty

Every classification should be interpreted in relation to its scope.

A result may be valid in one context and unsupported in another.

For example:

- A behavior is reproducible under a particular configuration.
- The same behavior has not been verified under a different configuration.
- The first result can remain usable within its original scope without being generalized to the second.

When scope changes, the system should determine whether the existing evidence still applies.

It should not automatically transfer a FACTΔ classification to a new context.

Unknown states should also retain their reasons.

Examples:

- Insufficient observations.
- Insufficient independence.
- Unbounded range.
- Conflicting evidence.
- Undefined terms.
- Missing comparison target.
- Unverified generalization.

This makes unknown a structured verification target rather than an empty label.

8. CHAIN integration

CHAIN is a reference graph used to connect related issues, observations, hypotheses, experiments, and records.

It is not the storage location for the entire reasoning process.

A Δ record may reference:

- Its source issue.
- Supporting observations.
- Related hypotheses.
- Relevant experiments.
- Contradictory observations.
- Previous classification records.
- The conditions required for its next review.

Suggested relationships include:

ISSUE
  └── Δ
       ├── supports → HYPOTHESIS
       ├── tested_by → EXPERIMENT
       ├── supported_by → EVIDENCE
       ├── contradicted_by → EVIDENCE
       ├── depends_on → Δ
       └── supersedes → PREVIOUS_STATE

These relationships are illustrative. The exact relation vocabulary should be standardized in the CHAIN specification.

The reference structure should allow the system to trace why a classification was assigned without duplicating every referenced document.

9. Suggested Δ record

A minimal record can be represented as JSON:

{
  "delta_id": "DELTA-001",
  "issue": "Description of the target question",
  "status": "unknown_hypothesis",
  "claim_type": "empirical",
  "scope": null,
  "hypotheses": [],
  "evidence_refs": [],
  "independence_assessment": "unknown",
  "tolerance": null,
  "unknown_reasons": [
    "insufficient_evidence"
  ],
  "next_checks": [],
  "promotion_conditions": [],
  "history_refs": []
}

The status strings are implementation identifiers for the four human-readable classifications:

Human-readable status| Suggested identifier
FACTΔ（実用）| "fact_practical"
FACTΔ（仮採用）| "fact_provisional"
unknownΔ（仮説アリ）| "unknown_hypothesis"
unknownΔ（不明）| "unknown_unresolved"

The record is a starting schema, not a finalized API contract.

A later implementation should define required fields, allowed values, validation rules, and migration behavior explicitly.

10. Human and LLM responsibilities

Δ-index is designed for collaborative classification.

LLM responsibilities

- Organize the issue and available observations.
- Identify differences and missing information.
- Generate candidate hypotheses.
- Suggest discriminating checks.
- Compare results with previous expectations.
- Identify contradictions and unsupported generalizations.
- Recommend a classification change with explicit reasons.

Human responsibilities

- Confirm the intended issue and scope.
- Review the supporting evidence.
- Decide whether provisional adoption is appropriate.
- Approve classification changes.
- Confirm the current snapshot.
- Preserve or reject proposed changes.

The LLM's recommendation does not itself constitute confirmation.

The system should distinguish a proposed update from a human-confirmed state.

11. Snapshot and history

The symbol "=" represents a human-confirmed snapshot at a particular point in time.

It records what was accepted at that moment, not an immutable declaration that can never be revised.

When a new check changes the assessment:

1. Preserve the previous snapshot.
2. Record the new observations and their references.
3. Explain the difference from the previous state.
4. Propose the updated classification.
5. Obtain human confirmation.
6. Save the confirmed version.

The initial persistence workflow can use explicit GitHub commits.

Rollback must preserve the historical record so that a previous classification can be reconstructed and its reasoning reviewed.

Memory persistence, execution state, and rack or working-state management must remain separate concerns. Only explicitly "="-confirmed states are candidates for persistence under this design.

12. Failure modes to check

The following are important validation targets.

- False promotion: A plausible hypothesis is treated as an established fact.
- Evidence duplication: Repeated checks of the same source are counted as independent evidence.
- Scope leakage: A classification is applied outside its verified conditions.
- Unbounded uncertainty: A result is accepted without defining an adequate range or tolerance where one is required.
- Confirmation bias: Supporting observations are retained while contradictory observations are ignored.
- History loss: A new classification overwrites the previous state without preserving the transition.
- Branch loss: A relevant alternative hypothesis disappears during summarization.
- Automatic adoption: An LLM-generated recommendation is treated as human-confirmed.
- Forced resolution: An unknown state is promoted simply to make the index appear complete.

These failure modes should be tested explicitly rather than assumed to be solved by the classification scheme itself.

13. Initial implementation priorities

Recommended implementation order:

1. Define the four status identifiers.
2. Define the minimal Δ record.
3. Implement evidence and history references.
4. Implement a repeatable check-and-review cycle.
5. Record proposed promotions and demotions.
6. Separate proposed states from "="-confirmed snapshots.
7. Integrate CHAIN references.
8. Add validation for missing evidence, scope changes, and contradictory records.
9. Build test cases for promotion, demotion, unresolved unknowns, and hypothesis splitting.

The initial objective is traceability and consistent classification, not automatic truth determination.

14. Design summary

Δ-index treats classification as an evolving assessment supported by evidence and explicit verification conditions.

Its four states distinguish practical adoption, provisional adoption, hypotheses awaiting verification, and unresolved unknowns.

Repeated checks are used to determine whether the current state should change. They do not guarantee promotion.

CHAIN preserves the relationships between issues and their evidence. Experimentis records the actual checks and their outcomes. Human-confirmed snapshots preserve the state accepted at each point in time.

The goal is not to eliminate unknowns. The goal is to make unknowns inspectable, testable, and traceable.
