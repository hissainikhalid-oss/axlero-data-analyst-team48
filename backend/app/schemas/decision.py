from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DecisionCreate(BaseModel):
    shipment_id: str

    original_mode: str
    selected_mode: str

    original_cost: float
    selected_cost: float

    original_hours: float
    selected_hours: float

    original_risk: float
    selected_risk: float


class DecisionEvaluationCreate(BaseModel):
    actual_cost: float
    actual_hours: float


class DecisionResponse(DecisionCreate):
    id: int

    decision_status: str

    actual_cost: Optional[float] = None
    actual_hours: Optional[float] = None
    actual_outcome: Optional[str] = None

    created_at: Optional[datetime] = None
    evaluated_at: Optional[datetime] = None

class DecisionAnalyticsResponse(BaseModel):
    total_decisions: int
    executed_decisions: int
    evaluated_decisions: int

    better_outcomes: int
    worse_outcomes: int
    mixed_outcomes: int

    average_expected_cost: float
    average_actual_cost: float
    total_cost_variance: float

    average_expected_hours: float
    average_actual_hours: float
    total_hours_variance: float    