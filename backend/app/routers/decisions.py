from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.decision import (
    DecisionCreate,
    DecisionEvaluationCreate,
    DecisionResponse,
    DecisionAnalyticsResponse,
)
from app.services import decision_service


router = APIRouter(
    prefix="/api/v1/decisions",
    tags=["Operational Decisions"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/execute",
    response_model=DecisionResponse,
    status_code=201,
)
def execute_decision(
    data: DecisionCreate,
    db: Session = Depends(get_db),
):
    return decision_service.execute_decision(
        db=db,
        data=data,
    )

@router.post(
    "/{decision_id}/evaluate",
    response_model=DecisionResponse,
    status_code=200,
)
def evaluate_decision(
    decision_id: int,
    data: DecisionEvaluationCreate,
    db: Session = Depends(get_db),
):
    try:
        return decision_service.evaluate_decision(
            db=db,
            decision_id=decision_id,
            actual_cost=data.actual_cost,
            actual_hours=data.actual_hours,
        )
    except ValueError as exc:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

@router.get(
    "/analytics",
    response_model=DecisionAnalyticsResponse,
)
def get_decision_analytics(
    db: Session = Depends(get_db),
):
    return decision_service.get_decision_analytics(db)

@router.get(
    "",
    response_model=List[DecisionResponse],
)
def get_decisions(
    db: Session = Depends(get_db),
):
    return decision_service.get_all_decisions(db)