from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from app.database import SessionLocal
from app.schemas.reports import CSVUploadResponse
from app.services import report_service

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["CSV Upload & Export"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/upload-csv",
    response_model=CSVUploadResponse,
    status_code=200,
)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    contents = await file.read()
    return report_service.process_csv_upload(db=db, file_content=contents)

@router.get("/export-csv")
def export_csv(
    db: Session = Depends(get_db),
):
    csv_data = report_service.generate_predictions_csv(db=db)
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=predictions_report.csv"},
    )
