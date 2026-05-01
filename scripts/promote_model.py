#!/usr/bin/env python3
"""Promote a candidate model after metric approval checks."""

from __future__ import annotations

import argparse

from credit_risk_mlops.models.registry import promote_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Promote a candidate credit-risk model")
    parser.add_argument("--model-id", default=None, help="Candidate model ID. Defaults to the latest candidate.")
    parser.add_argument("--min-roc-auc", type=float, default=0.70, help="Minimum ROC AUC required for approval.")
    parser.add_argument(
        "--min-average-precision",
        type=float,
        default=0.50,
        help="Minimum average precision required for approval.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    approved = promote_model(
        model_id=args.model_id,
        min_roc_auc=args.min_roc_auc,
        min_average_precision=args.min_average_precision,
    )
    print(f"Approved model: {approved['model_id']}")
    print(f"Serving artifact: {approved['approved_artifact_path']}")


if __name__ == "__main__":
    main()
