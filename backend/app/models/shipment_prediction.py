from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.database import Base


class ShipmentPrediction(Base):
    __tablename__ = "shipment_predictions"

    id = Column(Integer, primary_key=True, index=True)

    shipment_id = Column(String, unique=True, nullable=False)

    origin = Column(String, nullable=False)

    destination = Column(String, nullable=False)

    distance = Column(Float, nullable=False)

    weather = Column(String, nullable=False)

    traffic = Column(String, nullable=False)

    vehicle_type = Column(String, nullable=False)

    prediction = Column(String)

    probability = Column(Float)

    recommendation = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())