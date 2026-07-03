from spark_session import create_spark_session
from pyspark.sql.functions import *
import os

spark = create_spark_session()

os.makedirs("datasets/reports", exist_ok=True)

# ===========================================
# LOAD TRANSFORMED DATA
# ===========================================

df = spark.read \
.option("header", True) \
.option("inferSchema", True) \
.csv("datasets/transformed/integrated_supply_chain")

print("="*60)
print("DEMAND FORECASTING")
print("="*60)

# ===========================================
# PRODUCT DEMAND
# ===========================================

forecast = (

    df.groupBy(
        "Product_ID",
        "Product_Name",
        "Category"
    )

    .agg(

        sum("Quantity_Sold").alias("Historical_Demand"),

        avg("Quantity_Sold").alias("Average_Demand"),

        max("Quantity_Sold").alias("Peak_Demand"),

        min("Quantity_Sold").alias("Lowest_Demand"),

        sum("Revenue").alias("Total_Revenue")

    )

)

# ===========================================
# FORECAST
# ===========================================

forecast = forecast.withColumn(

    "Forecast_Next_Month",

    round(col("Average_Demand")*1.15,2)

)

forecast = forecast.withColumn(

    "Forecast_Next_Quarter",

    round(col("Average_Demand")*3.40,2)

)

forecast = forecast.orderBy(desc("Forecast_Next_Month"))

print("="*60)
print("TOP PRODUCTS")
print("="*60)

forecast.show(20,False)

# ===========================================
# SAVE REPORT
# ===========================================

forecast.write \
.mode("overwrite") \
.option("header",True) \
.csv("datasets/reports/demand_forecast")

print("="*60)
print("Demand Forecast Report Saved")
print("="*60)

spark.stop()