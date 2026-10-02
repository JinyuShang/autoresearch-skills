#!/usr/bin/env python3
"""Compare GPU rental plans while accounting for reacquisition risk."""

from __future__ import annotations

import argparse
import json
import math


def estimate(
    hourly_price: float,
    daily_price: float,
    pilot_hours: float,
    formal_hours: float,
    api_cost: float,
    storage_cost: float,
    reacquire_probability: float,
    reacquire_impact: float,
) -> dict[str, object]:
    for name, value in {
        "hourly_price": hourly_price,
        "daily_price": daily_price,
        "pilot_hours": pilot_hours,
        "formal_hours": formal_hours,
        "api_cost": api_cost,
        "storage_cost": storage_cost,
        "reacquire_impact": reacquire_impact,
    }.items():
        if value < 0:
            raise ValueError(f"{name} must be non-negative")
    if not 0 <= reacquire_probability <= 1:
        raise ValueError("reacquire_probability must be between 0 and 1")

    expected_risk = reacquire_probability * reacquire_impact
    fixed = api_cost + storage_cost
    hourly = hourly_price * (pilot_hours + formal_hours) + fixed + expected_risk
    daily_days = math.ceil((pilot_hours + formal_hours) / 24)
    formal_days = math.ceil(formal_hours / 24)
    daily = daily_price * daily_days + fixed
    hybrid = hourly_price * pilot_hours + daily_price * formal_days + fixed
    totals = {"hourly": hourly, "daily": daily, "hybrid": hybrid}
    recommendation = min(totals, key=totals.get)
    return {
        "expected_reacquisition_loss": round(expected_risk, 2),
        "charged_days": {"daily": daily_days, "hybrid_formal": formal_days},
        "totals": {key: round(value, 2) for key, value in totals.items()},
        "arithmetic_recommendation": recommendation,
        "decision_note": (
            "Use the arithmetic result only after the end-to-end pilot passes; "
            "capacity continuity and the experiment stop-loss remain hard gates."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hourly-price", type=float, required=True)
    parser.add_argument("--daily-price", type=float, required=True)
    parser.add_argument("--pilot-hours", type=float, required=True)
    parser.add_argument("--formal-hours", type=float, required=True)
    parser.add_argument("--api-cost", type=float, default=0)
    parser.add_argument("--storage-cost", type=float, default=0)
    parser.add_argument("--reacquire-probability", type=float, default=0)
    parser.add_argument("--reacquire-impact", type=float, default=0)
    args = parser.parse_args()
    try:
        result = estimate(**vars(args))
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
