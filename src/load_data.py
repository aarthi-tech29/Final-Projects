from spark_session import create_spark_session

# Create Spark Session
spark = create_spark_session()

# -------------------------
# Load CSV Files
# -------------------------

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

# -------------------------
# Print Row Counts
# -------------------------

print("=" * 60)
print("ROW COUNTS")
print("=" * 60)

print("Sales       :", sales_df.count())
print("Inventory   :", inventory_df.count())
print("Procurement :", procurement_df.count())
print("Shipment    :", shipment_df.count())
print("Suppliers   :", suppliers_df.count())
print("Warehouse   :", warehouse_df.count())
print("Products    :", products_df.count())

# -------------------------
# Print Schema
# -------------------------

print("\nSales Schema")
sales_df.printSchema()

print("\nInventory Schema")
inventory_df.printSchema()

print("\nProcurement Schema")
procurement_df.printSchema()

print("\nShipment Schema")
shipment_df.printSchema()

# -------------------------
# Show Sample Records
# -------------------------

print("\nSales Data")
sales_df.show(5)

print("\nInventory Data")
inventory_df.show(5)

print("\nProcurement Data")
procurement_df.show(5)

print("\nShipment Data")
shipment_df.show(5)

spark.stop()