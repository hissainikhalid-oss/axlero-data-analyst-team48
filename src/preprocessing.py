import pandas as pd
from sklearn.preprocessing import LabelEncoder

# =====================================================
# Step 1: Load Raw Dataset
# =====================================================

df = pd.read_csv("data/raw/dynamic_supply_chain_logistics_dataset_with_country.csv")

print("Dataset Loaded Successfully!")
print("Dataset Shape:", df.shape)

# =====================================================
# Step 2: Remove Unnecessary Columns
# =====================================================

df = df.drop(columns=["product_id", "supplier_id"])

print("\nRemaining Columns:")
print(df.columns)

# =====================================================
# Step 3: Check Missing Values
# =====================================================

print("\nMissing Values:")
print(df.isnull().sum())

# =====================================================
# Step 4: Encode Target Variable
# =====================================================

label_encoder = LabelEncoder()

df["risk_classification"] = label_encoder.fit_transform(
    df["risk_classification"]
)

print("\nRisk Classification Mapping:")

for original, encoded in zip(
    label_encoder.classes_,
    label_encoder.transform(label_encoder.classes_)
):
    print(f"{original} --> {encoded}")

# =====================================================
# Step 5: Dataset Information
# =====================================================

print("\nDataset Information:")
print(df.info())

print("\nDataset Shape After Preprocessing:")
print(df.shape)

# =====================================================
# Step 6: Save Cleaned Dataset
# =====================================================

df.to_csv(
    "data/processed/cleaned_supply_chain.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")
print("Location: data/processed/cleaned_supply_chain.csv")