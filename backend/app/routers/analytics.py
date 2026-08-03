from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.analytics import (
    BatchShipmentPredictionCreate,
    BatchShipmentPredictionResponse,
    AnalyticsSummaryResponse,
    AnalyticsBreakdownResponse,
)
from app.services import analytics_service

router = APIRouter(
    prefix="/api/v1",
    tags=["Batch & Analytics"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/predictions/batch",
    response_model=BatchShipmentPredictionResponse,
    status_code=201,
)
def create_batch_predictions(
    batch_data: BatchShipmentPredictionCreate,
    db: Session = Depends(get_db),
):
    return analytics_service.create_batch_predictions(db=db, batch_data=batch_data)

@router.get(
    "/analytics/summary",
    response_model=AnalyticsSummaryResponse,
)
def get_analytics_summary(
    db: Session = Depends(get_db),
):
    return analytics_service.get_analytics_summary(db=db)

@router.get(
    "/analytics/breakdown",
    response_model=AnalyticsBreakdownResponse,
)
def get_analytics_breakdown(
    db: Session = Depends(get_db),
):
    return analytics_service.get_analytics_breakdown(db=db)
