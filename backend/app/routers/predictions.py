from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.shipment_prediction import (
    ShipmentPredictionCreate,
    ShipmentPredictionResponse,
)
from app.services import prediction_service

router = APIRouter(
    prefix="/api/v1/predictions",
    tags=["Shipment Predictions"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    response_model=ShipmentPredictionResponse,
    status_code=201,
)
def create_prediction(
    data: ShipmentPredictionCreate,
    db: Session = Depends(get_db),
):
    return prediction_service.create_prediction(db=db, data=data)

@router.get(
    "/",
    response_model=list[ShipmentPredictionResponse],
)
def list_predictions(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return prediction_service.get_all_predictions(db=db, skip=skip, limit=limit)

@router.get(
    "/{prediction_id}",
    response_model=ShipmentPredictionResponse,
)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    prediction = prediction_service.get_prediction_by_id(db=db, prediction_id=prediction_id)
    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail=f"Prediction with id {prediction_id} not found",
        )
    return prediction

@router.get(
    "/shipment/{shipment_id}",
    response_model=ShipmentPredictionResponse,
)
def get_prediction_by_shipment_id(
    shipment_id: str,
    db: Session = Depends(get_db),
):
    prediction = prediction_service.get_prediction_by_shipment_id(db=db, shipment_id=shipment_id)
    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail=f"Prediction with shipment_id '{shipment_id}' not found",
        )
    return prediction
