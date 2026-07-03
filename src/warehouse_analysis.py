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
print("WAREHOUSE ANALYSIS")
print("=" * 60)

# ------------------------------------------
# Rename duplicate warehouse region column
# ------------------------------------------

if "Region13" in df.columns:
    df = df.withColumnRenamed("Region13", "Warehouse_Region")

# ==========================================
# Warehouse Analysis
# ==========================================

warehouse = (

    df.groupBy(
        "Warehouse_ID",
        "Warehouse_Name",
        "Warehouse_Region"
    )

    .agg(

        count("Sale_ID").alias("Total_Orders"),

        sum("Quantity_Sold").alias("Products_Moved"),

        sum("Current_Stock").alias("Current_Stock"),

        round(sum("Revenue"),2).alias("Total_Revenue"),

        round(avg("Quantity_Sold"),2).alias("Average_Movement")

    )

)

# ==========================================
# Warehouse Utilization
# ==========================================

warehouse = warehouse.withColumn(

    "Warehouse_Utilization",

    when(col("Current_Stock") < 5000, "Low")

    .when(col("Current_Stock") < 15000, "Medium")

    .otherwise("High")

)

warehouse = warehouse.orderBy(desc("Total_Revenue"))

print("="*60)
print("Warehouse Performance")
print("="*60)

warehouse.show(20,False)

# ==========================================
# Save Report
# ==========================================

warehouse.write \
.mode("overwrite") \
.option("header",True) \
.csv("datasets/reports/warehouse_utilization")

print("="*60)
print("Warehouse Report Saved")
print("="*60)

spark.stop()