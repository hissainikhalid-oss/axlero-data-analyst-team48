from typing import List, Optional
from pydantic import BaseModel, Field

class RouteOption(BaseModel):
    transport_mode: str
    estimated_hours: float
    estimated_cost: float
    risk_score: float
    is_current: bool

class OptimizationSimulationRequest(BaseModel):
    origin: str = Field(..., example="Mumbai")
    destination: str = Field(..., example="Delhi")
    distance: float = Field(..., gt=0, example=1400.0)
    weather: str = Field(..., example="Storm")
    traffic: str = Field(..., example="High")
    vehicle_type: str = Field(..., example="Container")
    urgency_level: Optional[str] = Field(default="Medium", example="High")

class OptimizationSimulationResponse(BaseModel):
    original_mode: str
    original_hours: float
    original_cost: float
    original_risk: float
    optimal_mode: str
    optimal_hours: float
    optimal_cost: float
    optimal_risk: float
    time_saved_hours: float
    cost_impact: float
    risk_reduction_percentage: float
    recommendation_summary: str
    all_options: List[RouteOption]

class TransportModeProfile(BaseModel):
    mode: str
    speed_kmh: float
    cost_per_km: float
    base_risk: float
