from fastapi import APIRouter
from app.services import ml_service

router = APIRouter(
    prefix="/api/v1/model",
    tags=["ML Model Management"],
)

@router.get("/info")
def get_model_info():
    return ml_service.get_model_info()

@router.post("/reload")
def reload_model():
    return ml_service.reload_model()
