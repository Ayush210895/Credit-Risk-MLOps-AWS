FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    MODEL_PATH=/app/artifacts/models/approved/credit_risk_model.joblib

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY artifacts ./artifacts

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "credit_risk_mlops.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
