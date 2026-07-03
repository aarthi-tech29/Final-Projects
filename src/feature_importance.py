"""
=========================================================
AI CUSTOMER CHURN PREDICTION SYSTEM
Feature Importance Analysis
=========================================================
"""

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

print("=" * 70)
print("FEATURE IMPORTANCE ANALYSIS")
print("=" * 70)

# =====================================================
# Create Reports Folder
# =====================================================

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
# Prepare Features
# =====================================================

X = df.drop(["CustomerID", "Churn"], axis=1)

# =====================================================
# Load Tuned Random Forest Model
# =====================================================

model = joblib.load("models/random_forest_tuned.pkl")

# =====================================================
# Feature Importance
# =====================================================

importance = model.feature_importances_

feature_importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance": importance

})

feature_importance = feature_importance.sort_values(

    by="Importance",

    ascending=False

)

print("\nTop 20 Important Features\n")

print(feature_importance.head(20))

# =====================================================
# Save CSV
# =====================================================

feature_importance.to_csv(

    "reports/feature_importance.csv",

    index=False

)

# =====================================================
# Plot
# =====================================================

plt.figure(figsize=(12,8))

top15 = feature_importance.head(15)

plt.barh(

    top15["Feature"],

    top15["Importance"]

)

plt.gca().invert_yaxis()

plt.xlabel("Importance Score")

plt.ylabel("Features")

plt.title("Top 15 Churn Influencing Features")

plt.tight_layout()

plt.savefig(

    "reports/feature_importance.png"

)

plt.close()

# =====================================================
# Display Top Features
# =====================================================

print("\n")
print("=" * 70)
print("TOP 10 CHURN FACTORS")
print("=" * 70)

for index, row in feature_importance.head(10).iterrows():

    print(

        f"{row['Feature']} : {row['Importance']:.4f}"

    )

print("\n")
print("=" * 70)
print("FILES GENERATED")
print("=" * 70)

print("✓ reports/feature_importance.csv")

print("✓ reports/feature_importance.png")

print("\nFeature Importance Completed Successfully")