from datetime import datetime
from sqlalchemy.orm import Session

from app.models.decision import Decision
from app.schemas.decision import DecisionCreate


def execute_decision(
    db: Session,
    data: DecisionCreate,
) -> Decision:

    decision = Decision(
        shipment_id=data.shipment_id,

        original_mode=data.original_mode,
        selected_mode=data.selected_mode,

        original_cost=data.original_cost,
        selected_cost=data.selected_cost,

        original_hours=data.original_hours,
        selected_hours=data.selected_hours,

        original_risk=data.original_risk,
        selected_risk=data.selected_risk,

        decision_status="Executed",
        created_at=datetime.utcnow(),
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return decision


def evaluate_decision(
    db: Session,
    decision_id: int,
    actual_cost: float,
    actual_hours: float,
) -> Decision:

    decision = (
        db.query(Decision)
        .filter(Decision.id == decision_id)
        .first()
    )

    if decision is None:
        raise ValueError(f"Decision {decision_id} not found")

    decision.actual_cost = actual_cost
    decision.actual_hours = actual_hours

    cost_difference = actual_cost - decision.selected_cost
    time_difference = actual_hours - decision.selected_hours

    if cost_difference <= 0 and time_difference <= 0:
        decision.actual_outcome = "Better than expected"
    elif cost_difference > 0 and time_difference > 0:
        decision.actual_outcome = "Worse than expected"
    else:
        decision.actual_outcome = "Mixed outcome"

    decision.decision_status = "Evaluated"
    decision.evaluated_at = datetime.utcnow()

    db.commit()
    db.refresh(decision)

    return decision


def get_all_decisions(db: Session):
    return (
        db.query(Decision)
        .order_by(Decision.created_at.desc())
        .all()
    )

def get_decision_analytics(db: Session):
    decisions = db.query(Decision).all()

    total_decisions = len(decisions)

    executed_decisions = sum(
        1 for d in decisions
        if d.decision_status == "Executed"
    )

    evaluated_decisions = sum(
        1 for d in decisions
        if d.decision_status == "Evaluated"
    )

    better_outcomes = sum(
        1 for d in decisions
        if d.actual_outcome == "Better than expected"
    )

    worse_outcomes = sum(
        1 for d in decisions
        if d.actual_outcome == "Worse than expected"
    )

    mixed_outcomes = sum(
        1 for d in decisions
        if d.actual_outcome == "Mixed outcome"
    )

    evaluated = [
        d for d in decisions
        if d.actual_cost is not None
        and d.actual_hours is not None
    ]

    if evaluated:
        average_expected_cost = sum(
            d.selected_cost for d in evaluated
        ) / len(evaluated)

        average_actual_cost = sum(
            d.actual_cost for d in evaluated
        ) / len(evaluated)

        total_cost_variance = sum(
            d.actual_cost - d.selected_cost
            for d in evaluated
        )

        average_expected_hours = sum(
            d.selected_hours for d in evaluated
        ) / len(evaluated)

        average_actual_hours = sum(
            d.actual_hours for d in evaluated
        ) / len(evaluated)

        total_hours_variance = sum(
            d.actual_hours - d.selected_hours
            for d in evaluated
        )
    else:
        average_expected_cost = 0.0
        average_actual_cost = 0.0
        total_cost_variance = 0.0

        average_expected_hours = 0.0
        average_actual_hours = 0.0
        total_hours_variance = 0.0

    return {
        "total_decisions": total_decisions,
        "executed_decisions": executed_decisions,
        "evaluated_decisions": evaluated_decisions,

        "better_outcomes": better_outcomes,
        "worse_outcomes": worse_outcomes,
        "mixed_outcomes": mixed_outcomes,

        "average_expected_cost": round(average_expected_cost, 2),
        "average_actual_cost": round(average_actual_cost, 2),
        "total_cost_variance": round(total_cost_variance, 2),

        "average_expected_hours": round(average_expected_hours, 2),
        "average_actual_hours": round(average_actual_hours, 2),
        "total_hours_variance": round(total_hours_variance, 2),
    }