from spark_session import create_spark_session
from pyspark.sql.functions import *
import os

spark = create_spark_session()

# ==========================================
# Create Reports Folder
# ==========================================

os.makedirs("datasets/reports", exist_ok=True)

# ==========================================
# Load Shipment Dataset
# ==========================================

shipment_df = spark.read \
.option("header", True) \
.option("inferSchema", True) \
.csv("datasets/raw/shipment.csv")

supplier_df = spark.read \
.option("header", True) \
.option("inferSchema", True) \
.csv("datasets/raw/suppliers.csv")

print("="*60)
print("TRANSPORTATION ANALYSIS")
print("="*60)

# ==========================================
# Join Shipment with Supplier
# ==========================================

transport = shipment_df.join(

    supplier_df,

    "Supplier_ID",

    "left"

)

# Rename Region column
if "Region" in transport.columns:
    transport = transport.withColumnRenamed(
        "Region",
        "Supplier_Region"
    )

# ==========================================
# Transportation Performance
# ==========================================

transport_report = (

    transport.groupBy(

        "Supplier_ID",

        "Supplier_Name",

        "Supplier_Region"

    )

    .agg(

        count("Shipment_ID").alias("Total_Shipments"),

        round(sum("Shipment_Cost"),2).alias("Total_Transport_Cost"),

        round(avg("Shipment_Cost"),2).alias("Average_Transport_Cost"),

        round(avg("Distance"),2).alias("Average_Distance"),

        max("Distance").alias("Maximum_Distance"),

        min("Distance").alias("Minimum_Distance")

    )

    .orderBy(desc("Total_Transport_Cost"))

)

print("="*60)
print("Transportation Performance")
print("="*60)

transport_report.show(20, False)

# ==========================================
# Save Report
# ==========================================

transport_report.write \
.mode("overwrite") \
.option("header", True) \
.csv("datasets/reports/transportation_analysis")

print("="*60)
print("Transportation Report Saved")
print("="*60)

spark.stop()