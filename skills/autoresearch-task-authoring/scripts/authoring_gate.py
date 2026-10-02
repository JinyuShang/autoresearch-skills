#!/usr/bin/env python3
"""Fail closed when an AutoResearch authoring milestone lacks evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PLACEHOLDERS = {"", "todo", "tbd", "unknown", "none", "n/a"}
STAGES = {
    "selection": (
        "source_identity",
        "license_evidence",
        "optimization_surface",
        "duplicate_registry_evidence",
    ),
    "pilot": (
        "baseline_receipt",
        "reference_receipt",
        "effect_noise_decision",
        "evaluator_recompute",
    ),
    "container": (
        "agent_image_digest",
        "verifier_image_digest",
        "hidden_isolation_probe",
        "target_harness_receipt",
    ),
    "long_run": (
        "track_a_lineage",
        "track_b_lineage",
        "snapshot_restore_probe",
    ),
    "release": (
        "independent_qa_report",
        "attachment_privacy_report",
        "artifact_manifest",
    ),
}


def _missing(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip().lower() in PLACEHOLDERS)


def required_through(stage: str) -> tuple[str, ...]:
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage}")
    required: list[str] = []
    for name, fields in STAGES.items():
        required.extend(fields)
        if name == stage:
            break
    return tuple(required)


def validate(stage: str, evidence: dict[str, object]) -> list[str]:
    return [field for field in required_through(stage) if _missing(evidence.get(field))]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=tuple(STAGES))
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.evidence.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        parser.error("evidence must be a JSON object")
    missing = validate(args.stage, payload)
    report = {"stage": args.stage, "status": "PASS" if not missing else "FAIL", "missing": missing}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
