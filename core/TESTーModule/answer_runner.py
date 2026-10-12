"""Mock demo for the sequential flow protocol; replace with a real model adapter."""
from typing import Any, Mapping, Sequence
import json
from flow_policy import AnswerMode, SequentialAnswerRunner, StageArtifact

class DemoGenerator:
    """Deterministic protocol test double; not an LLM."""
    def generate_stage(self, *, stage: str, task: str, answer_mode: str,
                       prior_artifacts: Sequence[StageArtifact],
                       requirements: Mapping[str, Any]) -> Mapping[str, Any]:
        if stage == "INPUT":
            return {"problem_statement": task, "constraints": ["visible artifacts only"],
                    "unknowns": ["whether trace represents all internal computation"]}
        if stage == "SCOPE":
            return {"answer_mode": answer_mode, "goal": "answer under selected policy",
                    "scope": "visible answer and reported evidence",
                    "stop_condition": "required checks complete or limits recorded"}
        if stage == "DECOMPOSE":
            return {"subquestions": ["What is asked?", "What evidence exists?"],
                    "assumptions": ["only observable data is available"],
                    "knowns": [task], "unknowns": ["unobserved internal computation"]}
        if stage == "BRANCH":
            branches = {
                "general_answer": [{"id": "ordinary", "question": "What is the direct answer?"}],
                "boundary_exploration": [{"id": "rule", "question": "What rule applies?"},
                                         {"id": "edge", "question": "Where might it fail?"}],
                "both": [{"id": "ordinary", "question": "What is the direct answer?"},
                         {"id": "edge", "question": "What are its limits?"}],
                "undecided": [],
            }[answer_mode]
            return {"branches": branches, "branching_rationale": "Mock protocol example only."}
        if stage == "CHECK":
            return {"checks": ["stages present", "unknowns preserved"],
                    "unresolved_items": ["demo does not score factual correctness"],
                    "boundary_status": "candidate boundary path present" if answer_mode in
                        ("boundary_exploration", "both") else "no systematic boundary exploration requested"}
        if stage == "ANSWER":
            return {"answer": f"Demo response to: {task}", "answer_mode": answer_mode,
                    "scope_statement": "Mock output, not a real evaluation.",
                    "limitations": ["DemoGenerator is not an LLM", "no correctness claim"]}
        raise ValueError(f"unknown stage {stage}")

if __name__ == "__main__":
    runner = SequentialAnswerRunner(DemoGenerator())
    for mode in AnswerMode:
        run = runner.run("Can answer creation be constrained by a flow chart?", mode)
        print(json.dumps({"mode": mode.value, "validation": runner.validate_run(run),
                          "stages": [{"stage": a.stage, "hash": a.content_hash[:12]}
                                     for a in run.artifacts]}, ensure_ascii=False, indent=2))
