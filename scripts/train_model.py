#!/usr/bin/env python3
"""Train and persist the credit-risk model."""

from __future__ import annotations

import argparse
from pathlib import Path

from credit_risk_mlops.config.settings import RAW_DATA_PATH, SAMPLE_DATA_PATH
from credit_risk_mlops.data.load_data import load_credit_data
from credit_risk_mlops.models.train import save_model_artifacts, train_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train credit-risk model")
    parser.add_argument("--data", type=Path, default=None, help="CSV path. Defaults to raw OpenML data if present, else sample data.")
    parser.add_argument("--model-type", default="logistic_regression", choices=["logistic_regression", "random_forest"])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_path = args.data or (RAW_DATA_PATH if RAW_DATA_PATH.exists() else SAMPLE_DATA_PATH)
    df = load_credit_data(data_path)
    result = train_model(df, model_type=args.model_type)
    save_model_artifacts(result)
    print(f"Trained {result['metrics']['model_type']} on {result['metrics']['rows']} rows")


if __name__ == "__main__":
    main()
