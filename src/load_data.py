import pandas as pd
import json
import os

# Dataset Folder
DATASET_PATH = "datasets"


def load_csv():
    """Load Customer CSV"""
    file_path = os.path.join(DATASET_PATH, "customers_csv.csv")

    df = pd.read_csv(file_path)

    print("\nCSV Dataset Loaded Successfully")
    print(df.head())

    return df


def load_excel():
    """Load Customer Excel"""

    file_path = os.path.join(DATASET_PATH, "customers_excel.xlsx")

    df = pd.read_excel(file_path)

    print("\nExcel Dataset Loaded Successfully")
    print(df.head())

    return df


def load_json():
    """Load Customer JSON"""

    file_path = os.path.join(DATASET_PATH, "customers_json.json")

    with open(file_path, "r") as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    print("\nJSON Dataset Loaded Successfully")
    print(df.head())

    return df


def load_api():
    """
    Simulated API
    Reads api_customers.json
    """

    file_path = os.path.join(DATASET_PATH, "api_customers.json")

    with open(file_path, "r") as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    print("\nAPI Dataset Loaded Successfully")
    print(df.head())

    return df


def load_all_data():
    """
    Load all datasets
    """

    csv_df = load_csv()

    excel_df = load_excel()

    json_df = load_json()

    api_df = load_api()

    return csv_df, excel_df, json_df, api_df


if __name__ == "__main__":

    csv_df, excel_df, json_df, api_df = load_all_data()