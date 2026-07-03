from spark_session import create_spark_session
from pyspark.sql.functions import *
import os

spark = create_spark_session()

# ==========================================
# Create Reports Folder
# ==========================================

os.makedirs("datasets/reports", exist_ok=True)

# ==========================================
# Load Integrated Dataset
# ==========================================

df = spark.read \
.option("header", True) \
.option("inferSchema", True) \
.csv("datasets/transformed/integrated_supply_chain")

print("="*60)
print("SEASONAL DEMAND ANALYSIS")
print("="*60)

# ==========================================
# Create Month Column
# ==========================================

if "Date" in df.columns:
    df = df.withColumn(
        "Month",
        month(col("Date"))
    )
else:
    print("Date column not found.")
    spark.stop()
    exit()

# ==========================================
# Monthly Analysis
# ==========================================

seasonal = (

    df.groupBy("Month")

    .agg(

        count("Sale_ID").alias("Total_Orders"),

        sum("Quantity_Sold").alias("Total_Quantity"),

        round(sum("Revenue"),2).alias("Total_Revenue"),

        round(avg("Quantity_Sold"),2).alias("Average_Demand")

    )

    .orderBy("Month")

)

print("="*60)
print("Monthly Demand")
print("="*60)

seasonal.show(12, False)

# ==========================================
# Peak Month
# ==========================================

peak = seasonal.orderBy(desc("Total_Revenue"))

print("="*60)
print("Highest Revenue Month")
print("="*60)

peak.show(1, False)

# ==========================================
# Save Report
# ==========================================

seasonal.write \
.mode("overwrite") \
.option("header",True) \
.csv("datasets/reports/seasonal_analysis")

print("="*60)
print("Seasonal Report Saved")
print("="*60)

spark.stop()