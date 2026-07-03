import pandas as pd
import os

OUTPUT_FOLDER = "cleaned_data"


def merge_customer_data(customer_df, purchase_df, json_df, api_df):
    """
    ==========================================================
          ENTERPRISE CUSTOMER DATA MERGING
    ==========================================================
    Merge:
        1. Customer CSV
        2. Purchase Excel
        3. Customer JSON
        4. API Customer Data

    Output:
        customer_master_dataset.csv
    ==========================================================
    """

    print("\n" + "=" * 70)
    print("              CUSTOMER DATA MERGING STARTED")
    print("=" * 70)

    # ---------------------------------------------------------
    # Merge Customer + Purchase
    # ---------------------------------------------------------

    merged_df = pd.merge(
        customer_df,
        purchase_df,
        on="CustomerID",
        how="left",
        suffixes=("", "_purchase")
    )

    print("✓ Customer Dataset + Purchase Dataset Merged")

    # ---------------------------------------------------------
    # Merge JSON Dataset
    # ---------------------------------------------------------

    merged_df = pd.merge(
        merged_df,
        json_df,
        on="CustomerID",
        how="left"
    )

    print("✓ Demographic Dataset Merged")

    # ---------------------------------------------------------
    # Merge API Dataset
    # ---------------------------------------------------------

    merged_df = pd.merge(
        merged_df,
        api_df,
        on="CustomerID",
        how="left"
    )

    print("✓ API Dataset Merged")

    # ---------------------------------------------------------
    # Fill Missing Values
    # ---------------------------------------------------------

    merged_df["Occupation"] = merged_df["Occupation"].fillna("Unknown")
    merged_df["Income"] = merged_df["Income"].fillna(0)
    merged_df["MaritalStatus"] = merged_df["MaritalStatus"].fillna("Unknown")
    merged_df["Membership"] = merged_df["Membership"].fillna("None")
    merged_df["RewardPoints"] = merged_df["RewardPoints"].fillna(0)
    merged_df["Status"] = merged_df["Status"].fillna("Inactive")

    # ---------------------------------------------------------
    # Save Dataset
    # ---------------------------------------------------------

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    output_file = os.path.join(
        OUTPUT_FOLDER,
        "customer_master_dataset.csv"
    )

    merged_df.to_csv(output_file, index=False)

    # ---------------------------------------------------------
    # Display Summary
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("              DATA MERGING COMPLETED")
    print("=" * 70)

    print(f"Total Records           : {len(merged_df)}")
    print(f"Total Columns           : {len(merged_df.columns)}")
    print(f"Dataset Saved           : {output_file}")

    print("\nMerged Datasets")
    print("-" * 70)
    print("✓ Customer CSV")
    print("✓ Purchase Excel")
    print("✓ Customer JSON")
    print("✓ API Customer JSON")

    print("-" * 70)

    # ---------------------------------------------------------
    # Preview
    # ---------------------------------------------------------

    preview_columns = [
        "CustomerID",
        "Name",
        "Age",
        "City",
        "Orders",
        "TotalPurchase",
        "Income",
        "Membership",
        "RewardPoints",
        "CLV",
        "PurchaseCategory"
    ]

    print("\nPreview of Master Dataset")
    print("-" * 120)

    print(
        merged_df[preview_columns]
        .head()
        .to_string(index=False)
    )

    print("-" * 120)

    return merged_df