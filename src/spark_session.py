import os
import sys

from pyspark.sql import SparkSession


def create_spark_session():
    """
    Create and return a Spark Session
    """

    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    spark = (
        SparkSession.builder
        .appName("Supply Chain Analytics Platform")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark


if __name__ == "__main__":

    spark = create_spark_session()

    print("=" * 60)
    print("Spark Session Created Successfully")
    print("=" * 60)

    print("Spark Version :", spark.version)

    spark.stop()