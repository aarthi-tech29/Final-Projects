from spark_session import create_spark_session
from pyspark.sql.functions import *

spark = create_spark_session()

# =====================================
# LOAD TRANSFORMED DATA
# =====================================

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("datasets/transformed/integrated_supply_chain")

print("="*60)
print("Supplier Analysis")
print("="*60)

# Print schema (for verification)
df.printSchema()

# =====================================
# Rename Region Column
# =====================================

if "Region11" in df.columns:
    df = df.withColumnRenamed("Region11", "Supplier_Region")

if "Region13" in df.columns:
    df = df.withColumnRenamed("Region13", "Warehouse_Region")

# =====================================
# Supplier Performance
# =====================================

supplier_analysis = (

    df.groupBy(
        "Supplier_ID",
        "Supplier_Name",
        "Supplier_Region"
    )

    .agg(

        count("Sale_ID").alias("Total_Orders"),

        sum("Quantity_Sold").alias("Total_Quantity"),

        round(sum("Revenue"),2).alias("Total_Revenue"),

        round(avg("Selling_Price"),2).alias("Average_Selling_Price"),

        round(avg("Unit_Cost"),2).alias("Average_Unit_Cost")

    )

    .orderBy(desc("Total_Revenue"))

)

print("="*60)
print("TOP SUPPLIERS")
print("="*60)

supplier_analysis.show(20, False)

# =====================================
# SAVE REPORT
# =====================================

supplier_analysis.write \
.mode("overwrite") \
.option("header",True) \
.csv("datasets/reports/supplier_performance")

print("="*60)
print("Supplier Performance Report Saved")
print("="*60)

spark.stop()