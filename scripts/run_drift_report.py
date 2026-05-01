#!/usr/bin/env python3
"""Generate a basic numeric drift report."""

from __future__ import annotations

import argparse
from pathlib import Path

from credit_risk_mlops.data.load_data import load_credit_data
from credit_risk_mlops.monitoring.drift import numeric_drift_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate drift report")
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("reports/drift_report.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    reference = load_credit_data(args.reference)
    current = load_credit_data(args.current)
    report = numeric_drift_report(reference, current)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(args.output, index=False)
    print(args.output)


if __name__ == "__main__":
    main()
