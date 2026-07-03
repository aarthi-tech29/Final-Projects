"""
=========================================================
AI CUSTOMER CHURN PREDICTION SYSTEM
Data Preprocessing
=========================================================
"""

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE


def load_dataset(filepath):
    """Load customer dataset."""
    print("=" * 60)
    print("Loading Dataset...")
    print("=" * 60)

    df = pd.read_csv(filepath)

    print(f"Dataset Shape : {df.shape}")
    print(df.head())

    return df


def clean_dataset(df):
    """Clean dataset."""

    print("\nCleaning Dataset...")

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nDuplicate Rows :", df.duplicated().sum())

    df = df.drop_duplicates()

    return df


def encode_features(df):
    """Encode categorical features."""

    print("\nEncoding Categorical Columns...")

    label_encoders = {}

    categorical_columns = df.select_dtypes(include="object").columns

    for col in categorical_columns:

        if col == "CustomerID":
            continue

        encoder = LabelEncoder()

        df[col] = encoder.fit_transform(df[col])

        label_encoders[col] = encoder

    return df, label_encoders


def split_dataset(df):

    X = df.drop("Churn", axis=1)

    if "CustomerID" in X.columns:
        X = X.drop("CustomerID", axis=1)

    y = df["Churn"]

    return train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )


def scale_features(X_train, X_test):

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)

    X_test = scaler.transform(X_test)

    return X_train, X_test, scaler


def balance_dataset(X_train, y_train):

    print("\nApplying SMOTE...")

    smote = SMOTE(random_state=42)

    X_train, y_train = smote.fit_resample(
        X_train,
        y_train
    )

    return X_train, y_train


def save_files(
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
        encoders
):

    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    train = pd.DataFrame(X_train)
    train["Churn"] = y_train

    test = pd.DataFrame(X_test)
    test["Churn"] = y_test.values

    train.to_csv("data/train.csv", index=False)
    test.to_csv("data/test.csv", index=False)

    joblib.dump(
        scaler,
        "models/scaler.pkl"
    )

    joblib.dump(
        encoders,
        "models/label_encoders.pkl"
    )

    print("\nFiles Saved Successfully")


def main():

    dataset_path = "data/customer_churn_dataset.csv"

    df = load_dataset(dataset_path)

    df = clean_dataset(df)

    df, encoders = encode_features(df)

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = split_dataset(df)

    (
        X_train,
        X_test,
        scaler
    ) = scale_features(
        X_train,
        X_test
    )

    (
        X_train,
        y_train
    ) = balance_dataset(
        X_train,
        y_train
    )

    save_files(
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
        encoders
    )

    print("\nPreprocessing Completed Successfully")


if __name__ == "__main__":
    main()