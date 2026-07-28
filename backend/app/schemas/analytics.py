from typing import List, Dict
from pydantic import BaseModel
from app.schemas.shipment_prediction import ShipmentPredictionCreate, ShipmentPredictionResponse

class BatchShipmentPredictionCreate(BaseModel):
    shipments: List[ShipmentPredictionCreate]

class BatchShipmentPredictionResponse(BaseModel):
    total_processed: int
    delayed_count: int
    on_time_count: int
    predictions: List[ShipmentPredictionResponse]

class AnalyticsSummaryResponse(BaseModel):
    total_shipments: int
    delayed_count: int
    on_time_count: int
    delay_rate_percentage: float
    average_delay_probability: float
    high_risk_count: int

class RiskBreakdownItem(BaseModel):
    label: str
    total_count: int
    delayed_count: int
    delay_rate_percentage: float

class AnalyticsBreakdownResponse(BaseModel):
    weather: List[RiskBreakdownItem]
    traffic: List[RiskBreakdownItem]
    vehicle_type: List[RiskBreakdownItem]
