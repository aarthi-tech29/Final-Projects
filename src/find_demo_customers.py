import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/customer_churn_featured.csv")

# Encode exactly like training
for col in df.select_dtypes(include="object").columns:
    if col == "CustomerID":
        continue
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

X = df.drop(["CustomerID", "Churn"], axis=1)

feature_columns = joblib.load("models/feature_columns.pkl")
scaler = joblib.load("models/scaler.pkl")
model = joblib.load("models/best_model.pkl")

X = X[feature_columns]
X_scaled = scaler.transform(X)

df["Probability"] = model.predict_proba(X_scaled)[:,1]

print("\nTop 5 HIGH RISK customers")
print(df.sort_values("Probability", ascending=False).head(5))

print("\nTop 5 LOW RISK customers")
print(df.sort_values("Probability").head(5))