<<<<<<< HEAD
import pandas as pd
import json
import os

# Dataset Folder
DATASET_PATH = "datasets"


def load_csv():
    """Load Customer CSV"""
    file_path = os.path.join(DATASET_PATH, "customers_csv.csv")

    df = pd.read_csv(file_path)

    print("\nCSV Dataset Loaded Successfully")
    print(df.head())

    return df


def load_excel():
    """Load Customer Excel"""

    file_path = os.path.join(DATASET_PATH, "customers_excel.xlsx")

    df = pd.read_excel(file_path)

    print("\nExcel Dataset Loaded Successfully")
    print(df.head())

    return df


def load_json():
    """Load Customer JSON"""

    file_path = os.path.join(DATASET_PATH, "customers_json.json")

    with open(file_path, "r") as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    print("\nJSON Dataset Loaded Successfully")
    print(df.head())

    return df


def load_api():
    """
    Simulated API
    Reads api_customers.json
    """

    file_path = os.path.join(DATASET_PATH, "api_customers.json")

    with open(file_path, "r") as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    print("\nAPI Dataset Loaded Successfully")
    print(df.head())

    return df


def load_all_data():
    """
    Load all datasets
    """

    csv_df = load_csv()

    excel_df = load_excel()

    json_df = load_json()

    api_df = load_api()

    return csv_df, excel_df, json_df, api_df


if __name__ == "__main__":

    csv_df, excel_df, json_df, api_df = load_all_data()
=======
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
>>>>>>> 97a553df6231bc30e5f83e5ac81e1532704fa22c
