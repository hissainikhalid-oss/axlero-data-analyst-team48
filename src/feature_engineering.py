import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_supply_chain.csv")

print("Cleaned Dataset Loaded")
print(df.shape)

# Check data types
print(df.info())

# Handle categorical columns
categorical_columns = df.select_dtypes(include="str").columns

encoder = LabelEncoder()

for col in categorical_columns:
    df[col] = encoder.fit_transform(df[col])

print("\nAfter Encoding:")
print(df.head())

# Save feature engineered dataset
df.to_csv(
    "data/processed/feature_engineered_supply_chain.csv",
    index=False
)

print("Feature Engineering Completed!")