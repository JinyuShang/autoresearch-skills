import unittest

from authoring_gate import STAGES, required_through, validate


class AuthoringGateTests(unittest.TestCase):
    def test_later_stage_includes_all_earlier_requirements(self):
        expected = sum((len(fields) for fields in STAGES.values()), 0)
        self.assertEqual(len(required_through("release")), expected)

    def test_placeholder_fails_closed(self):
        evidence = {field: "evidence/ref" for field in required_through("selection")}
        evidence["license_evidence"] = "TBD"
        self.assertEqual(validate("selection", evidence), ["license_evidence"])

    def test_complete_pilot_passes(self):
        evidence = {field: "evidence/ref" for field in required_through("pilot")}
        self.assertEqual(validate("pilot", evidence), [])

    def test_unknown_stage_is_rejected(self):
        with self.assertRaises(ValueError):
            required_through("later")


if __name__ == "__main__":
    unittest.main()
