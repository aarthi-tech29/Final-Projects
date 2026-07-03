from spark_session import create_spark_session
from pyspark.sql.functions import *
import os

spark = create_spark_session()

# ==========================================
# Create reports folder
# ==========================================

os.makedirs("datasets/reports", exist_ok=True)

# ==========================================
# Load Integrated Dataset
# ==========================================

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("datasets/transformed/integrated_supply_chain")

print("=" * 60)
print("INVENTORY PREDICTION")
print("=" * 60)

# ==========================================
# Aggregate Product Inventory
# ==========================================

inventory = (

    df.groupBy(
        "Product_ID",
        "Product_Name",
        "Category"
    )

    .agg(

        sum("Current_Stock").alias("Current_Stock"),

        sum("Quantity_Sold").alias("Total_Sold"),

        avg("Quantity_Sold").alias("Average_Demand")

    )

)

# ==========================================
# Inventory Status
# ==========================================

inventory = inventory.withColumn(

    "Inventory_Status",

    when(col("Current_Stock") < 100, "Inventory Shortage")

    .when(col("Current_Stock") > 1000, "Over Stock")

    .otherwise("Optimal Stock")

)

# ==========================================
# Suggested Replenishment
# ==========================================

inventory = inventory.withColumn(

    "Recommended_Order",

    when(

        col("Inventory_Status") == "Inventory Shortage",

        round(col("Average_Demand") * 30)

    )

    .otherwise(lit(0))

)

# ==========================================
# Sort
# ==========================================

inventory = inventory.orderBy(desc("Recommended_Order"))

print("=" * 60)
print("Inventory Prediction")
print("=" * 60)

inventory.show(20, False)

# ==========================================
# Save Report
# ==========================================

inventory.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("datasets/reports/inventory_prediction")

print("=" * 60)
print("Inventory Prediction Report Saved")
print("=" * 60)

spark.stop()