"""API schemas."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CreditApplication(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
                "foreign_worker": "yes",
            }
        }
    )

    checking_status: str
    duration: int
    credit_history: str
    purpose: str
    credit_amount: int
    savings_status: str
    employment: str
    installment_commitment: int
    personal_status: str
    other_parties: str
    residence_since: int
    property_magnitude: str
    age: int
    other_payment_plans: str
    housing: str
    existing_credits: int
    job: str
    num_dependents: int
    own_telephone: str
    foreign_worker: str


class PredictionResponse(BaseModel):
    default_probability: float
    risk_band: str
    decision: str
