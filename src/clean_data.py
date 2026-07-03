import pandas as pd
import os

OUTPUT_FOLDER = "cleaned_data"


def clean_customer_data(df):
    """
    ==========================================================
            ENTERPRISE CUSTOMER DATA CLEANING
    ==========================================================

    Operations:
    1. Remove Duplicate Records
    2. Handle Missing Values
    3. Standardize Customer Data
    4. Clean Phone Numbers
    5. Export Clean Dataset
    ==========================================================
    """

    print("\n" + "=" * 70)
    print("               CUSTOMER DATA CLEANING")
    print("=" * 70)

    # ---------------------------------------------------------
    # Make a Copy
    # ---------------------------------------------------------

    df = df.copy()

    # ---------------------------------------------------------
    # Remove Duplicate Records
    # ---------------------------------------------------------

    before_rows = len(df)

    df = df.drop_duplicates(subset="CustomerID").reset_index(drop=True)

    after_rows = len(df)

    duplicates_removed = before_rows - after_rows

    # ---------------------------------------------------------
    # Handle Missing Age
    # ---------------------------------------------------------

    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Age"] = df["Age"].fillna(df["Age"].median())

    # ---------------------------------------------------------
    # Clean Phone Numbers
    # ---------------------------------------------------------

    df["Phone"] = (
        df["Phone"]
        .astype(str)
        .replace("nan", "")
        .replace("None", "")
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    df["Phone"] = df["Phone"].replace("", "9999999999")

    # ---------------------------------------------------------
    # Handle Missing Email
    # ---------------------------------------------------------

    df["Email"] = (
        df["Email"]
        .fillna("unknown@gmail.com")
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # ---------------------------------------------------------
    # Standardize Customer Name
    # ---------------------------------------------------------

    df["Name"] = (
        df["Name"]
        .astype(str)
        .str.title()
        .str.strip()
    )

    # ---------------------------------------------------------
    # Standardize Address
    # ---------------------------------------------------------

    df["City"] = (
        df["City"]
        .astype(str)
        .str.title()
        .str.strip()
    )

    df["State"] = (
        df["State"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["Country"] = (
        df["Country"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # ---------------------------------------------------------
    # Save Clean Dataset
    # ---------------------------------------------------------

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    output_file = os.path.join(
        OUTPUT_FOLDER,
        "customer_master.csv"
    )

    df.to_csv(output_file, index=False)

    # ---------------------------------------------------------
    # Display Summary
    # ---------------------------------------------------------

    print("\n✓ Duplicate Records Removed")
    print(f"Records Before Cleaning : {before_rows}")
    print(f"Records After Cleaning  : {after_rows}")
    print(f"Duplicates Removed      : {duplicates_removed}")

    print("\n✓ Missing Values Handled")
    print("✓ Customer Names Standardized")
    print("✓ Email Addresses Standardized")
    print("✓ Phone Numbers Cleaned")
    print("✓ Address Information Standardized")

    print(f"\nDataset Saved : {output_file}")

    print("=" * 70)

    preview_columns = [
        "CustomerID",
        "Name",
        "Age",
        "City",
        "Phone",
        "Email"
    ]

    print("\nPreview of Cleaned Data")
    print("-" * 90)
    print(df[preview_columns].head().to_string(index=False))
    print("-" * 90)

    return df