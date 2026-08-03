from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ShipmentPredictionCreate(BaseModel):
    origin: str = Field(..., min_length=1, max_length=100)
    destination: str = Field(..., min_length=1, max_length=100)
    distance: float = Field(..., gt=0)
    weather: str = Field(..., min_length=1, max_length=50)
    traffic: str = Field(..., min_length=1, max_length=50)
    vehicle_type: str = Field(..., min_length=1, max_length=50)

class ShipmentPredictionResponse(BaseModel):
    id: int
    shipment_id: str
    origin: str
    destination: str
    distance: float
    weather: str
    traffic: str
    vehicle_type: str
    prediction: Optional[str] = None
    probability: Optional[float] = None
    recommendation: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
