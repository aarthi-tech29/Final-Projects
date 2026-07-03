<<<<<<< HEAD
import logging
import os

from src.load_data import load_all_data
from src.validate import validate_customer_data
from src.clean_data import clean_customer_data
from src.feature_engineering import feature_engineering
from src.merge_data import merge_customer_data
from src.statistics import generate_statistics
from src.segmentation import customer_segmentation
from src.mysql_store import store_to_mysql
from src.export import export_datasets


LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_FOLDER, "processing.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filemode="w"
)


def run_pipeline():
    """
    ==========================================================
          ENTERPRISE CUSTOMER DATA ETL PIPELINE
    ==========================================================
    """

    print("\n" + "=" * 80)
    print("            AUTOMATED ETL PIPELINE STARTED")
    print("=" * 80)

    logging.info("Pipeline Started")

    # ---------------------------------------------------------
    # Step 1 : Load Data
    # ---------------------------------------------------------

    csv_df, excel_df, json_df, api_df = load_all_data()

    logging.info("Datasets Loaded Successfully")

    # ---------------------------------------------------------
    # Step 2 : Validation
    # ---------------------------------------------------------

    validate_customer_data(csv_df)

    logging.info("Validation Completed")

    # ---------------------------------------------------------
    # Step 3 : Cleaning
    # ---------------------------------------------------------

    customer_df = clean_customer_data(csv_df)

    logging.info("Customer Data Cleaned")

    # ---------------------------------------------------------
    # Step 4 : Feature Engineering
    # ---------------------------------------------------------

    feature_df = feature_engineering(
        customer_df,
        excel_df
    )

    logging.info("Feature Engineering Completed")

    # ---------------------------------------------------------
    # Step 5 : Merge
    # ---------------------------------------------------------

    master_df = merge_customer_data(
        feature_df,
        excel_df,
        json_df,
        api_df
    )

    logging.info("Datasets Merged")

    # ---------------------------------------------------------
    # Step 6 : Statistics
    # ---------------------------------------------------------

    generate_statistics(master_df)

    logging.info("Statistics Generated")

    # ---------------------------------------------------------
    # Step 7 : Segmentation
    # ---------------------------------------------------------

    segmented_df = customer_segmentation(master_df)

    logging.info("Customer Segmentation Completed")

    # ---------------------------------------------------------
    # Step 8 : Store in MySQL
    # ---------------------------------------------------------

    store_to_mysql(segmented_df)

    logging.info("Stored in MySQL")

    # ---------------------------------------------------------
    # Step 9 : Export Files
    # ---------------------------------------------------------

    export_datasets(segmented_df)

    logging.info("Datasets Exported")

    logging.info("Pipeline Completed Successfully")

    print("\n" + "=" * 80)
    print("          ETL PIPELINE EXECUTED SUCCESSFULLY")
    print("=" * 80)
=======
import subprocess
import os
import sys

print("=" * 70)
print("SUPPLY CHAIN ANALYTICS PIPELINE")
print("=" * 70)

scripts = [

    "clean_data.py",

    "transform_data.py",

    "supplier_analysis.py",

    "demand_forecasting.py",

    "inventory_prediction.py",

    "warehouse_analysis.py",

    "transportation_analysis.py",

    "seasonal_analysis.py",

    "procurement_planning.py"

]

current_dir = os.path.dirname(__file__)

for script in scripts:

    print("\n" + "=" * 70)
    print(f"Running {script}")
    print("=" * 70)

    script_path = os.path.join(current_dir, script)

    result = subprocess.run(

        [sys.executable, script_path],

        capture_output=True,

        text=True

    )

    print(result.stdout)

    if result.stderr:

        print(result.stderr)

print("\n" + "=" * 70)
print("PIPELINE COMPLETED")
print("=" * 70)
>>>>>>> 97a553df6231bc30e5f83e5ac81e1532704fa22c
