"""
=========================================================
AI CUSTOMER CHURN PREDICTION SYSTEM
Feature Engineering
=========================================================
"""

import pandas as pd


def load_data():

    print("=" * 60)
    print("Loading Dataset...")
    print("=" * 60)

    df = pd.read_csv("data/customer_churn_dataset.csv")

    return df


def create_features(df):

    print("\nCreating New Features...")

    # Average Monthly Spend
    df["AvgMonthlySpend"] = (
        df["TotalCharges"] /
        (df["Tenure"] + 1)
    )

    # Complaint Ratio
    df["ComplaintRatio"] = (
        df["Complaints"] /
        (df["SupportTickets"] + 1)
    )

    # Loyalty Score
    df["LoyaltyScore"] = (
        df["Tenure"] *
        df["SatisfactionScore"]
    )

    # Engagement Score
    df["EngagementScore"] = (
        df["UsageHours"] +
        df["LoginFrequency"] +
        df["AvgSessionTime"]
    )

    # Payment Risk
    df["PaymentRisk"] = (
        df["LatePayments"] *
        df["MonthlyCharges"]
    )

    # High Value Customer
    df["HighValueCustomer"] = (
        df["CustomerLifetimeValue"] > 8000
    ).astype(int)

    # Usage Category
    df["UsageCategory"] = pd.cut(
        df["UsageHours"],
        bins=[0,80,180,400],
        labels=[
            "Low",
            "Medium",
            "High"
        ]
    )

    # Tenure Group
    df["TenureGroup"] = pd.cut(
        df["Tenure"],
        bins=[0,12,36,72],
        labels=[
            "New",
            "Regular",
            "Loyal"
        ]
    )

    # Service Engagement
    df["ServiceEngagement"] = (
        df["StreamingTV"].map({"Yes":1,"No":0}) +
        df["StreamingMovies"].map({"Yes":1,"No":0}) +
        df["OnlineBackup"].map({"Yes":1,"No":0}) +
        df["OnlineSecurity"].map({"Yes":1,"No":0}) +
        df["DeviceProtection"].map({"Yes":1,"No":0}) +
        df["TechSupport"].map({"Yes":1,"No":0})
    )

    # Customer Health Score
    df["CustomerHealthScore"] = (
        df["SatisfactionScore"] * 2 +
        df["UsageHours"] * 0.2 -
        df["Complaints"] * 3 -
        df["LatePayments"] * 2
    )

    return df


def save_dataset(df):

    df.to_csv(
        "data/customer_churn_featured.csv",
        index=False
    )

    print("\nFeature Engineered Dataset Saved")


def main():

    df = load_data()

    df = create_features(df)

    print("\nNew Dataset Shape :", df.shape)

    print("\nNew Columns Added")

    print(df.columns.tolist())

    save_dataset(df)

    print("\nFeature Engineering Completed Successfully")


if __name__ == "__main__":
    main()