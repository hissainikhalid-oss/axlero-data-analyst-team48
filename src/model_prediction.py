import pandas as pd
import joblib

MODEL_PATH = "models/xgboost_model.pkl"


def load_model():
    """Load the trained XGBoost model."""
    return joblib.load(MODEL_PATH)


def predict_risk(input_data):
    """
    Predict risk classification for prepared input data.

    input_data must contain the same feature columns
    used during model training.
    """

    model = load_model()

    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    prediction = model.predict(input_data)

    return int(prediction[0])


if __name__ == "__main__":
    print("Model Prediction Module Ready!")
    print("This module can be used by the FastAPI backend.")