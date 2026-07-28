import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.models.shipment_prediction import ShipmentPrediction
from app.schemas.analytics import (
    BatchShipmentPredictionCreate,
    BatchShipmentPredictionResponse,
    AnalyticsSummaryResponse,
    AnalyticsBreakdownResponse,
    RiskBreakdownItem,
)
from app.services.prediction_service import (
    _calculate_delay_probability,
    _get_recommendation,
)

def create_batch_predictions(
    db: Session, batch_data: BatchShipmentPredictionCreate
) -> BatchShipmentPredictionResponse:
    db_objects = []
    delayed_count = 0
    on_time_count = 0

    for item in batch_data.shipments:
        shipment_id = f"SHP-{uuid.uuid4().hex[:8].upper()}"
        probability = _calculate_delay_probability(item)
        prediction = "Delayed" if probability >= 0.5 else "On Time"
        recommendation = _get_recommendation(prediction, probability, item)

        if prediction == "Delayed":
            delayed_count += 1
        else:
            on_time_count += 1

        db_prediction = ShipmentPrediction(
            shipment_id=shipment_id,
            origin=item.origin,
            destination=item.destination,
            distance=item.distance,
            weather=item.weather,
            traffic=item.traffic,
            vehicle_type=item.vehicle_type,
            prediction=prediction,
            probability=probability,
            recommendation=recommendation,
        )
        db_objects.append(db_prediction)

    db.add_all(db_objects)
    db.commit()

    for obj in db_objects:
        db.refresh(obj)

    return BatchShipmentPredictionResponse(
        total_processed=len(db_objects),
        delayed_count=delayed_count,
        on_time_count=on_time_count,
        predictions=db_objects,
    )

def get_analytics_summary(db: Session) -> AnalyticsSummaryResponse:
    total_shipments = db.query(func.count(ShipmentPrediction.id)).scalar() or 0

    if total_shipments == 0:
        return AnalyticsSummaryResponse(
            total_shipments=0,
            delayed_count=0,
            on_time_count=0,
            delay_rate_percentage=0.0,
            average_delay_probability=0.0,
            high_risk_count=0,
        )

    delayed_count = db.query(func.count(ShipmentPrediction.id)).filter(
        ShipmentPrediction.prediction == "Delayed"
    ).scalar() or 0

    on_time_count = total_shipments - delayed_count

    avg_prob = db.query(func.avg(ShipmentPrediction.probability)).scalar() or 0.0

    high_risk_count = db.query(func.count(ShipmentPrediction.id)).filter(
        ShipmentPrediction.probability >= 0.7
    ).scalar() or 0

    delay_rate = round((delayed_count / total_shipments) * 100, 2)

    return AnalyticsSummaryResponse(
        total_shipments=total_shipments,
        delayed_count=delayed_count,
        on_time_count=on_time_count,
        delay_rate_percentage=delay_rate,
        average_delay_probability=round(float(avg_prob), 4),
        high_risk_count=high_risk_count,
    )

def _get_group_breakdown(db: Session, column_attr) -> list[RiskBreakdownItem]:
    results = (
        db.query(
            column_attr.label("category"),
            func.count(ShipmentPrediction.id).label("total"),
            func.sum(
                case((ShipmentPrediction.prediction == "Delayed", 1), else_=0)
            ).label("delayed"),
        )
        .group_by(column_attr)
        .all()
    )

    breakdown_items = []
    for category, total, delayed in results:
        delayed = delayed or 0
        rate = round((delayed / total) * 100, 2) if total > 0 else 0.0
        breakdown_items.append(
            RiskBreakdownItem(
                label=str(category),
                total_count=total,
                delayed_count=delayed,
                delay_rate_percentage=rate,
            )
        )
    return breakdown_items

def get_analytics_breakdown(db: Session) -> AnalyticsBreakdownResponse:
    weather_items = _get_group_breakdown(db, ShipmentPrediction.weather)
    traffic_items = _get_group_breakdown(db, ShipmentPrediction.traffic)
    vehicle_items = _get_group_breakdown(db, ShipmentPrediction.vehicle_type)

    return AnalyticsBreakdownResponse(
        weather=weather_items,
        traffic=traffic_items,
        vehicle_type=vehicle_items,
    )
