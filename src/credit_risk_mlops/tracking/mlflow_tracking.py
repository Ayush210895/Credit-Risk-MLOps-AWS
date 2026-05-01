"""MLflow tracking for model training runs."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import mlflow

from credit_risk_mlops.config.settings import MLFLOW_DB_PATH, MLFLOW_EXPERIMENT_NAME


def tracking_uri(default_db_path: Path = MLFLOW_DB_PATH, override: str | None = None) -> str:
    uri = override or os.environ.get("MLFLOW_TRACKING_URI")
    if uri:
        return uri
    default_db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{default_db_path}"


def log_training_run(
    result: dict[str, Any],
    *,
    params: dict[str, Any],
    artifact_paths: list[Path],
    tracking_uri_override: str | None = None,
    experiment_name: str = MLFLOW_EXPERIMENT_NAME,
) -> str:
    """Log a completed training run and return the MLflow run ID."""
    metrics = result["metrics"]
    mlflow.set_tracking_uri(tracking_uri(override=tracking_uri_override))
    mlflow.set_experiment(experiment_name)

    run_name = f"{metrics['model_type']}-{metrics['rows']}-rows"
    with mlflow.start_run(run_name=run_name) as run:
        mlflow.set_tags(
            {
                "project": "credit-risk-mlops-aws",
                "stage": "training",
                "model_type": str(metrics["model_type"]),
            }
        )
        mlflow.log_params({key: _stringify(value) for key, value in params.items()})
        mlflow.log_metrics(_numeric_metrics(metrics))
        for artifact_path in artifact_paths:
            if artifact_path.exists():
                mlflow.log_artifact(str(artifact_path), artifact_path="training")
        return run.info.run_id


def _numeric_metrics(metrics: dict[str, Any]) -> dict[str, float]:
    numeric: dict[str, float] = {}
    for key, value in metrics.items():
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            numeric[key] = float(value)
    return numeric


def _stringify(value: Any) -> str:
    if isinstance(value, Path):
        return str(value)
    return str(value)
