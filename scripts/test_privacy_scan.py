import tempfile
import unittest
from pathlib import Path

from privacy_scan import format_finding, scan


class PrivacyScanTests(unittest.TestCase):
    def test_safe_public_content_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "safe.md").write_text("Public example at https://github.com/example/project\n", encoding="utf-8")
            self.assertEqual(scan(root), [])

    def test_private_patterns_are_classified_without_echoing_values(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            secret = "sk-" + "A" * 24
            private_url = "https://team." + "feishu" + ".cn/wiki/private"
            email = "person" + "@" + "example.com"
            private_home = "/" + "Users" + "/private-name/project"
            private_ip = ".".join(("192", "168", "2", "4"))
            values = [secret, private_url, email, private_home, private_ip]
            (root / "unsafe.txt").write_text("\n".join(values), encoding="utf-8")
            findings = scan(root)
            codes = {finding.code for finding in findings}
            self.assertEqual(codes, {"API_TOKEN", "PRIVATE_COLLAB_URL", "EMAIL", "MAC_HOME", "PRIVATE_IPV4"})
            output = "\n".join(format_finding(finding, root) for finding in findings)
            for value in values:
                self.assertNotIn(value, output)

    def test_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.txt"
            target.write_text("public\n", encoding="utf-8")
            (root / "alias.txt").symlink_to(target)
            self.assertIn("SYMLINK", {finding.code for finding in scan(root)})


if __name__ == "__main__":
    unittest.main()
