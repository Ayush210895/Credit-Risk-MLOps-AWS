# Model Registry and Approval Gate

Training creates a candidate model. Serving uses only an approved model artifact.

## Workflow

```bash
PYTHONPATH=src python scripts/train_model.py
PYTHONPATH=src python scripts/promote_model.py --min-roc-auc 0.70 --min-average-precision 0.50
PYTHONPATH=src uvicorn credit_risk_mlops.api.main:app --reload
```

## Registry Files

| File | Purpose |
| --- | --- |
| `artifacts/registry/model_registry.json` | Full model history with candidate, approved, and archived statuses |
| `artifacts/registry/approved_model.json` | Metadata for the model currently allowed to serve |
| `artifacts/models/approved/credit_risk_model.joblib` | Approved serving artifact |

These generated files are intentionally ignored by Git. The repository stores the code and documentation; each environment creates and approves its own artifacts.

## Approval Rules

The promotion script blocks models that do not meet minimum metric thresholds:

```bash
PYTHONPATH=src python scripts/promote_model.py \
  --min-roc-auc 0.75 \
  --min-average-precision 0.55
```

This is deliberately lightweight. It mirrors the operational pattern used in larger systems: trained model, evaluation checks, approval metadata, then serving.
