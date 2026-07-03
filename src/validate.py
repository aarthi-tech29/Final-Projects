import pandas as pd
import re
import os


REPORT_PATH = "reports"


def validate_customer_data(df):
    """
    Validate customer records and generate validation report.
    """

    os.makedirs(REPORT_PATH, exist_ok=True)

    validation_report = []

    # ------------------------------
    # Missing CustomerID
    # ------------------------------
    missing_customerid = df["CustomerID"].isnull().sum()

    validation_report.append({
        "Validation": "Missing CustomerID",
        "Count": missing_customerid
    })

    # ------------------------------
    # Duplicate CustomerID
    # ------------------------------
    duplicate_customerid = df["CustomerID"].duplicated().sum()

    validation_report.append({
        "Validation": "Duplicate CustomerID",
        "Count": duplicate_customerid
    })

    # ------------------------------
    # Missing Name
    # ------------------------------
    missing_name = df["Name"].isnull().sum()

    validation_report.append({
        "Validation": "Missing Name",
        "Count": missing_name
    })

    # ------------------------------
    # Missing Age
    # ------------------------------
    missing_age = df["Age"].isnull().sum()

    validation_report.append({
        "Validation": "Missing Age",
        "Count": missing_age
    })

    # ------------------------------
    # Invalid Email
    # ------------------------------
    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    invalid_email = df["Email"].astype(str).apply(
        lambda x: not bool(re.match(email_pattern, x))
    ).sum()

    validation_report.append({
        "Validation": "Invalid Email",
        "Count": invalid_email
    })

    # ------------------------------
    # Invalid Phone
    # ------------------------------
    invalid_phone = df["Phone"].astype(str).apply(
        lambda x: not (x.isdigit() and len(x) == 10)
    ).sum()

    validation_report.append({
        "Validation": "Invalid Phone",
        "Count": invalid_phone
    })

    # ------------------------------
    # Invalid Age
    # ------------------------------
    invalid_age = ((df["Age"] < 18) | (df["Age"] > 100)).sum()

    validation_report.append({
        "Validation": "Invalid Age",
        "Count": invalid_age
    })

    report_df = pd.DataFrame(validation_report)

    report_df.to_csv(
        os.path.join(REPORT_PATH, "validation_report.csv"),
        index=False
    )

    print("\nValidation Report")
    print(report_df)

    return report_df