from typing import List
from fastapi import APIRouter
from app.schemas.optimization import (
    OptimizationSimulationRequest,
    OptimizationSimulationResponse,
    TransportModeProfile,
)
from app.services import optimization_service

router = APIRouter(
    prefix="/api/v1/optimization",
    tags=["Route & Schedule Optimization"],
)

@router.post(
    "/simulate",
    response_model=OptimizationSimulationResponse,
    status_code=200,
)
def simulate_route_optimization(
    request: OptimizationSimulationRequest,
):
    return optimization_service.run_route_optimization(request)

@router.get(
    "/modes",
    response_model=List[TransportModeProfile],
)
def get_transport_modes():
    return optimization_service.get_transport_modes()
