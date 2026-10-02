#!/usr/bin/env python3
"""Detect common private identifiers and secrets without echoing matched values."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    code: str
    path: Path
    line: int


PATTERNS = {
    "MAC_HOME": re.compile(r"/" + r"Users/[A-Za-z0-9._-]+/"),
    "LINUX_HOME": re.compile(r"/" + r"home/[A-Za-z0-9._-]+/"),
    "WINDOWS_HOME": re.compile(r"[A-Za-z]:\\" + r"Users\\[^\\\s]+\\", re.IGNORECASE),
    "PRIVATE_KEY": re.compile("BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "API_TOKEN": re.compile(r"(?:sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AKIA[A-Z0-9]{16})"),
    "BEARER_TOKEN": re.compile(r"Authorization\s*:\s*Bearer\s+(?![<$\[{])[A-Za-z0-9._~+/-]{12,}", re.IGNORECASE),
    "PRIVATE_COLLAB_URL": re.compile(r"https?://[^\s)\]]*(?:" + "feishu" + r"\.cn|" + "larkoffice" + r"\.com)[^\s)\]]*", re.IGNORECASE),
    "PRIVATE_IPV4": re.compile(r"(?<!\d)(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})(?!\d)"),
    "EMAIL": re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])"),
}


def scan(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts:
            continue
        if path.is_symlink():
            findings.append(Finding("SYMLINK", path, 0))
            continue
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for code, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append(Finding(code, path, line_number))
    return findings


def format_finding(finding: Finding, root: Path) -> str:
    return f"{finding.code}:{finding.path.relative_to(root)}:{finding.line}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    findings = scan(root)
    if findings:
        for finding in findings:
            print(format_finding(finding, root))
        print(f"FAIL: {len(findings)} privacy finding(s); matched values were suppressed")
        return 1
    print("PASS: no blocked private identifiers or secret patterns found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
