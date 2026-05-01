"""Project paths and constants."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "credit_g.csv"
SAMPLE_DATA_PATH = DATA_DIR / "sample" / "credit_sample.csv"
MODEL_DIR = ROOT / "artifacts" / "models"
MODEL_PATH = MODEL_DIR / "credit_risk_model.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"
MLFLOW_DIR = ROOT / "mlruns"
MLFLOW_DB_PATH = ROOT / "artifacts" / "mlflow" / "mlflow.db"
MLFLOW_EXPERIMENT_NAME = "credit-risk-mlops"
REPORT_PATH = ROOT / "reports" / "model_report.md"
PREDICTION_LOG_DIR = ROOT / "prediction_logs"
TARGET_COLUMN = "class"
POSITIVE_LABEL = "bad"
