import os
import sys
from typing import List

# Ensure project root is in sys.path so optimization module can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from optimization.optimizer import optimize_shipment_route, TRANSPORT_MODES
from app.schemas.optimization import (
    OptimizationSimulationRequest,
    OptimizationSimulationResponse,
    RouteOption,
    TransportModeProfile,
)

def run_route_optimization(
    request: OptimizationSimulationRequest
) -> OptimizationSimulationResponse:
    res = optimize_shipment_route(
        distance=request.distance,
        weather=request.weather,
        traffic=request.traffic,
        current_vehicle=request.vehicle_type,
        urgency_level=request.urgency_level or "Medium",
    )

    all_opts = [
        RouteOption(
            transport_mode=o["transport_mode"],
            estimated_hours=o["estimated_hours"],
            estimated_cost=o["estimated_cost"],
            risk_score=o["risk_score"],
            is_current=o["is_current"],
        )
        for o in res["all_options"]
    ]

    if res["optimal_mode"] == res["original_mode"]:
        summary = (
            f"Current mode '{res['original_mode']}' is already optimal for route "
            f"{request.origin} → {request.destination} under {request.weather} weather."
        )
    else:
        summary = (
            f"Switching from '{res['original_mode']}' to '{res['optimal_mode']}' "
            f"reduces delay risk by {res['risk_reduction_percentage']}% and saves "
            f"{res['time_saved_hours']} hours (cost impact: {'+' if res['cost_impact'] > 0 else ''}${res['cost_impact']:.2f})."
        )

    return OptimizationSimulationResponse(
        original_mode=res["original_mode"],
        original_hours=res["original_hours"],
        original_cost=res["original_cost"],
        original_risk=res["original_risk"],
        optimal_mode=res["optimal_mode"],
        optimal_hours=res["optimal_hours"],
        optimal_cost=res["optimal_cost"],
        optimal_risk=res["optimal_risk"],
        time_saved_hours=res["time_saved_hours"],
        cost_impact=res["cost_impact"],
        risk_reduction_percentage=res["risk_reduction_percentage"],
        recommendation_summary=summary,
        all_options=all_opts,
    )

def get_transport_modes() -> List[TransportModeProfile]:
    return [
        TransportModeProfile(
            mode=mode,
            speed_kmh=profile["speed_kmh"],
            cost_per_km=profile["cost_per_km"],
            base_risk=profile["base_risk"],
        )
        for mode, profile in TRANSPORT_MODES.items()
    ]
