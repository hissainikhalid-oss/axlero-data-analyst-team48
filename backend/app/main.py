from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.predictions import router as predictions_router
from app.routers.analytics import router as analytics_router
from app.routers.model import router as model_router
from app.routers.optimization import router as optimization_router
from app.routers.reports import router as reports_router
from app.models.shipment_prediction import ShipmentPrediction  # noqa: F401
from app.models.decision import Decision  # noqa: F401
from app.routers.decisions import router as decisions_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SupplyPrescript API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predictions_router)
app.include_router(analytics_router)
app.include_router(model_router)
app.include_router(optimization_router)
app.include_router(reports_router)
app.include_router(decisions_router)

@app.get("/")
def home():
    return {
        "status": "healthy",
        "message": "SupplyPrescript Backend is Running!",
    }