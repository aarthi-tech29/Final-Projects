"""
=========================================================
AI CUSTOMER CHURN PREDICTION SYSTEM
Customer Segmentation
=========================================================
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

print("=" * 70)
print("CUSTOMER SEGMENTATION")
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
# Features for Segmentation
# =====================================================

features = [

    "Tenure",

    "MonthlyCharges",

    "CustomerLifetimeValue",

    "UsageHours",

    "SatisfactionScore"

]

X = df[features]

# =====================================================
# Scale Data
# =====================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# =====================================================
# KMeans Clustering
# =====================================================

kmeans = KMeans(

    n_clusters=4,

    random_state=42,

    n_init=10

)

df["CustomerSegment"] = kmeans.fit_predict(X_scaled)

# =====================================================
# Segment Names
# =====================================================

segment_names = {

    0: "Premium Customers",

    1: "Loyal Customers",

    2: "At Risk Customers",

    3: "New Customers"

}

df["SegmentName"] = df["CustomerSegment"].map(segment_names)

# =====================================================
# Save Dataset
# =====================================================

df.to_csv(

    "reports/customer_segments.csv",

    index=False

)

# =====================================================
# Segment Summary
# =====================================================

summary = df.groupby("SegmentName")[

    [

        "MonthlyCharges",

        "CustomerLifetimeValue",

        "SatisfactionScore",

        "Tenure"

    ]

].mean()

summary.to_csv(

    "reports/customer_segment_summary.csv"

)

print("\nSegment Summary\n")

print(summary)

# =====================================================
# Visualization
# =====================================================

counts = df["SegmentName"].value_counts()

plt.figure(figsize=(8,6))

plt.bar(

    counts.index,

    counts.values

)

plt.title("Customer Segments")

plt.xlabel("Segment")

plt.ylabel("Number of Customers")

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(

    "reports/customer_segments.png"

)

plt.close()

# =====================================================
# Executive Insights
# =====================================================

print("\n")
print("=" * 70)
print("EXECUTIVE INSIGHTS")
print("=" * 70)

largest = counts.idxmax()

print("Largest Segment :", largest)

print("Total Customers :", len(df))

print("Total Segments :", len(counts))

print("\nSegment Distribution")

print(counts)

print("\n")
print("=" * 70)
print("FILES CREATED")
print("=" * 70)

print("✓ reports/customer_segments.csv")

print("✓ reports/customer_segment_summary.csv")

print("✓ reports/customer_segments.png")

print("\nCustomer Segmentation Completed Successfully")