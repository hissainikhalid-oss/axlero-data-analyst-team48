import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def train_and_save_model():
    np.random.seed(42)
    n_samples = 1000

    distances = np.random.uniform(50, 3000, n_samples)
    weathers = np.random.choice(["Clear", "Rain", "Fog", "Storm"], n_samples, p=[0.4, 0.3, 0.15, 0.15])
    traffics = np.random.choice(["Low", "Medium", "High"], n_samples, p=[0.4, 0.35, 0.25])
    vehicles = np.random.choice(["Truck", "Lorry", "Container", "Trailer"], n_samples, p=[0.35, 0.3, 0.2, 0.15])

    weather_weights = {"Clear": 0.0, "Rain": 0.3, "Fog": 0.5, "Storm": 0.8}
    traffic_weights = {"Low": 0.0, "Medium": 0.3, "High": 0.7}
    vehicle_weights = {"Truck": 0.1, "Lorry": 0.2, "Container": 0.3, "Trailer": 0.4}

    probs = []
    for d, w, t, v in zip(distances, weathers, traffics, vehicles):
        p = 0.25 * (d / 3000.0 * 0.4) + 0.30 * weather_weights[w] + 0.30 * traffic_weights[t] + 0.15 * vehicle_weights[v]
        probs.append(p)

    labels = [1 if p >= 0.45 else 0 for p in probs]

    df = pd.DataFrame({
        "distance": distances,
        "weather": weathers,
        "traffic": traffics,
        "vehicle_type": vehicles,
        "delayed": labels
    })

    X = df[["distance", "weather", "traffic", "vehicle_type"]]
    y = df["delayed"]

    categorical_features = ["weather", "traffic", "vehicle_type"]
    numeric_features = ["distance"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features)
        ]
    )

    model_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    model_pipeline.fit(X, y)

    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "delay_model.joblib")
    joblib.dump(model_pipeline, model_path)
    print(f"Model successfully trained and saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
