"""Lightweight model registry and approval gate."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
import shutil
from typing import Any
from uuid import uuid4

from credit_risk_mlops.config.settings import (
    APPROVED_MODEL_METADATA_PATH,
    APPROVED_MODEL_PATH,
    METRICS_PATH,
    MODEL_PATH,
    MODEL_REGISTRY_PATH,
    REPORT_PATH,
)


def register_candidate(
    result: dict[str, Any],
    *,
    model_path: Path = MODEL_PATH,
    metrics_path: Path = METRICS_PATH,
    report_path: Path = REPORT_PATH,
    registry_path: Path = MODEL_REGISTRY_PATH,
    data_path: Path | None = None,
    mlflow_run_id: str | None = None,
) -> dict[str, Any]:
    registry = load_registry(registry_path)
    model_id = _new_model_id(str(result["metrics"]["model_type"]))
    record = {
        "model_id": model_id,
        "status": "candidate",
        "registered_at": _now(),
        "model_type": result["metrics"]["model_type"],
        "metrics": result["metrics"],
        "feature_columns": result["feature_columns"],
        "artifact_path": str(model_path),
        "metrics_path": str(metrics_path),
        "report_path": str(report_path),
        "data_path": str(data_path) if data_path is not None else None,
        "mlflow_run_id": mlflow_run_id,
    }
    registry["models"].append(record)
    save_registry(registry, registry_path)
    return record


def promote_model(
    *,
    model_id: str | None = None,
    min_roc_auc: float = 0.70,
    min_average_precision: float = 0.50,
    registry_path: Path = MODEL_REGISTRY_PATH,
    approved_model_path: Path = APPROVED_MODEL_PATH,
    approved_metadata_path: Path = APPROVED_MODEL_METADATA_PATH,
) -> dict[str, Any]:
    registry = load_registry(registry_path)
    candidate = select_candidate(registry, model_id)
    _validate_candidate(candidate, min_roc_auc=min_roc_auc, min_average_precision=min_average_precision)

    source_path = Path(candidate["artifact_path"])
    if not source_path.exists():
        raise FileNotFoundError(f"Candidate model artifact does not exist: {source_path}")

    approved_model_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, approved_model_path)
    promoted_at = _now()

    for record in registry["models"]:
        if record.get("status") == "approved":
            record["status"] = "archived"
            record["archived_at"] = promoted_at
    candidate["status"] = "approved"
    candidate["approved_at"] = promoted_at
    candidate["approved_artifact_path"] = str(approved_model_path)
    save_registry(registry, registry_path)

    approved_metadata = {
        "model_id": candidate["model_id"],
        "approved_at": promoted_at,
        "approved_artifact_path": str(approved_model_path),
        "source_artifact_path": candidate["artifact_path"],
        "model_type": candidate["model_type"],
        "metrics": candidate["metrics"],
        "mlflow_run_id": candidate.get("mlflow_run_id"),
    }
    approved_metadata_path.parent.mkdir(parents=True, exist_ok=True)
    approved_metadata_path.write_text(json.dumps(approved_metadata, indent=2), encoding="utf-8")
    return approved_metadata


def load_approved_metadata(approved_metadata_path: Path = APPROVED_MODEL_METADATA_PATH) -> dict[str, Any]:
    if not approved_metadata_path.exists():
        raise FileNotFoundError(f"No approved model metadata found: {approved_metadata_path}")
    return json.loads(approved_metadata_path.read_text(encoding="utf-8"))


def resolve_approved_model_path(approved_metadata_path: Path = APPROVED_MODEL_METADATA_PATH) -> Path:
    metadata = load_approved_metadata(approved_metadata_path)
    model_path = Path(metadata["approved_artifact_path"])
    if not model_path.exists():
        raise FileNotFoundError(f"Approved model artifact does not exist: {model_path}")
    return model_path


def select_candidate(registry: dict[str, Any], model_id: str | None = None) -> dict[str, Any]:
    candidates = [record for record in registry["models"] if record.get("status") == "candidate"]
    if model_id is not None:
        matches = [record for record in registry["models"] if record["model_id"] == model_id]
        if not matches:
            raise ValueError(f"Model ID not found in registry: {model_id}")
        return matches[0]
    if not candidates:
        raise ValueError("No candidate models available for promotion")
    return sorted(candidates, key=lambda record: record["registered_at"])[-1]


def load_registry(registry_path: Path = MODEL_REGISTRY_PATH) -> dict[str, Any]:
    if not registry_path.exists():
        return {"models": []}
    return json.loads(registry_path.read_text(encoding="utf-8"))


def save_registry(registry: dict[str, Any], registry_path: Path = MODEL_REGISTRY_PATH) -> None:
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def _validate_candidate(candidate: dict[str, Any], *, min_roc_auc: float, min_average_precision: float) -> None:
    metrics = candidate["metrics"]
    if float(metrics["roc_auc"]) < min_roc_auc:
        raise ValueError(f"roc_auc {metrics['roc_auc']:.4f} is below approval threshold {min_roc_auc:.4f}")
    if float(metrics["average_precision"]) < min_average_precision:
        raise ValueError(
            f"average_precision {metrics['average_precision']:.4f} is below approval threshold {min_average_precision:.4f}"
        )


def _new_model_id(model_type: str) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    return f"{model_type}-{stamp}-{uuid4().hex[:8]}"


def _now() -> str:
    return datetime.now(UTC).isoformat()
