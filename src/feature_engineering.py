import pandas as pd
import numpy as np
import os


OUTPUT_FOLDER = "cleaned_data"


def feature_engineering(customer_df, purchase_df):
    """
    ============================================================
          Enterprise Customer Feature Engineering
    ============================================================

    Features Created
    ----------------
    1. Orders
    2. TotalPurchase
    3. LastPurchase
    4. AgeGroup
    5. PurchaseFrequency
    6. Customer Lifetime Value (CLV)
    7. LoyalCustomer
    8. PurchaseCategory

    ============================================================
    """

    print("\n" + "=" * 65)
    print("            FEATURE ENGINEERING STARTED")
    print("=" * 65)

    # ---------------------------------------------------------
    # Merge Customer Dataset with Purchase Dataset
    # ---------------------------------------------------------

    df = pd.merge(
        customer_df,
        purchase_df,
        on="CustomerID",
        how="left"
    )

    # ---------------------------------------------------------
    # Handle Missing Purchase Data
    # ---------------------------------------------------------

    df["Orders"] = df["Orders"].fillna(0).astype(int)

    df["TotalPurchase"] = df["TotalPurchase"].fillna(0)

    df["LastPurchase"] = df["LastPurchase"].fillna("Not Available")

    # ---------------------------------------------------------
    # Feature 1 : Age Group
    # ---------------------------------------------------------

    df["AgeGroup"] = np.select(
        [
            df["Age"] < 25,
            (df["Age"] >= 25) & (df["Age"] < 40),
            df["Age"] >= 40
        ],
        [
            "Young",
            "Adult",
            "Senior"
        ],
        default="Unknown"
    )

    # ---------------------------------------------------------
    # Feature 2 : Purchase Frequency
    # ---------------------------------------------------------

    df["PurchaseFrequency"] = np.round(
        df["Orders"] / 12,
        2
    )

    # ---------------------------------------------------------
    # Feature 3 : Customer Lifetime Value
    # ---------------------------------------------------------

    df["CLV"] = np.round(
        df["Orders"] * df["TotalPurchase"],
        2
    )

    # ---------------------------------------------------------
    # Feature 4 : Loyal Customer
    # ---------------------------------------------------------

    df["LoyalCustomer"] = np.where(
        df["Orders"] >= 10,
        "Yes",
        "No"
    )

    # ---------------------------------------------------------
    # Feature 5 : Purchase Category
    # ---------------------------------------------------------

    df["PurchaseCategory"] = np.select(
        [
            df["TotalPurchase"] >= 5000,
            (df["TotalPurchase"] >= 2000) &
            (df["TotalPurchase"] < 5000)
        ],
        [
            "High Value",
            "Medium Value"
        ],
        default="Low Value"
    )

    # ---------------------------------------------------------
    # Save Feature Engineered Dataset
    # ---------------------------------------------------------

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    output_file = os.path.join(
        OUTPUT_FOLDER,
        "customer_features.csv"
    )

    df.to_csv(output_file, index=False)

    # ---------------------------------------------------------
    # Display Summary
    # ---------------------------------------------------------

    print("\n✓ Customer Dataset Merged Successfully")

    print("✓ Feature Engineering Completed")

    print("\n" + "-" * 60)

    print("Feature Name".ljust(35), "Status")

    print("-" * 60)

    print("AgeGroup".ljust(35), "✓")

    print("PurchaseFrequency".ljust(35), "✓")

    print("Customer Lifetime Value".ljust(35), "✓")

    print("LoyalCustomer".ljust(35), "✓")

    print("PurchaseCategory".ljust(35), "✓")

    print("-" * 60)

    print(f"Total Customers Processed : {len(df)}")

    print(f"Total Columns Available   : {len(df.columns)}")

    print(f"Dataset Saved             : {output_file}")

    print("=" * 65)

    print("\nPreview (First 5 Records)\n")

    print(df.head().to_string(index=False))

    print("=" * 65)

    return df