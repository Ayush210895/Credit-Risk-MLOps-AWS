"""Simple data drift checks for numeric features."""

from __future__ import annotations

import pandas as pd


def numeric_drift_report(reference: pd.DataFrame, current: pd.DataFrame, threshold: float = 0.2) -> pd.DataFrame:
    rows = []
    numeric_columns = reference.select_dtypes(include=["number"]).columns
    for column in numeric_columns:
        ref_mean = float(reference[column].mean())
        cur_mean = float(current[column].mean())
        ref_std = float(reference[column].std()) or 1.0
        shift = abs(cur_mean - ref_mean) / ref_std
        rows.append(
            {
                "feature": column,
                "reference_mean": ref_mean,
                "current_mean": cur_mean,
                "standardized_shift": shift,
                "drift_flag": shift >= threshold,
            }
        )
    return pd.DataFrame(rows)
