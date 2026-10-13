# W1 v0.1 — WASHAWASHA Structure Analyzer

**Status:** Specification draft / v0.1  
**Purpose:** Analyze externally observable response structure as a flowchart, explicitly accounting for branches, assumptions, and the stated or inferred reasons for them.

## 1. Purpose

W1 v0.1 turns a target LLM response (and any available prompt/context) into a structured analysis:

1. A flowchart of observable stages and transitions.
2. A branch inventory, including branch count, location, alternatives, and reasons.
3. Two separate assumption ledgers:
   - **Explicit assumptions:** assumptions stated directly in the response or supplied context.
   - **Inferred assumptions:** assumptions the analyst believes may be required to explain the response structure, but which are not explicitly stated.
4. Evidence and uncertainty labels that prevent interpretations from being presented as observed facts.
5. A summary suitable for later hypothesis generation about the conditions that may produce “WASHAWASHA” (branching, reformulation, assumption changes, return, drift, and related observable transitions).

W1 does **not** claim to expose a model's private internal reasoning. It analyzes only available external evidence: prompts, response text, tool-visible actions/logs, and explicit intermediate artifacts supplied for analysis.

## 2. Non-goals

- Do not claim to recover hidden chain-of-thought or internal computation.
- Do not invent a branch merely because a response could have taken another path.
- Do not treat a plausible explanation as a verified cause.
- Do not merge branch count and assumption count.
- Do not equate a branch, a hypothesis, an assumption, and a conclusion.
- Do not force every response into a branching pattern.
- Do not score an answer as good/bad unless a separate evaluation task explicitly requests it.

## 3. Core concepts

### 3.1 Observable stage

A response segment or externally evidenced operation, such as defining the question, introducing a condition, comparing alternatives, revising a premise, returning to an earlier issue, or stating a conclusion.

Each stage should cite its supporting text or artifact. If stage order cannot be established from the evidence, mark the order as uncertain.

### 3.2 Branch

A point where the response explicitly or observably distinguishes two or more alternative paths, cases, interpretations, conditions, or outcomes.

- Count **branch points** separately from **outgoing branches/alternatives**.
- Report both values where possible.
- A list of options is not automatically evidence that the model internally explored every option. Describe it as an output-level alternative set.
- If the response presents a single path and no observable alternatives, report `confirmed_branch_points = 0` and note the evidence scope; do not infer that no internal branching occurred.

### 3.3 Assumption

A proposition accepted provisionally for the purpose of analysis or answering.

**Explicit assumption:** directly stated as an assumption, condition, supposition, simplification, or provisional premise.

**Inferred assumption:** not stated as an assumption, but appears necessary to explain a step, transition, or conclusion. Inferred assumptions must be marked as interpretations, include rationale, and have confidence/uncertainty noted.

Do not count ordinary factual claims as assumptions merely because they could be wrong. If unclear whether an item is an assumption, place it in `uncertain_items` rather than forcing classification.

### 3.4 Reason

A reason is an explanation for why a branch or assumption appears in the response. Separate:
- `stated_reason`: reason explicitly given in the source response/context.
- `analyst_interpretation`: a plausible interpretation based on observable evidence.
- `unknown`: no supported reason can be assigned.

Do not state that a reason is the model's actual internal cause unless independently evidenced. Prefer phrasing such as “the response states…”, “the structure is consistent with…”, and “cause unknown from available evidence.”

## 4. Required output

Every full analysis must contain the following sections in order:

1. **Scope and evidence**
   - Target prompt/context available
   - Response/artifacts analyzed
   - Missing evidence and limitations
2. **Flowchart**
   - Mermaid flowchart or equivalent node-edge representation
   - Evidence references for nodes and edges
   - Uncertain edges marked explicitly
3. **Branch inventory**
   - Branch ID and location
   - Branch point count
   - Number of observable alternatives
   - Alternatives and evidence
   - Stated reason / analyst interpretation / unknown
4. **Assumption ledger — explicit**
   - ID, assumption, evidence, introduction point, status, downstream influence
5. **Assumption ledger — inferred**
   - ID, inferred assumption, evidence supporting inference, rationale, confidence, alternatives, status
6. **Transition and return analysis**
   - Reformulations, premise changes, abstraction shifts, substitutions, return to earlier issue, drift-like changes, unresolved transitions
7. **Counts and accounting**
   - Confirmed branch points
   - Observable alternatives across branch points (do not conflate with branch points)
   - Explicit assumption count
   - Inferred assumption count
   - Uncertain/unclassified candidate count
   - Counts are scoped to the supplied evidence
8. **Unknowns and counter-interpretations**
9. **Structured JSON**
   - Valid JSON conforming to the schema in `schema/w1_analysis.schema.json` (when available)

## 5. Counting rules

- **Branch point count:** number of distinct evidenced locations where at least two alternatives are represented.
- **Alternative count:** number of outgoing options represented at each branch point; report per point and optionally total.
- **Explicit assumption count:** number of unique explicit assumptions. Repetition of the same assumption does not create a new assumption unless its meaning changes.
- **Inferred assumption count:** number of distinct inferred assumptions, kept separate from explicit assumptions.
- **Uncertain candidate count:** items that may be assumptions or branches but lack enough evidence for classification.
- One assumption can support several branches; one branch can involve several assumptions. Never force a one-to-one mapping.
- Deduplicate semantically equivalent items, preserving links to all occurrences.
- If no evidence is supplied for a count, use `null` or “not assessable,” not an invented zero.
- Counts describe the analyzed artifact, not the model's complete internal process.

## 6. Evidence and confidence

Use evidence IDs (e.g., `E1`, `E2`) tied to exact quotes or short paraphrases with a location/segment identifier. Prefer short excerpts; do not reproduce irrelevant source text.

Suggested confidence labels:
- `high`: directly supported by clear, unambiguous evidence.
- `medium`: reasonable interpretation supported by evidence, with plausible alternatives.
- `low`: weakly supported or highly ambiguous.
- `unknown`: evidence is insufficient.

Confidence describes the analysis claim, not the correctness of the original answer.

## 7. Suggested workflow

1. Freeze the target prompt/context and response artifact.
2. Segment the response into observable stages.
3. Identify only evidenced transitions and branch points.
4. Inventory explicit assumptions.
5. Separately propose inferred assumptions; justify each one.
6. Attach stated reasons or clearly labeled interpretations to each branch/assumption.
7. Build the flowchart from the inventory, not from a preconceived narrative.
8. Count and cross-check items.
9. Search for counter-interpretations and missing evidence.
10. Emit the structured report and JSON.

## 8. Relationship to later W1 stages

- **B — mechanism hypotheses:** may use multiple W1 reports to propose candidate structures that could generate observed patterns. B remains a hypothesis, not a fact.
- **LLM audit:** checks coherence, alternative explanations, falsifiability, and whether proposed tests can distinguish hypotheses. LLM agreement is not proof.
- **A — efficient observation plan:** chooses the smallest useful set of observations/interventions that distinguishes competing B hypotheses.
- **Δindex:** may classify claims by evidence maturity, but must preserve uncertainty and provenance.

## 9. Initial validation tests

A v0.1 implementation should pass at least these cases:

1. **Single-path response:** no observable branch point; no forced branch.
2. **Explicit alternatives:** one branch point with two or more alternatives.
3. **Explicit assumption:** counted only in explicit ledger.
4. **Inferred assumption:** counted only in inferred ledger and accompanied by rationale.
5. **Repeated assumption:** semantically duplicate mentions deduplicated, occurrences retained.
6. **Branch without assumption:** branch count increases; assumption count need not.
7. **Assumption supporting multiple branches:** assumption counted once and linked to multiple branches.
8. **Unknown reason:** marked unknown, not fabricated.
9. **Conflicting evidence:** conflict retained and confidence lowered.
10. **No prompt or incomplete context:** scope limitation reported.
11. **Post-hoc rationalization risk:** reasons from the response are labeled as stated reasons, not confirmed internal causes.
12. **Invalid or ambiguous flow order:** uncertain edge/order recorded instead of guessed.

## 10. Version boundary

v0.1 defines the analysis contract and prompt behavior. It does not prescribe a particular model, runtime, graph library, or automatic parser. Keep the output schema stable where practical and version future breaking changes explicitly.
