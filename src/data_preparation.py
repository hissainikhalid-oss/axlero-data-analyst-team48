import pandas as pd
from sklearn.model_selection import train_test_split

# =====================================================
# Step 1: Load Feature Engineered Dataset
# =====================================================

df = pd.read_csv("data/processed/feature_engineered_supply_chain.csv")

print("Feature Engineered Dataset Loaded Successfully!")
print("Dataset Shape:", df.shape)

# =====================================================
# Step 2: One-Hot Encode supplier_country
# =====================================================

df = pd.get_dummies(
    df,
    columns=["supplier_country"],
    dtype=int
)

print("\nDataset Shape After One-Hot Encoding:")
print(df.shape)

# =====================================================
# Step 3: Separate Features and Target
# =====================================================

X = df.drop(columns=["risk_classification"])
y = df["risk_classification"]

print("\nFeatures Shape:", X.shape)
print("Target Shape:", y.shape)

# =====================================================
# Step 4: Split Dataset into Training and Testing Sets
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Set Shape")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

print("\nTesting Set Shape")
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)

# =====================================================
# Step 5: Save Prepared Datasets
# =====================================================

X_train.to_csv(
    "data/processed/X_train.csv",
    index=False
)

X_test.to_csv(
    "data/processed/X_test.csv",
    index=False
)

y_train.to_csv(
    "data/processed/y_train.csv",
    index=False
)

y_test.to_csv(
    "data/processed/y_test.csv",
    index=False
)

print("\nPrepared Datasets Saved Successfully!")

print("\nSaved Files:")
print("- X_train.csv")
print("- X_test.csv")
print("- y_train.csv")
print("- y_test.csv")