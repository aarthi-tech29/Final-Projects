"""
=========================================================
AI CUSTOMER CHURN PREDICTION SYSTEM
Customer Lifetime Value Prediction
=========================================================
"""

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

print("=" * 70)
print("CUSTOMER LIFETIME VALUE PREDICTION")
print("=" * 70)

os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# =====================================================
# Load Dataset
# =====================================================

df = pd.read_csv("data/customer_churn_featured.csv")

# =====================================================
# Encode Categorical Columns
# =====================================================

for col in df.select_dtypes(include="object").columns:

    if col == "CustomerID":
        continue

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col])

# =====================================================
# Features & Target
# =====================================================

X = df.drop(
    ["CustomerID", "CustomerLifetimeValue"],
    axis=1
)

y = df["CustomerLifetimeValue"]

# =====================================================
# Train Test Split
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

# =====================================================
# Train Model
# =====================================================

model = RandomForestRegressor(

    n_estimators=200,

    random_state=42

)

model.fit(

    X_train,

    y_train

)

predictions = model.predict(X_test)

# =====================================================
# Evaluation
# =====================================================

mae = mean_absolute_error(

    y_test,

    predictions

)

mse = mean_squared_error(

    y_test,

    predictions

)

rmse = mse ** 0.5

r2 = r2_score(

    y_test,

    predictions

)

print("\nModel Performance\n")

print("MAE  :", round(mae,2))

print("MSE  :", round(mse,2))

print("RMSE :", round(rmse,2))

print("R² Score :", round(r2,4))

# =====================================================
# Save Model
# =====================================================

joblib.dump(

    model,

    "models/lifetime_value_model.pkl"

)

# =====================================================
# Prediction Report
# =====================================================

results = pd.DataFrame({

    "Actual Lifetime Value": y_test.values,

    "Predicted Lifetime Value": predictions

})

results.to_csv(

    "reports/lifetime_value_predictions.csv",

    index=False

)

# =====================================================
# Visualization
# =====================================================

plt.figure(figsize=(8,6))

plt.scatter(

    y_test,

    predictions

)

plt.xlabel("Actual Lifetime Value")

plt.ylabel("Predicted Lifetime Value")

plt.title("Actual vs Predicted Customer Lifetime Value")

plt.tight_layout()

plt.savefig(

    "reports/lifetime_value_prediction.png"

)

plt.close()

# =====================================================
# Summary
# =====================================================

print("\n")
print("=" * 70)
print("FILES CREATED")
print("=" * 70)

print("✓ models/lifetime_value_model.pkl")

print("✓ reports/lifetime_value_predictions.csv")

print("✓ reports/lifetime_value_prediction.png")

print("\nCustomer Lifetime Value Prediction Completed Successfully")