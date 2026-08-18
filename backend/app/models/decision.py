from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)

    shipment_id = Column(String, nullable=False, index=True)

    original_mode = Column(String, nullable=False)
    selected_mode = Column(String, nullable=False)

    original_cost = Column(Float, nullable=False)
    selected_cost = Column(Float, nullable=False)

    original_hours = Column(Float, nullable=False)
    selected_hours = Column(Float, nullable=False)

    original_risk = Column(Float, nullable=False)
    selected_risk = Column(Float, nullable=False)

    decision_status = Column(
        String,
        default="Executed",
        nullable=False
    )

    actual_cost = Column(Float, nullable=True)
    actual_hours = Column(Float, nullable=True)
    actual_outcome = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    evaluated_at = Column(DateTime, nullable=True)