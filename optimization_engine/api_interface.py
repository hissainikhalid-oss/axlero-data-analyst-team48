"""
api_interface.py

This module defines the exact input/output contract for Member-3's
FastAPI backend to call your optimization engine. Member-3 should
import `get_recommendation` and call it from a POST endpoint, e.g.:

    from optimization_engine.api_interface import get_recommendation

    @app.post("/recommend")
    def recommend(request: RecommendationRequest):
        return get_recommendation(
            predicted_delay_days=request.predicted_delay_days,
            budget_limit=request.budget_limit,
            max_acceptable_delay_days=request.max_acceptable_delay_days,
            base_order_value=request.base_order_value,
        )

The function returns a plain JSON-serializable dict, ready to be
returned directly as a FastAPI response.
"""

from optimization_engine import recommend_options


def get_recommendation(predicted_delay_days: int,
                        budget_limit: float = 20000,
                        max_acceptable_delay_days: int = 10,
                        base_order_value: float = 100000) -> dict:
    """
    Public entry point for the backend. Wraps recommend_options()
    and returns a clean, JSON-safe dictionary.

    Input (from Member-1's ML model / dashboard form):
        predicted_delay_days: int
        budget_limit: float
        max_acceptable_delay_days: int
        base_order_value: float

    Output (for Member-3's dashboard UI):
        {
            "status": "Optimal" | "Infeasible",
            "recommended_option": "A" | "B" | "C" | None,
            "options": {
                "A": {"name": ..., "cost": ..., "delay_days": ..., "description": ...},
                "B": {...},
                "C": {...}
            }
        }
    """
    result = recommend_options(
        predicted_delay_days=predicted_delay_days,
        budget_limit=budget_limit,
        max_acceptable_delay_days=max_acceptable_delay_days,
        base_order_value=base_order_value,
    )

    # Ensure everything is a plain JSON-serializable type (no numpy types, etc.)
    return {
        "status": result["status"],
        "recommended_option": result["recommended_option"],
        "predicted_delay_days": result["predicted_delay_days"],
        "budget_limit": result["budget_limit"],
        "max_acceptable_delay_days": result["max_acceptable_delay_days"],
        "options": {
            key: {
                "name": opt["name"],
                "cost": float(opt["cost"]),
                "delay_days": int(opt["delay_days"]),
                "description": opt["description"],
            }
            for key, opt in result["options"].items()
        },
    }


if __name__ == "__main__":
    import json
    output = get_recommendation(predicted_delay_days=14, max_acceptable_delay_days=5)
    print(json.dumps(output, indent=2))
