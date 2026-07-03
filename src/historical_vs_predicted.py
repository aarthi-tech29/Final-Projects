"""
=========================================================
AI CUSTOMER CHURN PREDICTION SYSTEM
Historical vs Predicted Churn Trend
=========================================================
"""

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

print("=" * 70)
print("HISTORICAL VS PREDICTED CHURN")
print("=" * 70)

os.makedirs("reports", exist_ok=True)

# =====================================================
# Load Dataset
# =====================================================

df = pd.read_csv("data/customer_churn_featured.csv")

# =====================================================
# Encode Categorical Columns
# =====================================================

for col in df.select_dtypes(include="object").columns:

    if col == "CustomerID":
        continue

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col])

# =====================================================
# Features
# =====================================================

X = df.drop(["CustomerID", "Churn"], axis=1)

feature_columns = joblib.load("models/feature_columns.pkl")

X = X[feature_columns]

scaler = joblib.load("models/scaler.pkl")

X_scaled = scaler.transform(X)

# =====================================================
# Load Best Model
# =====================================================

model = joblib.load("models/best_model.pkl")

predicted_probability = model.predict_proba(X_scaled)[:,1]

predicted_churn = (predicted_probability >= 0.5).astype(int)

# =====================================================
# Historical Churn
# =====================================================

historical = df["Churn"].value_counts()

predicted = pd.Series(predicted_churn).value_counts()

comparison = pd.DataFrame({

    "Historical":[

        historical.get(0,0),

        historical.get(1,0)

    ],

    "Predicted":[

        predicted.get(0,0),

        predicted.get(1,0)

    ]

},

index=[

    "No Churn",

    "Churn"

])

print("\nComparison\n")

print(comparison)

# =====================================================
# Save CSV
# =====================================================

comparison.to_csv(

    "reports/historical_vs_predicted.csv"

)

# =====================================================
# Plot
# =====================================================

comparison.plot(

    kind="bar",

    figsize=(8,6)

)

plt.title("Historical vs Predicted Churn")

plt.ylabel("Customers")

plt.tight_layout()

plt.savefig(

    "reports/historical_vs_predicted.png"

)

plt.close()

# =====================================================
# Summary
# =====================================================

print("\n")
print("=" * 70)
print("FILES CREATED")
print("=" * 70)

print("✓ reports/historical_vs_predicted.csv")

print("✓ reports/historical_vs_predicted.png")

print("\nHistorical Trend Analysis Completed Successfully")