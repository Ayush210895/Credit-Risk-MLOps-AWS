#!/usr/bin/env python3
"""Train and persist the credit-risk model."""

from __future__ import annotations

import argparse
from pathlib import Path

from credit_risk_mlops.config.settings import METRICS_PATH, MLFLOW_EXPERIMENT_NAME, MODEL_PATH, RAW_DATA_PATH, REPORT_PATH, SAMPLE_DATA_PATH
from credit_risk_mlops.data.load_data import load_credit_data
from credit_risk_mlops.models.train import save_model_artifacts, train_model
from credit_risk_mlops.tracking.mlflow_tracking import log_training_run


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train credit-risk model")
    parser.add_argument("--data", type=Path, default=None, help="CSV path. Defaults to raw OpenML data if present, else sample data.")
    parser.add_argument("--model-type", default="logistic_regression", choices=["logistic_regression", "random_forest"])
    parser.add_argument("--tracking-uri", default=None, help="Optional MLflow tracking URI. Defaults to local SQLite metadata.")
    parser.add_argument("--experiment-name", default=MLFLOW_EXPERIMENT_NAME, help="MLflow experiment name.")
    parser.add_argument("--no-mlflow", action="store_true", help="Skip MLflow tracking for this run.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_path = args.data or (RAW_DATA_PATH if RAW_DATA_PATH.exists() else SAMPLE_DATA_PATH)
    df = load_credit_data(data_path)
    result = train_model(df, model_type=args.model_type)
    save_model_artifacts(result)
    print(f"Trained {result['metrics']['model_type']} on {result['metrics']['rows']} rows")
    if not args.no_mlflow:
        run_id = log_training_run(
            result,
            params={
                "data_path": data_path,
                "model_type": args.model_type,
                "feature_count": len(result["feature_columns"]),
                "test_size": 0.25,
                "positive_label": "bad",
            },
            artifact_paths=[MODEL_PATH, METRICS_PATH, REPORT_PATH],
            tracking_uri_override=args.tracking_uri,
            experiment_name=args.experiment_name,
        )
        print(f"MLflow run logged: {run_id}")


if __name__ == "__main__":
    main()
