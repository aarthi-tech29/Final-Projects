import pandas as pd
import numpy as np
from faker import Faker
import random
import os

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