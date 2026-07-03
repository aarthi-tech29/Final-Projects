import os
import sys

# Tell Spark exactly which Python executable to use
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Supply Chain Analytics")
    .master("local[*]")
    .getOrCreate()
)

data = [
    (1, "Laptop", 120),
    (2, "Phone", 80),
    (3, "Tablet", 50)
]

df = spark.createDataFrame(data, ["ID", "Product", "Sales"])
df.show()

spark.stop()