# Credit Risk MLOps AWS

Production-style credit-risk machine learning project built in phases. Phase 1 runs locally with a reproducible training script, FastAPI inference service, Docker, tests, CI, and a basic monitoring report. Phase 2 adds AWS deployment and monitoring.

## Why This Project

Credit risk is a strong finance ML use case because it connects model quality with operational controls: data access, model versioning, deployment, monitoring, and governance. This repo is designed to show that lifecycle, not just a notebook.

## Current Capabilities

| Area | Included |
| --- | --- |
| Data | OpenML `credit-g` download script plus offline sample CSV |
| Modeling | Logistic regression and random forest pipelines |
| Features | Numeric scaling, categorical one-hot encoding, missing-value handling |
| Evaluation | ROC AUC, average precision, precision, recall, F1 |
| Experiment tracking | MLflow runs with params, metrics, model artifact, and report artifact |
| Model registry | Candidate registration plus metric-gated approval for serving |
| Serving | FastAPI `/health` and `/predict` endpoints |
| Packaging | Dockerfile and docker-compose |
| CI | GitHub Actions tests, compile check, Docker build |
| Monitoring | Numeric drift report scaffold |
| AWS path | No-cost guarded AWS readiness docs and manual ECR workflow |

## Data Source

The full dataset is OpenML `credit-g`, dataset ID `31`, originally from UCI/Statlog German Credit. It classifies applicants as good or bad credit risks.

- OpenML docs note that datasets can be retrieved by name or ID.
- The `credit-g` dataset can be retrieved as `get_dataset("credit-g")` or ID `31`.

Sources: [OpenML intro](https://docs.openml.org/intro/), [OpenML credit-g listing](https://www.openml.org/d/31).

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Train on bundled sample data
PYTHONPATH=src python scripts/train_model.py

# Approve the candidate model for serving
PYTHONPATH=src python scripts/promote_model.py

# Run tests
PYTHONPATH=src python -m pytest -q

# Start API
PYTHONPATH=src uvicorn credit_risk_mlops.api.main:app --reload
```

## MLflow Tracking

Training logs an MLflow run by default to local SQLite metadata under `artifacts/mlflow/`.

```bash
PYTHONPATH=src python scripts/train_model.py
PYTHONPATH=src mlflow ui --backend-store-uri sqlite:///artifacts/mlflow/mlflow.db
```

Then open `http://127.0.0.1:5000` to compare runs, metrics, parameters, and artifacts.

Useful options:

```bash
# Train a different baseline and log it to the same experiment
PYTHONPATH=src python scripts/train_model.py --model-type random_forest

# Use a remote tracking server later
PYTHONPATH=src python scripts/train_model.py --tracking-uri http://localhost:5000

# Skip tracking for quick debugging
PYTHONPATH=src python scripts/train_model.py --no-mlflow
```

## Model Approval Gate

Training registers a candidate model. The API serves the approved model artifact from `artifacts/models/approved/`.

```bash
PYTHONPATH=src python scripts/train_model.py
PYTHONPATH=src python scripts/promote_model.py --min-roc-auc 0.70 --min-average-precision 0.50
PYTHONPATH=src uvicorn credit_risk_mlops.api.main:app --reload
```

The promotion step writes registry metadata to `artifacts/registry/` and blocks candidates that miss the approval thresholds.

Test the API:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "checking_status": "no checking",
    "duration": 24,
    "credit_history": "existing paid",
    "purpose": "radio/tv",
    "credit_amount": 2500,
    "savings_status": "<100",
    "employment": "1<=X<4",
    "installment_commitment": 3,
    "personal_status": "male single",
    "other_parties": "none",
    "residence_since": 2,
    "property_magnitude": "real estate",
    "age": 35,
    "other_payment_plans": "none",
    "housing": "own",
    "existing_credits": 1,
    "job": "skilled",
    "num_dependents": 1,
    "own_telephone": "none",
    "foreign_worker": "yes"
  }'
```

## Download Full Dataset

```bash
PYTHONPATH=src python scripts/download_data.py
PYTHONPATH=src python scripts/train_model.py --data data/raw/credit_g.csv
PYTHONPATH=src python scripts/promote_model.py
```

`data/raw/` is ignored so large/raw data does not get committed.

## Docker

Train once so the model artifact exists locally:

```bash
PYTHONPATH=src python scripts/train_model.py
PYTHONPATH=src python scripts/promote_model.py
docker build -t credit-risk-mlops-aws .
docker run -p 8000:8000 credit-risk-mlops-aws
```

Or:

```bash
docker compose up --build
```

## AWS No-Cost Mode

AWS deployment is intentionally disabled by default. The manual workflow `.github/workflows/aws-ecr-manual.yml` runs a local dry run without AWS authentication or resource creation. The ECR publish job is skipped unless `enable_aws_push=true` and `cost_confirmation=I_UNDERSTAND_AWS_COSTS`.

Read these before enabling anything in AWS:

- `docs/aws/no_cost_guardrails.md`
- `docs/aws/iam_policy_templates.md`

## Project Structure

```text
.
|-- src/credit_risk_mlops/
|   |-- api/
|   |-- config/
|   |-- data/
|   |-- features/
|   |-- models/
|   `-- monitoring/
|-- scripts/
|-- tests/
|-- data/sample/
|-- artifacts/models/
|-- reports/
|-- docs/aws/
|-- docs/mlops/
|-- Dockerfile
|-- docker-compose.yml
`-- .github/workflows/ci.yml
```

## Roadmap

1. Push inference image to Amazon ECR.
2. Deploy FastAPI container to ECS Fargate or SageMaker.
3. Add CloudWatch dashboards and alarms.
4. Add scheduled drift monitoring and retraining trigger.
5. Add AWS-hosted MLflow backend with RDS/S3.
