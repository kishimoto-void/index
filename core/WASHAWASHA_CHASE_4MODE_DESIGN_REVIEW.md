# WASHAWASHA Chase — 4 Answer-Mode Probe
## ChatGPT Design Review / Experimental Protocol v0.1

**Status:** Experimental proposal  
**Target:** Index Hybrid / Connect Core  
**Purpose:** Compare externally observable problem-solving traces under four explicitly declared answer policies.

---

## 1. Design verdict

The four answer modes are a useful first experimental axis:

1. `general_answer`
2. `boundary_exploration`
3. `both`
4. `undecided`

They should be treated as **declared response policies**, not as claims about hidden model reasoning.

The experiment should compare the visible traces, not assume the mode caused every observed difference. Prompt wording, sampling, model/version, task difficulty, and the presence of the marker protocol may all affect output.

### Core recommendation

Separate three concerns:

- **Connect Core:** stores events, links, revisions, and observations.
- **Probe protocol:** defines the four conditions, marker vocabulary, and required fields.
- **Evaluator:** computes observable metrics and reports missing/ambiguous evidence.

Do not embed all experimental interpretation into `core.py`.

---

## 2. Four answer modes

| Mode | Instructional intent | Expected output contract |
|---|---|---|
| `general_answer` | Give the most useful ordinary answer within the stated scope. | Answer, key assumptions, uncertainty/limitations when material. Do not deliberately expand into exhaustive edge-case exploration. |
| `boundary_exploration` | Explore where a generalization stops holding. | Candidate rule, boundary conditions, counterexamples/edge cases, unresolved frontier. Do not imply the boundary is exhaustive unless tested. |
| `both` | Give the ordinary answer and then probe its limits. | Clearly separated general answer and boundary exploration. |
| `undecided` | Leave the answer policy unresolved as a control/diagnostic condition. | Record that no mode was selected. Do not treat this as a valid final-answer policy or compare its answer quality as if it were equivalent to the other three. |

### Important distinction

`undecided` is not a fourth style of good answer. It is a **policy-not-selected state**. For a clean experiment, run it as a diagnostic/control condition: does the system ask for clarification, default silently, or produce an unmarked mixture?

Record that behavior; do not force it to pretend a policy was explicitly selected.

---

## 3. Recommended marker vocabulary

Markers describe observable events, not private internal reasoning.

| Marker | Meaning | Minimum payload |
|---|---|---|
| `INPUT` | Task received | `problem_id`, `problem_text` or stable task reference |
| `SCOPE` | Declared scope / target | `goal`, `constraints`, `answer_mode` |
| `OBSERVE` | Visible facts extracted | `observations`, `unknowns` |
| `REFRAME` | Problem wording or representation changed | `before_representation`, `after_representation`, `reason_stated` |
| `HYPOTHESIS` | Candidate explanation or rule | `claim`, `support`, `uncertainties` |
| `BRANCH` | Explicit alternative path opened | `branch_id`, `parent_event_id`, `question` |
| `TRANSFORM` | Abstraction, substitution, premise change, or representation transform | `transform_type`, `before`, `after` |
| `COMPARE` | Alternatives compared | `items_compared`, `criteria` |
| `RETURN` | Explicit return to earlier question/state | `target_event_id`, `return_reason` |
| `CONVERGE` | One or more paths combined or selected | `source_event_ids`, `selection_basis` |
| `BOUNDARY` | Boundary/edge case examined | `rule_under_test`, `case`, `result` |
| `UNKNOWN` | Important unknown preserved | `unknown`, `why_material` |
| `ANSWER` | Final answer emitted | `answer_summary`, `answer_mode`, `scope_statement` |
| `LIMITATION` | Limits of answer stated | `limitation`, `effect_on_conclusion` |
| `FAIL` | Attempt failed or was abandoned | `attempt`, `observed_failure`, `next_action` |

Not every task needs every marker. Missing markers should not automatically count as a failure; the evaluator should distinguish `not applicable`, `not observed`, and `not reported`.

### Minimum required markers

Every run:
- `INPUT`
- `SCOPE`
- `ANSWER`

When applicable:
- `BRANCH` for explicit alternatives
- `RETURN` for a documented return to an earlier representation
- `BOUNDARY` for an actually tested edge/boundary case
- `UNKNOWN` when a material uncertainty is intentionally preserved

---

## 4. Protocol for a fair comparison

### 4.1 Hold constant

For each four-mode batch, hold constant as far as practical:

- exact task text and supplied context
- model and model version
- tools and tool access
- output length budget
- temperature/sampling settings, if controllable
- marker schema and reporting format
- scoring rubric

Only the declared answer mode should intentionally vary.

### 4.2 Repeat

One run per mode is a demonstration, not evidence of a stable pattern. Run multiple repetitions per mode if feasible, randomize the order, and record the run ID and timestamp.

Do not compare one unusually long boundary answer with one short general answer without accounting for output budget.

### 4.3 Avoid marker-induced confounding

A required marker format can change the response. Use the same logging scaffold for all modes. If practical, add a separate unmarked baseline to estimate the effect of the marker protocol itself.

### 4.4 Do not demand hidden chain-of-thought

Ask for concise, externally checkable artifacts:
- assumptions explicitly stated
- candidate rules
- alternatives considered at a summary level
- boundary cases actually tested
- answer scope and limitations
- visible changes from earlier representations

Do not ask the model to reveal private internal reasoning. A trace is a record of reported/externalized steps, not a complete transcript of internal computation.

---

## 5. Metrics: record first, interpret later

Recommended raw metrics:

- `event_count`
- `marker_counts`
- `branch_count`
- `explicit_return_count`
- `explicit_convergence_count`
- `reframe_count`
- `boundary_cases_attempted`
- `boundary_cases_resolved`
- `unknowns_preserved`
- `answer_mode_declared`
- `answer_mode_consistent_with_output` (human- or rubric-assessed)
- `initial_problem_preserved` (yes/no/unclear)
- `answer_correctness` (task-specific external rubric)
- `coverage_of_requested_scope`
- `unsupported_claim_count`
- `missing_required_fields`

### Guardrails

- More branches does not automatically mean better reasoning.
- More boundary cases does not automatically mean better coverage.
- A return to the original problem is not automatically drift or failure.
- A changed representation is not automatically progress.
- `undecided` should not be ranked as a normal answer style.
- Correctness must be scored independently from trace richness.
- Do not create a single composite score until the individual metrics have been inspected.

Keep raw observations separate from interpretations.

---

## 6. Suggested experiment tasks

Use a small task set with different structures:

1. **Simple factual task:** ordinary answer should be sufficient.
2. **Rule/generalization task:** several examples invite a rule, but the rule has a boundary.
3. **Ambiguous task:** multiple plausible interpretations; scope choice matters.
4. **Counterexample task:** a broad claim is challenged by edge cases.
5. **Multi-step planning task:** branches, returns, and convergence may be observable.

Use the exact same task within each four-mode batch. Avoid using only a task whose answer is already known to favor boundary exploration.

---

## 7. Example run envelope

This is an example record, not a mandatory JSON serialization format:

```json
{
  "experiment_id": "washi-4mode-001",
  "run_id": "task-02-boundary-r1",
  "problem_id": "task-02",
  "mode_condition": "boundary_exploration",
  "declared_answer_mode": "boundary_exploration",
  "model": "record exact model identifier",
  "model_version": "record if available",
  "task_hash": "hash of exact task text and context",
  "events": [
    {
      "marker": "INPUT",
      "summary": "Rule/generalization task received",
      "payload": {"problem_id": "task-02"}
    },
    {
      "marker": "SCOPE",
      "summary": "Boundary of the proposed rule is the target",
      "payload": {"answer_mode": "boundary_exploration"}
    },
    {
      "marker": "BOUNDARY",
      "summary": "Candidate edge case tested",
      "payload": {
        "rule_under_test": "rule R",
        "case": "case C",
        "result": "supports / contradicts / inconclusive"
      }
    },
    {
      "marker": "ANSWER",
      "summary": "Boundary-focused conclusion",
      "payload": {
        "answer_mode": "boundary_exploration",
        "scope_statement": "Boundary explored for tested cases; not exhaustive"
      }
    }
  ]
}
```

In real use, `task_hash` should be calculated from a canonical representation of the exact task and context. Do not use a placeholder string as if it were a computed hash.

---

## 8. Connect Core integration notes

Current `core.py` v0.3.0 has:
- `AnswerMode`
- `mark_flow(..., answer_mode=...)`
- `chase_flow(...)`
- explicit event links and parent event IDs

Recommended near-term additions, after protocol trials:

1. Add a small `ProbeRun` wrapper containing experiment ID, run ID, task hash, mode condition, model metadata, and event IDs.
2. Validate required marker payloads at the protocol layer, not inside generic Connect Core.
3. Add `not_applicable` / `not_observed` distinctions to evaluator results.
4. Add import/export of run bundles for comparing multiple modes.
5. Add a deterministic report that shows raw metrics before interpretations.

Do not make `ConnectCore` itself decide whether an answer is correct, whether a path is “good,” or whether drift occurred.

---

## 9. Acceptance checks for v0.1

- [ ] All four mode labels are accepted as declared conditions.
- [ ] Final `ANSWER` event cannot omit `answer_mode`.
- [ ] `undecided` is visibly reported as unresolved, not silently converted to another mode.
- [ ] Each event has a stable event ID and sequence number.
- [ ] Parent links and explicit return/convergence links survive export.
- [ ] The exact task/context and model metadata can be associated with each run.
- [ ] Missing markers are not automatically treated as zero behavior.
- [ ] Correctness and trace metrics are reported separately.
- [ ] A mode declaration is not treated as proof that the output followed that mode.
- [ ] No internal-chain-of-thought access is required.

---

## 10. ChatGPT design review conclusion

**Recommendation: proceed with a small four-mode pilot, but keep the protocol and Connect Core separate.**

The strongest design choice is to treat answer mode as an explicit experimental condition and the trace as observable evidence. The most important risk is conflating a declared policy, an observed output pattern, and a causal explanation.

The first milestone should not be “prove one mode is best.” It should be:

> Determine whether the four modes produce reliably distinguishable, externally recordable differences in scope, branching, boundary coverage, returns, and final answers under controlled conditions.

That is a modest, falsifiable, and useful first experiment for Index Hybrid.
