import pandas as pd
import numpy as np
import os

OUTPUT_FOLDER = "cleaned_data"


def customer_segmentation(df):
    """
    ==========================================================
           ENTERPRISE CUSTOMER SEGMENTATION
    ==========================================================

    Segmentation based on Customer Lifetime Value (CLV)

    Platinum : CLV >= 100000
    Gold     : CLV >= 60000
    Silver   : CLV >= 30000
    Bronze   : CLV < 30000

    ==========================================================
    """

    print("\n" + "=" * 70)
    print("             CUSTOMER SEGMENTATION")
    print("=" * 70)

    # -------------------------------------------------------
    # Customer Segments
    # -------------------------------------------------------

    conditions = [
        df["CLV"] >= 100000,
        (df["CLV"] >= 60000) & (df["CLV"] < 100000),
        (df["CLV"] >= 30000) & (df["CLV"] < 60000),
        df["CLV"] < 30000
    ]

    segments = [
        "Platinum",
        "Gold",
        "Silver",
        "Bronze"
    ]

    df["Segment"] = np.select(
        conditions,
        segments,
        default="Bronze"
    )

    # -------------------------------------------------------
    # Segment Summary
    # -------------------------------------------------------

    segment_summary = (
        df["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_summary.columns = [
        "Segment",
        "CustomerCount"
    ]

    # -------------------------------------------------------
    # Save Files
    # -------------------------------------------------------

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    df.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "customer_segments.csv"
        ),
        index=False
    )

    segment_summary.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "segment_summary.csv"
        ),
        index=False
    )

    # -------------------------------------------------------
    # Display
    # -------------------------------------------------------

    print("\nCustomer Segmentation Completed\n")

    print(segment_summary.to_string(index=False))

    print("\nFiles Created")

    print("-----------------------------------------")

    print("✓ customer_segments.csv")

    print("✓ segment_summary.csv")

    print("=" * 70)

    return df