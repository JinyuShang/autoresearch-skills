import unittest

from plan_capacity import estimate, estimate_api_mode
from preflight import validate as validate_contract
from verify_lineage import validate as validate_lineage


class ToolTests(unittest.TestCase):
    def test_capacity_includes_reacquisition_risk(self):
        result = estimate(10, 100, 2, 23, 5, 1, 0.5, 80)
        self.assertEqual(result["expected_reacquisition_loss"], 40)
        self.assertEqual(result["arithmetic_recommendation"], "hybrid")
        self.assertEqual(result["hourly_reacquisition_break_even_probability"], 0)

    def test_capacity_reports_hourly_risk_break_even(self):
        result = estimate(3, 100, 1, 20, 0, 0, 0.2, 100)
        self.assertEqual(result["hourly_reacquisition_break_even_probability"], 0.37)

    def test_api_mode_chooses_eligible_plan(self):
        result = estimate_api_mode(1000, 0.2, 100, 1000, 0.3, True)
        self.assertEqual(result["arithmetic_recommendation"], "plan")

    def test_api_mode_rejects_ineligible_plan(self):
        result = estimate_api_mode(1000, 0.2, 50, 1000, 0.3, False)
        self.assertEqual(result["arithmetic_recommendation"], "payg")

    def test_preflight_rejects_placeholders(self):
        errors = validate_contract({"task_id": "todo", "tracks": ["same", "same"]})
        self.assertTrue(any("task_id" in error for error in errors))
        self.assertTrue(any("two distinct" in error for error in errors))

    def test_preflight_accepts_complete_contract(self):
        contract = {
            "task_id": "public-task",
            "metric_name": "validation_loss",
            "metric_direction": "minimize",
            "improvement_threshold": 0.01,
            "randomness_protocol": "three fixed training seeds",
            "tracks": ["lane-a", "lane-b"],
            "development_runtime": "compose development profile",
            "target_harness": "pinned target backend version",
            "requires_gpu": True,
            "backend_gpu_evidence": "official capability reference and planned real trial",
            "persistent_snapshot": "object storage snapshot with hashes",
            "stop_loss": "stop after two failed pilots",
        }
        self.assertEqual(validate_contract(contract), [])

    def test_lineage_rejects_spliced_receipt(self):
        run = self._run()
        run["receipt_run_id"] = "another-run"
        self.assertTrue(any("receipt_run_id" in error for error in validate_lineage({"runs": [run]})))

    def test_lineage_accepts_consistent_trial(self):
        self.assertEqual(validate_lineage({"runs": [self._run()]}), [])

    @staticmethod
    def _run():
        return {
            "run_id": "run-001",
            "role": "lane-a",
            "training_seed": 7,
            "replicate_id": 1,
            "source_sha256": "a" * 64,
            "config_sha256": "b" * 64,
            "receipt_run_id": "run-001",
            "artifact_run_id": "run-001",
        }


if __name__ == "__main__":
    unittest.main()
