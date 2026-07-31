import uuid
from typing import Optional
from sqlalchemy.orm import Session

from app.models.shipment_prediction import ShipmentPrediction
from app.schemas.shipment_prediction import ShipmentPredictionCreate
from app.services import ml_service

WEATHER_RISK = {
    "clear": 0.0,
    "rain": 0.4,
    "fog": 0.5,
    "storm": 0.9,
}

TRAFFIC_RISK = {
    "low": 0.0,
    "medium": 0.3,
    "high": 0.7,
}

VEHICLE_RISK = {
    "truck": 0.1,
    "lorry": 0.2,
    "container": 0.3,
    "trailer": 0.4,
}

def _calculate_delay_probability(data: ShipmentPredictionCreate) -> float:
    distance_risk = min(data.distance / 3000.0, 1.0) * 0.4
    weather_risk = WEATHER_RISK.get(data.weather.lower(), 0.1)
    traffic_risk = TRAFFIC_RISK.get(data.traffic.lower(), 0.1)
    vehicle_risk = VEHICLE_RISK.get(data.vehicle_type.lower(), 0.1)

    probability = (
        0.25 * distance_risk
        + 0.30 * weather_risk
        + 0.30 * traffic_risk
        + 0.15 * vehicle_risk
    )
    return round(min(max(probability, 0.0), 1.0), 4)

def predict_delay_and_probability(data: ShipmentPredictionCreate):
    ml_result = ml_service.predict_with_model(
        distance=data.distance,
        weather=data.weather,
        traffic=data.traffic,
        vehicle_type=data.vehicle_type,
    )

    if ml_result is not None:
        prediction, probability = ml_result
    else:
        probability = _calculate_delay_probability(data)
        prediction = "Delayed" if probability >= 0.5 else "On Time"

    return prediction, probability

def _get_recommendation(
    prediction: str, probability: float, data: ShipmentPredictionCreate
) -> str:
    if prediction == "On Time":
        return (
            f"Shipment from {data.origin} to {data.destination} is expected to "
            f"arrive on time (confidence: {(1 - probability) * 100:.1f}%). "
            f"No action needed. Continue monitoring weather conditions."
        )

    suggestions = []
    if data.weather.lower() in ("storm", "fog"):
        suggestions.append(
            f"Weather is '{data.weather}' — consider delaying dispatch until "
            f"conditions improve or choose an alternate route"
        )
    if data.traffic.lower() == "high":
        suggestions.append(
            "Traffic is high — schedule dispatch during off-peak hours "
            "(early morning or late night)"
        )
    if data.distance > 1500:
        suggestions.append(
            f"Long-haul route ({data.distance:.0f} km) — set up an intermediate "
            f"staging warehouse to split the journey"
        )
    if data.vehicle_type.lower() in ("container", "trailer"):
        suggestions.append(
            f"Vehicle type '{data.vehicle_type}' is slower — consider a faster "
            f"vehicle type like Truck for time-sensitive shipments"
        )
    if not suggestions:
        suggestions.append("Review route and consider alternative logistics options")

    return (
        f"⚠️ HIGH DELAY RISK ({probability * 100:.1f}%) for shipment "
        f"{data.origin} → {data.destination}. Recommendations: "
        + "; ".join(suggestions)
        + "."
    )

def create_prediction(
    db: Session, data: ShipmentPredictionCreate
) -> ShipmentPrediction:
    shipment_id = f"SHP-{uuid.uuid4().hex[:8].upper()}"
    prediction, probability = predict_delay_and_probability(data)
    recommendation = _get_recommendation(prediction, probability, data)

    db_prediction = ShipmentPrediction(
        shipment_id=shipment_id,
        origin=data.origin,
        destination=data.destination,
        distance=data.distance,
        weather=data.weather,
        traffic=data.traffic,
        vehicle_type=data.vehicle_type,
        prediction=prediction,
        probability=probability,
        recommendation=recommendation,
    )

    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

def get_all_predictions(
    db: Session, skip: int = 0, limit: int = 100
) -> list[ShipmentPrediction]:
    return (
        db.query(ShipmentPrediction)
        .order_by(ShipmentPrediction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_prediction_by_id(
    db: Session, prediction_id: int
) -> Optional[ShipmentPrediction]:
    return (
        db.query(ShipmentPrediction)
        .filter(ShipmentPrediction.id == prediction_id)
        .first()
    )

def get_prediction_by_shipment_id(
    db: Session, shipment_id: str
) -> Optional[ShipmentPrediction]:
    return (
        db.query(ShipmentPrediction)
        .filter(ShipmentPrediction.shipment_id == shipment_id)
        .first()
    )
