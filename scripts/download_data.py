#!/usr/bin/env python3
"""Download the OpenML credit-g dataset."""

from __future__ import annotations

from sklearn.datasets import fetch_openml

from credit_risk_mlops.config.settings import RAW_DATA_PATH


def main() -> None:
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset = fetch_openml(data_id=31, as_frame=True)
    df = dataset.frame
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f"Wrote {RAW_DATA_PATH} with {len(df)} rows")


if __name__ == "__main__":
    main()
