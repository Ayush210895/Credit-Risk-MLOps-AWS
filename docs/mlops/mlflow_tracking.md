# MLflow Experiment Tracking

This project uses MLflow to track each model training run.

## What Gets Logged

| Category | Examples |
| --- | --- |
| Parameters | data path, model type, feature count, positive label |
| Metrics | ROC AUC, average precision, precision, recall, F1, row counts |
| Artifacts | trained model joblib, metrics JSON, model report markdown |
| Tags | project name, stage, model type |

## Local Backend

The default local backend is SQLite:

```bash
PYTHONPATH=src python scripts/train_model.py
PYTHONPATH=src mlflow ui --backend-store-uri sqlite:///artifacts/mlflow/mlflow.db
```

SQLite is used instead of a file-based tracking store so the local setup is closer to a real metadata store.

## Production Direction

For AWS deployment, the tracking layout should evolve to:

| Component | Local | AWS Target |
| --- | --- | --- |
| Metadata store | SQLite | RDS PostgreSQL |
| Artifact store | Local artifacts | S3 |
| Tracking UI/API | Local MLflow UI | ECS or SageMaker-hosted MLflow server |
| Model approval | Manual review | Registry stage or metadata gate |

The model registry layer in `docs/mlops/model_registry.md` uses this run metadata as part of the approval history.
