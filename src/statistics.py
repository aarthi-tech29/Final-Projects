import pandas as pd
import os

REPORT_FOLDER = "reports"


def generate_statistics(df):
    """
    ==========================================================
          ENTERPRISE CUSTOMER STATISTICAL ANALYSIS
    ==========================================================
    """

    print("\n" + "=" * 70)
    print("          CUSTOMER STATISTICAL ANALYSIS")
    print("=" * 70)

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    # -------------------------------------------------------
    # Basic Statistics
    # -------------------------------------------------------

    total_customers = len(df)

    average_age = round(df["Age"].mean(), 2)

    average_income = round(df["Income"].mean(), 2)

    average_purchase = round(df["TotalPurchase"].mean(), 2)

    average_clv = round(df["CLV"].mean(), 2)

    total_sales = round(df["TotalPurchase"].sum(), 2)

    highest_purchase = round(df["TotalPurchase"].max(), 2)

    lowest_purchase = round(df["TotalPurchase"].min(), 2)

    # -------------------------------------------------------
    # Customer Segments Count
    # -------------------------------------------------------

    membership_count = df["Membership"].value_counts()

    city_count = df["City"].value_counts()

    # -------------------------------------------------------
    # Correlation
    # -------------------------------------------------------

    correlation = df[
        ["Age", "Income", "Orders", "TotalPurchase", "CLV"]
    ].corr()

    # -------------------------------------------------------
    # Save Correlation
    # -------------------------------------------------------

    correlation.to_csv(
        os.path.join(REPORT_FOLDER, "correlation_report.csv")
    )

    # -------------------------------------------------------
    # Business Insights Report
    # -------------------------------------------------------

    report_file = os.path.join(
        REPORT_FOLDER,
        "business_insights.txt"
    )

    with open(report_file, "w") as file:

        file.write("ENTERPRISE CUSTOMER BUSINESS INSIGHTS\n")
        file.write("=" * 50 + "\n\n")

        file.write(f"Total Customers : {total_customers}\n")
        file.write(f"Average Age : {average_age}\n")
        file.write(f"Average Income : {average_income}\n")
        file.write(f"Average Purchase : {average_purchase}\n")
        file.write(f"Average CLV : {average_clv}\n")
        file.write(f"Total Sales : {total_sales}\n")
        file.write(f"Highest Purchase : {highest_purchase}\n")
        file.write(f"Lowest Purchase : {lowest_purchase}\n")

    # -------------------------------------------------------
    # Display
    # -------------------------------------------------------

    print(f"Total Customers      : {total_customers}")
    print(f"Average Age          : {average_age}")
    print(f"Average Income       : ${average_income}")
    print(f"Average Purchase     : ${average_purchase}")
    print(f"Average CLV          : ${average_clv}")
    print(f"Total Sales          : ${total_sales}")

    print("\nMembership Distribution")
    print("-" * 40)
    print(membership_count)

    print("\nTop Customer Cities")
    print("-" * 40)
    print(city_count.head())

    print("\n✓ Correlation Report Saved")

    print("✓ Business Insights Generated")

    print("=" * 70)

    return df