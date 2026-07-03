from spark_session import create_spark_session
from pyspark.sql.functions import *
import os

spark = create_spark_session()

# ==========================================
# Create Reports Folder
# ==========================================

os.makedirs("datasets/reports", exist_ok=True)

# ==========================================
# Load Procurement Dataset
# ==========================================

procurement_df = spark.read \
.option("header", True) \
.option("inferSchema", True) \
.csv("datasets/raw/procurement.csv")

supplier_df = spark.read \
.option("header", True) \
.option("inferSchema", True) \
.csv("datasets/raw/suppliers.csv")

print("="*60)
print("PROCUREMENT PLANNING")
print("="*60)

# ==========================================
# Join Supplier Details
# ==========================================

procurement = procurement_df.join(
    supplier_df,
    "Supplier_ID",
    "left"
)

# Rename Region if available
if "Region" in procurement.columns:
    procurement = procurement.withColumnRenamed(
        "Region",
        "Supplier_Region"
    )

# ==========================================
# Procurement Analysis
# ==========================================

report = (

    procurement.groupBy(
        "Supplier_ID",
        "Supplier_Name",
        "Supplier_Region"
    )

    .agg(

        count("Purchase_ID").alias("Total_Purchases"),

        sum("Ordered_Qty").alias("Total_Ordered_Qty"),

        round(sum("Purchase_Cost"),2).alias("Total_Purchase_Cost"),

        round(avg("Purchase_Cost"),2).alias("Average_Purchase_Cost")

    )

    .orderBy(desc("Total_Purchase_Cost"))

)

print("="*60)
print("Procurement Planning Report")
print("="*60)

report.show(20, False)

# ==========================================
# Save Report
# ==========================================

report.write \
.mode("overwrite") \
.option("header",True) \
.csv("datasets/reports/procurement_plan")

print("="*60)
print("Procurement Planning Report Saved")
print("="*60)

spark.stop()