"""Train a credit-risk classifier."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from credit_risk_mlops.config.settings import METRICS_PATH, MODEL_PATH, REPORT_PATH
from credit_risk_mlops.features.build_features import build_preprocessor, split_features_target


def train_model(
    df: pd.DataFrame,
    *,
    model_type: str = "logistic_regression",
    test_size: float = 0.25,
    random_state: int = 42,
) -> dict[str, Any]:
    X, y = split_features_target(df)
    stratify = y if y.nunique() > 1 and y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )
    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(X_train)),
            ("model", _make_model(model_type, random_state)),
        ]
    )
    pipeline.fit(X_train, y_train)

    scores = pipeline.predict_proba(X_test)[:, 1]
    predictions = (scores >= 0.5).astype(int)
    metrics = {
        "rows": int(len(df)),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "positive_rate": float(y.mean()),
        "roc_auc": safe_metric(roc_auc_score, y_test, scores),
        "average_precision": safe_metric(average_precision_score, y_test, scores),
        "precision": safe_metric(precision_score, y_test, predictions, zero_division=0),
        "recall": safe_metric(recall_score, y_test, predictions, zero_division=0),
        "f1": safe_metric(f1_score, y_test, predictions, zero_division=0),
        "model_type": model_type,
    }
    return {
        "pipeline": pipeline,
        "metrics": metrics,
        "feature_columns": X.columns.tolist(),
    }


def save_model_artifacts(result: dict[str, Any], model_path: Path = MODEL_PATH, metrics_path: Path = METRICS_PATH) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(result["pipeline"], model_path)
    metrics_path.write_text(json.dumps(result["metrics"], indent=2), encoding="utf-8")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result["metrics"]), encoding="utf-8")


def render_report(metrics: dict[str, Any]) -> str:
    lines = [
        "# Credit Risk Model Report",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key, value in metrics.items():
        if isinstance(value, float):
            lines.append(f"| {key} | {value:.4f} |")
        else:
            lines.append(f"| {key} | {value} |")
    return "\n".join(lines) + "\n"


def safe_metric(func: Any, y_true: Any, y_pred: Any, **kwargs: Any) -> float:
    try:
        return float(func(y_true, y_pred, **kwargs))
    except ValueError:
        return 0.0


def _make_model(model_type: str, random_state: int) -> Any:
    if model_type == "logistic_regression":
        return LogisticRegression(max_iter=1000, class_weight="balanced")
    if model_type == "random_forest":
        return RandomForestClassifier(n_estimators=150, random_state=random_state, class_weight="balanced")
    raise ValueError(f"Unsupported model_type: {model_type}")
