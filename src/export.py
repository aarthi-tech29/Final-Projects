import pandas as pd
import os

OUTPUT_FOLDER = "cleaned_data"
REPORT_FOLDER = "reports"


def export_datasets(df):
    """
    ==========================================================
            EXPORT DATASETS & DATA QUALITY REPORT
    ==========================================================

    1. Analytics Ready Dataset
    2. ML Ready Dataset
    3. Data Quality Report

    ==========================================================
    """

    print("\n" + "=" * 70)
    print("            EXPORTING DATASETS")
    print("=" * 70)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(REPORT_FOLDER, exist_ok=True)

    # =====================================================
    # Analytics Dataset
    # =====================================================

    analytics_columns = [
        "CustomerID",
        "Name",
        "Gender",
        "Age",
        "City",
        "Orders",
        "TotalPurchase",
        "Income",
        "CLV",
        "PurchaseFrequency",
        "Segment"
    ]

    analytics_df = df[analytics_columns]

    analytics_file = os.path.join(
        OUTPUT_FOLDER,
        "analytics_dataset.csv"
    )

    analytics_df.to_csv(
        analytics_file,
        index=False
    )

    # =====================================================
    # ML Dataset
    # =====================================================

    ml_columns = [
        "Age",
        "Orders",
        "TotalPurchase",
        "Income",
        "RewardPoints",
        "CLV",
        "PurchaseFrequency"
    ]

    ml_df = df[ml_columns]

    ml_file = os.path.join(
        OUTPUT_FOLDER,
        "ml_ready_dataset.csv"
    )

    ml_df.to_csv(
        ml_file,
        index=False
    )

    # =====================================================
    # Data Quality Report
    # =====================================================

    report = pd.DataFrame({

        "Metric": [

            "Total Records",
            "Total Columns",
            "Missing Values",
            "Duplicate Records"

        ],

        "Value": [

            len(df),
            len(df.columns),
            int(df.isnull().sum().sum()),
            int(df.duplicated().sum())

        ]

    })

    report_file = os.path.join(
        REPORT_FOLDER,
        "data_quality_report.xlsx"
    )

    report.to_excel(
        report_file,
        index=False
    )

    # =====================================================
    # Display
    # =====================================================

    print("✓ Analytics Dataset Exported")

    print("✓ ML Ready Dataset Exported")

    print("✓ Data Quality Report Generated")

    print("\nFiles Created")

    print("----------------------------------------")

    print("analytics_dataset.csv")

    print("ml_ready_dataset.csv")

    print("data_quality_report.xlsx")

    print("=" * 70)

    return analytics_df, ml_df