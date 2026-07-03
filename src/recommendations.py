from spark_session import create_spark_session
from pyspark.sql.functions import *
import os

spark = create_spark_session()

# ==========================================
# Create Reports Folder
# ==========================================

os.makedirs("datasets/reports", exist_ok=True)

# ==========================================
# Load Reports
# ==========================================

supplier = spark.read.option("header",True).option("inferSchema",True).csv(
    "datasets/reports/supplier_performance"
)

forecast = spark.read.option("header",True).option("inferSchema",True).csv(
    "datasets/reports/demand_forecast"
)

inventory = spark.read.option("header",True).option("inferSchema",True).csv(
    "datasets/reports/inventory_prediction"
)

warehouse = spark.read.option("header",True).option("inferSchema",True).csv(
    "datasets/reports/warehouse_utilization"
)

transport = spark.read.option("header",True).option("inferSchema",True).csv(
    "datasets/reports/transportation_analysis"
)

procurement = spark.read.option("header",True).option("inferSchema",True).csv(
    "datasets/reports/procurement_plan"
)

print("="*70)
print("EXECUTIVE SUPPLY CHAIN REPORT")
print("="*70)

# ==========================================
# KPI SUMMARY
# ==========================================

print("\nTOP 5 SUPPLIERS")
supplier.orderBy(desc("Total_Revenue")).show(5,False)

print("\nTOP 5 DEMAND PRODUCTS")
forecast.orderBy(desc("Forecast_Next_Month")).show(5,False)

print("\nWAREHOUSE UTILIZATION")
warehouse.show(5,False)

print("\nTRANSPORTATION PERFORMANCE")
transport.show(5,False)

print("\nPROCUREMENT SUMMARY")
procurement.show(5,False)

print("\nINVENTORY STATUS")
inventory.show(5,False)

# ==========================================
# EXECUTIVE RECOMMENDATIONS
# ==========================================

recommendations = [

("Increase inventory for products with high forecasted demand.",),

("Review suppliers with high procurement cost.",),

("Optimize warehouse utilization by balancing inventory.",),

("Reduce transportation cost through route optimization.",),

("Improve procurement scheduling for seasonal demand.",),

("Monitor low-stock products daily.",),

("Review supplier delivery performance monthly.",),

("Use demand forecasting for procurement planning.",),

("Increase safety stock for high-demand products.",),

("Create weekly executive KPI dashboards.",)

]

recommendation_df = spark.createDataFrame(
    recommendations,
    ["Recommendation"]
)

recommendation_df.show(truncate=False)

# ==========================================
# Save Recommendations
# ==========================================

recommendation_df.write \
.mode("overwrite") \
.option("header",True) \
.csv("datasets/reports/executive_recommendations")

print("="*70)
print("Executive Recommendations Saved")
print("="*70)

spark.stop()