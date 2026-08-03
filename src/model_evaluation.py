import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# =====================================================
# Step 1: Load Saved Model
# =====================================================

model = joblib.load("models/xgboost_model.pkl")

print("Saved Model Loaded Successfully!")

# =====================================================
# Step 2: Load Test Data
# =====================================================

X_test = pd.read_csv("data/processed/X_test.csv")
y_test = pd.read_csv("data/processed/y_test.csv").squeeze()

print("\nTesting Data Loaded Successfully!")
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)

# =====================================================
# Step 3: Make Predictions
# =====================================================

y_pred = model.predict(X_test)

print("\nPredictions Generated Successfully!")

# =====================================================
# Step 4: Evaluate Model
# =====================================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted"
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted"
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted"
)

print("\n==============================")
print("Model Evaluation")
print("==============================")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# =====================================================
# Step 5: Feature Importance
# =====================================================

feature_importance = pd.DataFrame({
    "Feature": X_test.columns,
    "Importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 10 Most Important Features:")
print(feature_importance.head(10))

# Save feature importance
feature_importance.to_csv(
    "data/processed/feature_importance.csv",
    index=False
)

print("\nFeature Importance Saved Successfully!")

# Plot Top 10 Features

plt.figure(figsize=(10,6))

plt.barh(
    feature_importance["Feature"].head(10),
    feature_importance["Importance"].head(10)
)

plt.gca().invert_yaxis()

plt.title("Top 10 Feature Importance")
plt.xlabel("Importance Score")
plt.ylabel("Features")

plt.tight_layout()
plt.show()