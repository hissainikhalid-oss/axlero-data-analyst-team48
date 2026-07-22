import os
import joblib
import pandas as pd
from xgboost import XGBClassifier

# =====================================================
# Step 1: Load Training Data
# =====================================================

X_train = pd.read_csv("data/processed/X_train.csv")
y_train = pd.read_csv("data/processed/y_train.csv").squeeze()

print("Training Data Loaded Successfully!")

print("\nTraining Data Shape:")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

# =====================================================
# Step 2: Create XGBoost Model
# =====================================================

model = XGBClassifier(
    objective="multi:softmax",
    num_class=3,
    random_state=42,
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1
)

print("\nXGBoost Model Created Successfully!")

# =====================================================
# Step 3: Train Model
# =====================================================

print("\nTraining the model...")

model.fit(X_train, y_train)

print("Model Training Completed Successfully!")

# =====================================================
# Step 4: Save Model
# =====================================================

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/xgboost_model.pkl")

print("\nModel Saved Successfully!")
print("Location: models/xgboost_model.pkl")