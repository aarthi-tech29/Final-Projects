from spark_session import create_spark_session
from pyspark.sql.functions import col
import os

spark = create_spark_session()

# ===========================================
# Create output folder
# ===========================================

os.makedirs("datasets/transformed", exist_ok=True)

# ===========================================
# Load Cleaned CSV Files
# ===========================================

sales_df = spark.read.option("header", True).option("inferSchema", True).csv(
    "datasets/raw/sales.csv"
)

inventory_df = spark.read.option("header", True).option("inferSchema", True).csv(
    "datasets/raw/inventory.csv"
)

procurement_df = spark.read.option("header", True).option("inferSchema", True).csv(
    "datasets/raw/procurement.csv"
)

shipment_df = spark.read.option("header", True).option("inferSchema", True).csv(
    "datasets/raw/shipment.csv"
)

suppliers_df = spark.read.option("header", True).option("inferSchema", True).csv(
    "datasets/raw/suppliers.csv"
)

warehouse_df = spark.read.option("header", True).option("inferSchema", True).csv(
    "datasets/raw/warehouse.csv"
)

products_df = spark.read.option("header", True).option("inferSchema", True).csv(
    "datasets/raw/products.csv"
)

print("="*60)
print("DATA LOADED")
print("="*60)

# ===========================================
# Join Sales + Products
# ===========================================

df = sales_df.join(
    products_df,
    "Product_ID",
    "left"
)

# ===========================================
# Join Suppliers
# ===========================================

df = df.join(
    suppliers_df,
    "Supplier_ID",
    "left"
)

# ===========================================
# Join Warehouse
# ===========================================

df = df.join(
    warehouse_df,
    "Warehouse_ID",
    "left"
)

# ===========================================
# Join Inventory
# ===========================================

inventory_small = inventory_df.select(
    "Warehouse_ID",
    "Product_ID",
    "Current_Stock"
)

df = df.join(
    inventory_small,
    ["Warehouse_ID", "Product_ID"],
    "left"
)

# ===========================================
# Show Result
# ===========================================

print("="*60)
print("Integrated Dataset")
print("="*60)

print("Rows :", df.count())

df.printSchema()

df.show(10, truncate=False)

# ===========================================
# Save CSV
# ===========================================

df.write \
.mode("overwrite") \
.option("header", True) \
.csv("datasets/transformed/integrated_supply_chain")

print("="*60)
print("Integrated dataset saved successfully")
print("="*60)

spark.stop()