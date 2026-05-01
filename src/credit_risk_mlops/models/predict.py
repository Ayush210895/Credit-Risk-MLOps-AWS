"""Prediction helpers."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from credit_risk_mlops.config.settings import MODEL_PATH


def load_model(path: str | Path = MODEL_PATH):
    model_path = Path(path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model artifact not found: {model_path}")
    return joblib.load(model_path)


def predict_default_probability(model, payload: dict[str, object]) -> float:
    row = pd.DataFrame([payload])
    return float(model.predict_proba(row)[:, 1][0])
