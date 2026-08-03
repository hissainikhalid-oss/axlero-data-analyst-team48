import pandas as pd

# =====================================================
# Step 1: Load Cleaned Dataset
# =====================================================

df = pd.read_csv("data/processed/cleaned_supply_chain.csv")

print("Cleaned Dataset Loaded")
print("Dataset Shape:", df.shape)

# =====================================================
# Step 2: Create New Features
# =====================================================

# Feature 1: Inventory Coverage
# Indicates how much inventory is available compared to demand.
df["inventory_coverage"] = (
    df["warehouse_inventory_level"] /
    (df["historical_demand"] + 1)
)

# Feature 2: Supplier Efficiency
# Higher reliability and lower lead time give better efficiency.
df["supplier_efficiency"] = (
    df["supplier_reliability_score"] /
    (df["lead_time_days"] + 1)
)

# Feature 3: Logistics Risk
# Combines shipping cost with route risk.
df["logistics_risk"] = (
    df["shipping_costs"] *
    df["route_risk_level"]
)

# Feature 4: Delay Impact
# Measures the expected impact of delivery delays.
df["delay_impact"] = (
    df["delay_probability"] *
    df["delivery_time_deviation"]
)

# =====================================================
# Step 3: Display New Features
# =====================================================

print("\nNew Feature Columns Added:")
print(df[[
    "inventory_coverage",
    "supplier_efficiency",
    "logistics_risk",
    "delay_impact"
]].head())

print("\nUpdated Dataset Shape:")
print(df.shape)

print("\nCurrent Columns:")
print(df.columns.tolist())

# =====================================================
# Step 4: Summary Statistics of New Features
# =====================================================

print("\nSummary Statistics of Engineered Features:")
print(df[[
    "inventory_coverage",
    "supplier_efficiency",
    "logistics_risk",
    "delay_impact"
]].describe())

# =====================================================
# Step 5: Check Duplicate Rows
# =====================================================

print("\nDuplicate Rows:", df.duplicated().sum())

# =====================================================
# Step 6: Check Missing Values in New Features
# =====================================================

print("\nMissing Values in New Features:")
print(df[[
    "inventory_coverage",
    "supplier_efficiency",
    "logistics_risk",
    "delay_impact"
]].isnull().sum())

# =====================================================
# Step 6: Save Feature Engineered Dataset
# =====================================================

df.to_csv(
    "data/processed/feature_engineered_supply_chain.csv",
    index=False
)

print("\nFeature Engineering Completed Successfully!")
print("Feature engineered dataset saved to:")
print("data/processed/feature_engineered_supply_chain.csv")