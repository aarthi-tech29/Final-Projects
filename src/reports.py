"""
=========================================================
AI CUSTOMER CHURN PREDICTION SYSTEM
Executive Reports & Analytics
=========================================================
"""

import os
import pandas as pd

print("=" * 70)
print("EXECUTIVE REPORT GENERATION")
print("=" * 70)

os.makedirs("reports", exist_ok=True)

# =====================================================
# Load Reports
# =====================================================

model_report = pd.read_csv("reports/model_comparison.csv")

feature_report = pd.read_csv("reports/feature_importance.csv")

retention_report = pd.read_csv("reports/retention_recommendations.csv")

segment_report = pd.read_csv("reports/customer_segments.csv")

ltv_report = pd.read_csv("reports/lifetime_value_predictions.csv")

trend_report = pd.read_csv("reports/historical_vs_predicted.csv")

# =====================================================
# Executive KPI Summary
# =====================================================

total_customers = len(retention_report)

high_risk = (retention_report["RiskCategory"] == "High").sum()

medium_risk = (retention_report["RiskCategory"] == "Medium").sum()

low_risk = (retention_report["RiskCategory"] == "Low").sum()

best_model = model_report.iloc[0]["Model"]

best_accuracy = model_report.iloc[0]["Accuracy"]

top_feature = feature_report.iloc[0]["Feature"]

avg_actual_ltv = ltv_report["Actual Lifetime Value"].mean()

avg_predicted_ltv = ltv_report["Predicted Lifetime Value"].mean()

total_segments = segment_report["SegmentName"].nunique()

# =====================================================
# Executive Summary
# =====================================================

summary = pd.DataFrame({

    "Metric":[

        "Total Customers",

        "High Risk Customers",

        "Medium Risk Customers",

        "Low Risk Customers",

        "Best Model",

        "Best Accuracy",

        "Top Churn Factor",

        "Average Actual LTV",

        "Average Predicted LTV",

        "Customer Segments"

    ],

    "Value":[

        total_customers,

        high_risk,

        medium_risk,

        low_risk,

        best_model,

        round(best_accuracy,4),

        top_feature,

        round(avg_actual_ltv,2),

        round(avg_predicted_ltv,2),

        total_segments

    ]

})

summary.to_csv(

    "reports/executive_summary.csv",

    index=False

)

# =====================================================
# Management Insights
# =====================================================

insights = []

if high_risk > total_customers * 0.30:

    insights.append(
        "High customer churn risk detected. Immediate retention campaigns recommended."
    )

else:

    insights.append(
        "Customer churn is under acceptable limits."
    )

insights.append(
    f"Best predictive model: {best_model} "
    f"(Accuracy: {best_accuracy:.2%})"
)

insights.append(
    f"Most influential churn factor: {top_feature}"
)

insights.append(
    "Focus marketing efforts on high-risk customer segments."
)

insights.append(
    "Provide personalized offers to medium-risk customers."
)

insights.append(
    "Upsell premium plans to low-risk customers."
)

insights_df = pd.DataFrame({

    "Management Insights": insights

})

insights_df.to_csv(

    "reports/management_insights.csv",

    index=False

)

# =====================================================
# Display Results
# =====================================================

print("\nEXECUTIVE SUMMARY\n")

print(summary)

print("\nMANAGEMENT INSIGHTS\n")

for i, text in enumerate(insights, start=1):

    print(f"{i}. {text}")

print("\n")
print("=" * 70)
print("FILES GENERATED")
print("=" * 70)

print("✓ reports/executive_summary.csv")

print("✓ reports/management_insights.csv")

print("\nExecutive Reporting Completed Successfully.")