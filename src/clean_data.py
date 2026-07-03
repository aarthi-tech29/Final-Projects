<<<<<<< HEAD
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
=======
from spark_session import create_spark_session
from pyspark.sql.functions import *
import os

# =====================================================
# CREATE SPARK SESSION
# =====================================================

spark = create_spark_session()

# =====================================================
# CREATE OUTPUT FOLDER
# =====================================================

os.makedirs("datasets/cleaned", exist_ok=True)

# =====================================================
# LOAD DATASETS
# =====================================================

sales_df = spark.read.csv(
    "datasets/raw/sales.csv",
    header=True,
    inferSchema=True
)

inventory_df = spark.read.csv(
    "datasets/raw/inventory.csv",
    header=True,
    inferSchema=True
)

procurement_df = spark.read.csv(
    "datasets/raw/procurement.csv",
    header=True,
    inferSchema=True
)

shipment_df = spark.read.csv(
    "datasets/raw/shipment.csv",
    header=True,
    inferSchema=True
)

suppliers_df = spark.read.csv(
    "datasets/raw/suppliers.csv",
    header=True,
    inferSchema=True
)

warehouse_df = spark.read.csv(
    "datasets/raw/warehouse.csv",
    header=True,
    inferSchema=True
)

products_df = spark.read.csv(
    "datasets/raw/products.csv",
    header=True,
    inferSchema=True
)

# =====================================================
# REMOVE DUPLICATES
# =====================================================

sales_df = sales_df.dropDuplicates()
inventory_df = inventory_df.dropDuplicates()
procurement_df = procurement_df.dropDuplicates()
shipment_df = shipment_df.dropDuplicates()
suppliers_df = suppliers_df.dropDuplicates()
warehouse_df = warehouse_df.dropDuplicates()
products_df = products_df.dropDuplicates()

print("Duplicates Removed")

# =====================================================
# HANDLE NULL VALUES
# =====================================================

sales_df = sales_df.fillna(0)
inventory_df = inventory_df.fillna(0)
procurement_df = procurement_df.fillna(0)
shipment_df = shipment_df.fillna(0)

suppliers_df = suppliers_df.fillna("Unknown")
warehouse_df = warehouse_df.fillna("Unknown")
products_df = products_df.fillna("Unknown")

print("Null Values Handled")

# =====================================================
# REMOVE INVALID VALUES
# =====================================================

sales_df = sales_df.filter(col("Quantity_Sold") >= 0)

inventory_df = inventory_df.filter(col("Current_Stock") >= 0)

procurement_df = procurement_df.filter(col("Ordered_Qty") >= 0)

shipment_df = shipment_df.filter(col("Shipment_Cost") >= 0)

print("Negative Records Removed")

# =====================================================
# CONVERT DATES
# =====================================================

if "Date" in sales_df.columns:
    sales_df = sales_df.withColumn(
        "Date",
        to_date(col("Date"))
    )

if "Order_Date" in procurement_df.columns:
    procurement_df = procurement_df.withColumn(
        "Order_Date",
        to_date(col("Order_Date"))
    )

if "Delivery_Date" in procurement_df.columns:
    procurement_df = procurement_df.withColumn(
        "Delivery_Date",
        to_date(col("Delivery_Date"))
    )

if "Shipment_Date" in shipment_df.columns:
    shipment_df = shipment_df.withColumn(
        "Shipment_Date",
        to_date(col("Shipment_Date"))
    )

print("Date Conversion Completed")

# =====================================================
# VERIFY DATA
# =====================================================

print("=" * 60)
print("Clean Dataset Counts")
print("=" * 60)

print("Sales       :", sales_df.count())
print("Inventory   :", inventory_df.count())
print("Procurement :", procurement_df.count())
print("Shipment    :", shipment_df.count())
print("Suppliers   :", suppliers_df.count())
print("Warehouse   :", warehouse_df.count())
print("Products    :", products_df.count())

# =====================================================
# SAVE CLEANED DATA AS CSV
# =====================================================

print("\nSaving cleaned datasets...")

sales_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("datasets/cleaned/sales_clean")

inventory_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("datasets/cleaned/inventory_clean")

procurement_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("datasets/cleaned/procurement_clean")

shipment_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("datasets/cleaned/shipment_clean")

suppliers_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("datasets/cleaned/supplier_clean")

warehouse_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("datasets/cleaned/warehouse_clean")

products_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("datasets/cleaned/product_clean")

print("\n" + "=" * 60)
print("CLEAN DATASETS SAVED SUCCESSFULLY")
print("=" * 60)

print("""
Output Folder

datasets/
└── cleaned/
    ├── sales_clean/
    ├── inventory_clean/
    ├── procurement_clean/
    ├── shipment_clean/
    ├── supplier_clean/
    ├── warehouse_clean/
    └── product_clean/
""")

spark.stop()
>>>>>>> 97a553df6231bc30e5f83e5ac81e1532704fa22c
