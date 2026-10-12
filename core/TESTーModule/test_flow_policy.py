import unittest
from flow_policy import AnswerMode, SequentialAnswerRunner, Stage
from answer_runner import DemoGenerator

class SequentialFlowTests(unittest.TestCase):
    def setUp(self): self.runner = SequentialAnswerRunner(DemoGenerator())
    def test_all_modes_complete(self):
        for mode in AnswerMode:
            run = self.runner.run("test task", mode)
            result = self.runner.validate_run(run)
            self.assertEqual(run.status, "completed")
            self.assertTrue(result["ordered_prefix_valid"])
            self.assertTrue(result["hash_links_valid"])
            self.assertTrue(result["completed_all_stages"])
    def test_hash_chain(self):
        run = self.runner.run("test task", AnswerMode.BOTH)
        for i, item in enumerate(run.artifacts):
            self.assertEqual(item.previous_artifact_hash,
                             run.artifacts[i-1].content_hash if i else None)
    def test_bad_order_rejected(self):
        with self.assertRaises(ValueError):
            SequentialAnswerRunner(DemoGenerator(),
                [Stage.INPUT, Stage.DECOMPOSE, Stage.SCOPE, Stage.BRANCH, Stage.CHECK, Stage.ANSWER])

if __name__ == "__main__": unittest.main()
