import csv
import io
import uuid
from typing import Tuple
from sqlalchemy.orm import Session

from app.models.shipment_prediction import ShipmentPrediction
from app.schemas.shipment_prediction import ShipmentPredictionCreate
from app.schemas.reports import CSVUploadResponse
from app.services.prediction_service import predict_delay_and_probability, _get_recommendation

def process_csv_upload(db: Session, file_content: bytes) -> CSVUploadResponse:
    text_data = file_content.decode("utf-8-sig")
    csv_reader = csv.DictReader(io.StringIO(text_data))

    db_objects = []
    errors = []
    row_count = 0
    success_count = 0

    for idx, row in enumerate(csv_reader, start=1):
        row_count += 1
        try:
            normalized_row = {k.strip().lower(): str(v).strip() for k, v in row.items() if k}
            
            origin = normalized_row.get("origin")
            destination = normalized_row.get("destination")
            distance_str = normalized_row.get("distance")
            weather = normalized_row.get("weather")
            traffic = normalized_row.get("traffic")
            vehicle_type = normalized_row.get("vehicle_type") or normalized_row.get("vehicle")

            if not all([origin, destination, distance_str, weather, traffic, vehicle_type]):
                errors.append({"row": idx, "error": "Missing required fields in CSV row"})
                continue

            distance = float(distance_str)
            if distance <= 0:
                errors.append({"row": idx, "error": "Distance must be greater than 0"})
                continue

            create_schema = ShipmentPredictionCreate(
                origin=origin,
                destination=destination,
                distance=distance,
                weather=weather,
                traffic=traffic,
                vehicle_type=vehicle_type
            )

            shipment_id = f"SHP-{uuid.uuid4().hex[:8].upper()}"
            prediction, probability = predict_delay_and_probability(create_schema)
            recommendation = _get_recommendation(prediction, probability, create_schema)

            db_obj = ShipmentPrediction(
                shipment_id=shipment_id,
                origin=origin,
                destination=destination,
                distance=distance,
                weather=weather,
                traffic=traffic,
                vehicle_type=vehicle_type,
                prediction=prediction,
                probability=probability,
                recommendation=recommendation
            )
            db_objects.append(db_obj)
            success_count += 1

        except Exception as e:
            errors.append({"row": idx, "error": str(e)})

    if db_objects:
        db.add_all(db_objects)
        db.commit()

    return CSVUploadResponse(
        total_rows=row_count,
        successful_predictions=success_count,
        failed_rows=len(errors),
        errors=errors
    )

def generate_predictions_csv(db: Session) -> str:
    predictions = db.query(ShipmentPrediction).order_by(ShipmentPrediction.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID", "Shipment ID", "Origin", "Destination", "Distance (km)",
        "Weather", "Traffic", "Vehicle Type", "Prediction",
        "Probability", "Recommendation", "Created At"
    ])

    for p in predictions:
        writer.writerow([
            p.id, p.shipment_id, p.origin, p.destination, p.distance,
            p.weather, p.traffic, p.vehicle_type, p.prediction,
            p.probability, p.recommendation, str(p.created_at)
        ])

    return output.getvalue()
