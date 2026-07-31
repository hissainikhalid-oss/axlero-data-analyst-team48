from typing import List, Dict, Any

TRANSPORT_MODES = {
    "Truck": {"speed_kmh": 60, "cost_per_km": 1.5, "base_risk": 0.10},
    "Express Truck": {"speed_kmh": 80, "cost_per_km": 2.2, "base_risk": 0.05},
    "Container": {"speed_kmh": 45, "cost_per_km": 1.1, "base_risk": 0.20},
    "Air Freight": {"speed_kmh": 500, "cost_per_km": 8.0, "base_risk": 0.02},
    "Rail Logistics": {"speed_kmh": 50, "cost_per_km": 0.9, "base_risk": 0.15},
}

WEATHER_IMPACT = {
    "Clear": 1.0,
    "Rain": 1.25,
    "Fog": 1.4,
    "Storm": 1.8,
}

TRAFFIC_IMPACT = {
    "Low": 1.0,
    "Medium": 1.2,
    "High": 1.6,
}

def optimize_shipment_route(
    distance: float,
    weather: str,
    traffic: str,
    current_vehicle: str,
    urgency_level: str = "Medium",
) -> Dict[str, Any]:
    w_factor = WEATHER_IMPACT.get(weather.title(), 1.1)
    t_factor = TRAFFIC_IMPACT.get(traffic.title(), 1.1)

    route_options: List[Dict[str, Any]] = []

    for mode, profile in TRANSPORT_MODES.items():
        adjusted_speed = profile["speed_kmh"] / (w_factor * t_factor)
        estimated_hours = round(distance / adjusted_speed, 2)
        total_cost = round(distance * profile["cost_per_km"], 2)
        mode_risk = round(min(profile["base_risk"] * w_factor * t_factor, 0.99), 4)

        route_options.append({
            "transport_mode": mode,
            "estimated_hours": estimated_hours,
            "estimated_cost": total_cost,
            "risk_score": mode_risk,
            "is_current": mode.lower() in current_vehicle.lower() or current_vehicle.lower() in mode.lower()
        })

    current_option = next((o for o in route_options if o["is_current"]), route_options[0])

    if urgency_level.lower() == "high":
        best_option = min(route_options, key=lambda x: (x["estimated_hours"], x["risk_score"]))
    elif urgency_level.lower() == "cost_sensitive":
        best_option = min(route_options, key=lambda x: (x["estimated_cost"], x["risk_score"]))
    else:
        best_option = min(route_options, key=lambda x: (x["risk_score"] * 0.5 + (x["estimated_hours"] / 100) * 0.5))

    time_saved = round(max(current_option["estimated_hours"] - best_option["estimated_hours"], 0.0), 2)
    cost_diff = round(best_option["estimated_cost"] - current_option["estimated_cost"], 2)
    risk_reduction = round(max((current_option["risk_score"] - best_option["risk_score"]) * 100, 0.0), 2)

    return {
        "original_mode": current_vehicle,
        "original_hours": current_option["estimated_hours"],
        "original_cost": current_option["estimated_cost"],
        "original_risk": current_option["risk_score"],
        "optimal_mode": best_option["transport_mode"],
        "optimal_hours": best_option["estimated_hours"],
        "optimal_cost": best_option["estimated_cost"],
        "optimal_risk": best_option["risk_score"],
        "time_saved_hours": time_saved,
        "cost_impact": cost_diff,
        "risk_reduction_percentage": risk_reduction,
        "all_options": sorted(route_options, key=lambda x: x["risk_score"])
    }
