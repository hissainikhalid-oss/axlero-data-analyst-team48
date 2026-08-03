import os
import joblib
import pandas as pd
from typing import Tuple, Dict, Any, Optional

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "models", "delay_model.joblib")

_model: Optional[Any] = None
_model_status: Dict[str, Any] = {
    "loaded": False,
    "model_type": None,
    "features": ["distance", "weather", "traffic", "vehicle_type"],
    "model_path": MODEL_PATH,
    "error": None
}

def load_ml_model() -> bool:
    global _model, _model_status
    abs_path = os.path.abspath(MODEL_PATH)
    if os.path.exists(abs_path):
        try:
            _model = joblib.load(abs_path)
            _model_status["loaded"] = True
            _model_status["model_type"] = type(_model.named_steps["classifier"]).__name__ if hasattr(_model, "named_steps") else type(_model).__name__
            _model_status["error"] = None
            return True
        except Exception as e:
            _model_status["loaded"] = False
            _model_status["error"] = str(e)
            return False
    else:
        _model_status["loaded"] = False
        _model_status["error"] = f"Model artifact not found at {abs_path}"
        return False

load_ml_model()

def predict_with_model(
    distance: float, weather: str, traffic: str, vehicle_type: str
) -> Optional[Tuple[str, float]]:
    global _model
    if _model is None:
        if not load_ml_model():
            return None

    try:
        input_df = pd.DataFrame([{
            "distance": float(distance),
            "weather": str(weather).title(),
            "traffic": str(traffic).title(),
            "vehicle_type": str(vehicle_type).title()
        }])
        probabilities = _model.predict_proba(input_df)[0]
        delay_probability = round(float(probabilities[1]), 4)
        prediction = "Delayed" if delay_probability >= 0.5 else "On Time"
        return prediction, delay_probability
    except Exception as e:
        print(f"ML Model inference error: {e}")
        return None

def get_model_info() -> Dict[str, Any]:
    return _model_status

def reload_model() -> Dict[str, Any]:
    success = load_ml_model()
    return {
        "success": success,
        "model_status": _model_status
    }
