"""FastAPI inference service for credit default risk."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import os
from typing import Any

from fastapi import FastAPI

from credit_risk_mlops.api.schemas import CreditApplication, PredictionResponse
from credit_risk_mlops.config.settings import MODEL_PATH
from credit_risk_mlops.models.predict import load_model, predict_default_probability


MODEL: Any | None = None


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    global MODEL
    model_path = os.environ.get("MODEL_PATH", str(MODEL_PATH))
    MODEL = load_model(model_path)
    yield


app = FastAPI(title="Credit Risk MLOps API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(application: CreditApplication) -> PredictionResponse:
    if MODEL is None:
        raise RuntimeError("Model artifact has not been loaded")
    probability = predict_default_probability(MODEL, application.model_dump())
    return PredictionResponse(
        default_probability=probability,
        risk_band=risk_band(probability),
        decision="review" if probability >= 0.35 else "approve",
    )


def risk_band(probability: float) -> str:
    if probability >= 0.65:
        return "high"
    if probability >= 0.35:
        return "medium"
    return "low"
