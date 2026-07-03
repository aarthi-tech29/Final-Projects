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