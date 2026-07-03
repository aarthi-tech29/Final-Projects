import pandas as pd
import numpy as np
from faker import Faker
import random
import os
from datetime import datetime, timedelta

fake = Faker()

# -------------------------
# Create folders
# -------------------------
os.makedirs("datasets/raw", exist_ok=True)

np.random.seed(42)
random.seed(42)

# -------------------------
# Constants
# -------------------------

NUM_PRODUCTS = 1000
NUM_SUPPLIERS = 500
NUM_WAREHOUSES = 100
NUM_SALES = 100000
NUM_INVENTORY = 50000
NUM_PROCUREMENT = 50000
NUM_SHIPMENTS = 50000

regions = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

categories = [
    "Electronics",
    "Furniture",
    "Food",
    "Clothing",
    "Medical",
    "Sports",
    "Office"
]

transport_modes = [
    "Truck",
    "Ship",
    "Air",
    "Rail"
]

delivery_status = [
    "Delivered",
    "Delayed",
    "In Transit"
]

customer_types = [
    "Retail",
    "Wholesale",
    "Online"
]

seasons = [
    "Winter",
    "Spring",
    "Summer",
    "Autumn"
]
# ==========================================================
# GENERATE PRODUCTS
# ==========================================================

print("Generating Products...")

products = []

for i in range(1, NUM_PRODUCTS + 1):

    category = random.choice(categories)

    cost = round(random.uniform(10, 1000), 2)

    selling_price = round(cost * random.uniform(1.20, 2.00), 2)

    products.append([
        f"P{i:04}",
        category,
        fake.word().capitalize() + " Product",
        cost,
        selling_price
    ])

products_df = pd.DataFrame(products, columns=[
    "Product_ID",
    "Category",
    "Product_Name",
    "Unit_Cost",
    "Selling_Price"
])

print(products_df.head())

# ==========================================================
# GENERATE SUPPLIERS
# ==========================================================

print("Generating Suppliers...")

suppliers = []

for i in range(1, NUM_SUPPLIERS + 1):

    suppliers.append([

        f"S{i:03}",

        fake.company(),

        random.choice(regions),

        round(random.uniform(3.0, 5.0), 2),

        round(random.uniform(50, 500), 2),

        round(random.uniform(70, 100), 2),

        round(random.uniform(80, 100), 2)

    ])

suppliers_df = pd.DataFrame(

    suppliers,

    columns=[

        "Supplier_ID",

        "Supplier_Name",

        "Region",

        "Supplier_Rating",

        "Average_Cost",

        "Quality_Score",

        "On_Time_Delivery"

    ]

)

print(suppliers_df.head())

# ==========================================================
# GENERATE WAREHOUSES
# ==========================================================

print("Generating Warehouses...")

warehouses = []

for i in range(1, NUM_WAREHOUSES + 1):

    capacity = random.randint(5000, 25000)

    utilization = random.randint(1000, capacity)

    warehouses.append([

        f"W{i:03}",

        f"Warehouse {i}",

        random.choice(regions),

        capacity,

        utilization,

        fake.name()

    ])

warehouse_df = pd.DataFrame(

    warehouses,

    columns=[

        "Warehouse_ID",

        "Warehouse_Name",

        "Region",

        "Capacity",

        "Current_Utilization",

        "Manager"

    ]

)

print(warehouse_df.head())

print("Master datasets generated successfully.")
# ==========================================================
# GENERATE SALES DATASET
# ==========================================================

print("Generating Sales Dataset...")

sales = []

start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)

date_range = (end_date - start_date).days

for i in range(1, NUM_SALES + 1):

    sale_date = start_date + timedelta(days=random.randint(0, date_range))

    month = sale_date.month

    if month in [12, 1, 2]:
        season = "Winter"
        seasonal_factor = 1.20
    elif month in [3, 4, 5]:
        season = "Spring"
        seasonal_factor = 1.05
    elif month in [6, 7, 8]:
        season = "Summer"
        seasonal_factor = 1.15
    else:
        season = "Autumn"
        seasonal_factor = 1.00

    product = products_df.sample(1).iloc[0]

    supplier = suppliers_df.sample(1).iloc[0]

    warehouse = warehouse_df.sample(1).iloc[0]

    quantity = random.randint(1, 200)

    quantity = int(quantity * seasonal_factor)

    unit_price = product["Selling_Price"]

    discount = round(random.uniform(0, 0.30), 2)

    revenue = round(quantity * unit_price * (1 - discount), 2)

    sales.append([

        i,

        sale_date.strftime("%Y-%m-%d"),

        product["Product_ID"],

        warehouse["Warehouse_ID"],

        supplier["Supplier_ID"],

        warehouse["Region"],

        quantity,

        unit_price,

        revenue,

        discount,

        random.choice(customer_types),

        season

    ])

sales_df = pd.DataFrame(

    sales,

    columns=[

        "Sale_ID",

        "Date",

        "Product_ID",

        "Warehouse_ID",

        "Supplier_ID",

        "Region",

        "Quantity_Sold",

        "Unit_Price",

        "Revenue",

        "Discount",

        "Customer_Type",

        "Season"

    ]

)

print(sales_df.head())

print("Sales Dataset Generated")
# ==========================================================
# GENERATE INVENTORY DATASET
# ==========================================================

print("Generating Inventory Dataset...")

inventory = []

for i in range(1, NUM_INVENTORY + 1):

    warehouse = warehouse_df.sample(1).iloc[0]
    product = products_df.sample(1).iloc[0]

    max_capacity = random.randint(500, 5000)

    current_stock = random.randint(0, max_capacity)

    safety_stock = random.randint(50, 300)

    reorder_level = safety_stock + random.randint(20, 100)

    utilization = round((current_stock / max_capacity) * 100, 2)

    if current_stock <= safety_stock:
        stock_status = "Low Stock"

    elif current_stock >= max_capacity * 0.90:
        stock_status = "Overstock"

    else:
        stock_status = "Normal"

    inventory.append([

        i,

        (start_date + timedelta(days=random.randint(0, date_range))).strftime("%Y-%m-%d"),

        warehouse["Warehouse_ID"],

        product["Product_ID"],

        current_stock,

        safety_stock,

        reorder_level,

        max_capacity,

        utilization,

        stock_status

    ])

inventory_df = pd.DataFrame(

    inventory,

    columns=[

        "Inventory_ID",

        "Date",

        "Warehouse_ID",

        "Product_ID",

        "Current_Stock",

        "Safety_Stock",

        "Reorder_Level",

        "Maximum_Capacity",

        "Warehouse_Utilization",

        "Stock_Status"

    ]

)

print(inventory_df.head())

print("Inventory Dataset Generated Successfully")
# ==========================================================
# GENERATE PROCUREMENT DATASET
# ==========================================================

print("Generating Procurement Dataset...")

procurement = []

for i in range(1, NUM_PROCUREMENT + 1):

    supplier = suppliers_df.sample(1).iloc[0]
    product = products_df.sample(1).iloc[0]

    order_date = start_date + timedelta(days=random.randint(0, date_range))

    lead_time = random.randint(2, 20)

    delivery_date = order_date + timedelta(days=lead_time)

    ordered_qty = random.randint(100, 1000)

    received_qty = ordered_qty - random.randint(0, 20)

    purchase_cost = round(
        ordered_qty * product["Unit_Cost"] * random.uniform(0.90, 1.10),
        2
    )

    delivery_status = "On Time"

    if lead_time > 12:
        delivery_status = "Delayed"

    procurement.append([

        i,

        supplier["Supplier_ID"],

        supplier["Supplier_Name"],

        product["Product_ID"],

        product["Category"],

        order_date.strftime("%Y-%m-%d"),

        delivery_date.strftime("%Y-%m-%d"),

        ordered_qty,

        received_qty,

        purchase_cost,

        lead_time,

        delivery_status

    ])

procurement_df = pd.DataFrame(

    procurement,

    columns=[

        "Purchase_ID",

        "Supplier_ID",

        "Supplier_Name",

        "Product_ID",

        "Category",

        "Order_Date",

        "Delivery_Date",

        "Ordered_Qty",

        "Received_Qty",

        "Purchase_Cost",

        "Lead_Time",

        "Delivery_Status"

    ]

)

print(procurement_df.head())

print("Procurement Dataset Generated Successfully")
# ==========================================================
# GENERATE SHIPMENT DATASET
# ==========================================================

print("Generating Shipment Dataset...")

shipments = []

destinations = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Phoenix",
    "Dallas",
    "Miami",
    "Seattle",
    "Boston",
    "Atlanta"
]

for i in range(1, NUM_SHIPMENTS + 1):

    warehouse = warehouse_df.sample(1).iloc[0]
    supplier = suppliers_df.sample(1).iloc[0]

    shipment_date = start_date + timedelta(days=random.randint(0, date_range))

    transport = random.choice(transport_modes)

    distance = random.randint(50, 3000)

    if transport == "Air":
        days = random.randint(1, 3)
    elif transport == "Truck":
        days = random.randint(2, 7)
    elif transport == "Rail":
        days = random.randint(4, 8)
    else:
        days = random.randint(10, 20)

    delivery_date = shipment_date + timedelta(days=days)

    shipment_cost = round(distance * random.uniform(1.5, 5.5), 2)

    if days <= 5:
        status = "Delivered"
    elif days <= 10:
        status = "In Transit"
    else:
        status = "Delayed"

    shipments.append([

        i,

        warehouse["Warehouse_ID"],

        supplier["Supplier_ID"],

        random.choice(destinations),

        shipment_date.strftime("%Y-%m-%d"),

        delivery_date.strftime("%Y-%m-%d"),

        transport,

        shipment_cost,

        status,

        distance

    ])

shipment_df = pd.DataFrame(

    shipments,

    columns=[

        "Shipment_ID",

        "Warehouse_ID",

        "Supplier_ID",

        "Destination",

        "Shipment_Date",

        "Delivery_Date",

        "Transportation_Mode",

        "Shipment_Cost",

        "Delivery_Status",

        "Distance"

    ]

)

print(shipment_df.head())

print("Shipment Dataset Generated Successfully")

# ==========================================================
# SAVE DATASETS
# ==========================================================

print("\nSaving datasets...\n")

products_df.to_csv(
    "datasets/raw/products.csv",
    index=False
)

suppliers_df.to_csv(
    "datasets/raw/suppliers.csv",
    index=False
)

warehouse_df.to_csv(
    "datasets/raw/warehouse.csv",
    index=False
)

sales_df.to_csv(
    "datasets/raw/sales.csv",
    index=False
)

inventory_df.to_csv(
    "datasets/raw/inventory.csv",
    index=False
)

procurement_df.to_csv(
    "datasets/raw/procurement.csv",
    index=False
)

shipment_df.to_csv(
    "datasets/raw/shipment.csv",
    index=False
)

print("=" * 60)
print("SUPPLY CHAIN DATASETS GENERATED SUCCESSFULLY")
print("=" * 60)

print(f"Products       : {len(products_df):,}")
print(f"Suppliers      : {len(suppliers_df):,}")
print(f"Warehouses     : {len(warehouse_df):,}")
print(f"Sales          : {len(sales_df):,}")
print(f"Inventory      : {len(inventory_df):,}")
print(f"Procurement    : {len(procurement_df):,}")
print(f"Shipments      : {len(shipment_df):,}")

print("\nFiles saved to:")
print("datasets/raw/")

print("""
Generated Files
---------------
products.csv
suppliers.csv
warehouse.csv
sales.csv
inventory.csv
procurement.csv
shipment.csv
""")

print("Dataset generation completed successfully!")