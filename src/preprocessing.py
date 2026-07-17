import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("data/dynamic_supply_chain_logistics_dataset_with_country.csv")

print("Dataset Loaded Successfully!")
print(df.shape)

# Remove unnecessary columns
df = df.drop(columns=["product_id", "supplier_id"])

print("\nRemaining Columns:")
print(df.columns)

# Save cleaned dataset
df.to_csv(
    "data/processed/cleaned_supply_chain.csv",
    index=False
)

print("Cleaned dataset saved successfully!")