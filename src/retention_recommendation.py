"""
=========================================================
AI CUSTOMER CHURN PREDICTION SYSTEM
Retention Recommendation System
=========================================================
"""

import os
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

print("=" * 70)
print("RETENTION RECOMMENDATION SYSTEM")
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
# Prepare Features
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

probability = model.predict_proba(X_scaled)[:, 1]

df["ChurnProbability"] = probability

# =====================================================
# Risk Category
# =====================================================

def risk(prob):

    if prob < 0.30:
        return "Low"

    elif prob < 0.70:
        return "Medium"

    return "High"

df["RiskCategory"] = df["ChurnProbability"].apply(risk)

# =====================================================
# Recommendation Function
# =====================================================

def recommendation(row):

    if row["RiskCategory"] == "High":

        return (
            "Immediate follow-up by customer support, "
            "offer 20% discount, assign dedicated account manager."
        )

    elif row["RiskCategory"] == "Medium":

        return (
            "Provide loyalty rewards, personalized offers, "
            "and proactive engagement."
        )

    else:

        return (
            "Maintain regular communication and "
            "offer premium services."
        )

df["RetentionRecommendation"] = df.apply(

    recommendation,

    axis=1

)

# =====================================================
# AI Business Recommendation
# =====================================================

def business_advice(prob):

    if prob >= 0.80:

        return "Critical Customer - Immediate retention campaign."

    elif prob >= 0.60:

        return "High Risk - Personalized offers recommended."

    elif prob >= 0.40:

        return "Moderate Risk - Increase engagement."

    else:

        return "Healthy Customer - Upsell premium services."

df["BusinessRecommendation"] = df["ChurnProbability"].apply(

    business_advice

)

# =====================================================
# Save Report
# =====================================================

report = df[[
    "CustomerID",
    "ChurnProbability",
    "RiskCategory",
    "RetentionRecommendation",
    "BusinessRecommendation"
]]

report.to_csv(

    "reports/retention_recommendations.csv",

    index=False

)

# =====================================================
# Summary
# =====================================================

print("\nRisk Category Distribution\n")

print(report["RiskCategory"].value_counts())

print("\nTop 10 Customers\n")

print(report.head(10))

print("\n")
print("=" * 70)
print("FILES CREATED")
print("=" * 70)

print("✓ reports/retention_recommendations.csv")

print("\nRetention Recommendation Completed Successfully")