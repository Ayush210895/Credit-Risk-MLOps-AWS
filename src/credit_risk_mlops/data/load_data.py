"""Load and validate credit-risk tabular data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from credit_risk_mlops.config.settings import SAMPLE_DATA_PATH, TARGET_COLUMN


def load_credit_data(path: str | Path | None = None) -> pd.DataFrame:
    data_path = Path(path) if path else SAMPLE_DATA_PATH
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    df = pd.read_csv(data_path)
    validate_credit_data(df)
    return df


def validate_credit_data(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Credit risk dataset is empty")
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")
    if df[TARGET_COLUMN].isna().any():
        raise ValueError("Target column contains missing values")
    if df.drop(columns=[TARGET_COLUMN]).empty:
        raise ValueError("Dataset must contain feature columns")
