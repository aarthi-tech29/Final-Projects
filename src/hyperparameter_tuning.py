"""
=========================================================
AI CUSTOMER CHURN PREDICTION SYSTEM
Hyperparameter Tuning
=========================================================
"""

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score

from imblearn.over_sampling import SMOTE

print("=" * 70)
print("HYPERPARAMETER TUNING")
print("=" * 70)

os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# =====================================================
# Load Dataset
# =====================================================

df = pd.read_csv("data/customer_churn_featured.csv")

label_encoders = {}

for col in df.select_dtypes(include="object").columns:

    if col == "CustomerID":
        continue

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col])

    label_encoders[col] = encoder

X = df.drop(["CustomerID", "Churn"], axis=1)

y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

smote = SMOTE(random_state=42)

X_train, y_train = smote.fit_resample(

    X_train,

    y_train

)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

results = []

# =====================================================
# Random Forest
# =====================================================

print("\nTuning Random Forest...")

rf = RandomForestClassifier(random_state=42)

rf_parameters = {

    "n_estimators":[100,200,300],

    "max_depth":[5,10,None],

    "min_samples_split":[2,5]

}

rf_grid = GridSearchCV(

    rf,

    rf_parameters,

    cv=5,

    scoring="accuracy",

    n_jobs=-1

)

rf_grid.fit(X_train,y_train)

rf_best = rf_grid.best_estimator_

rf_accuracy = accuracy_score(

    y_test,

    rf_best.predict(X_test)

)

joblib.dump(

    rf_best,

    "models/random_forest_tuned.pkl"

)

results.append({

    "Model":"Random Forest",

    "Accuracy":rf_accuracy,

    "Best Parameters":str(rf_grid.best_params_)

})

print(rf_grid.best_params_)

# =====================================================
# Gradient Boosting
# =====================================================

print("\nTuning Gradient Boosting...")

gb = GradientBoostingClassifier(random_state=42)

gb_parameters = {

    "n_estimators":[100,150],

    "learning_rate":[0.01,0.1],

    "max_depth":[3,5]

}

gb_grid = GridSearchCV(

    gb,

    gb_parameters,

    cv=5,

    scoring="accuracy",

    n_jobs=-1

)

gb_grid.fit(X_train,y_train)

gb_best = gb_grid.best_estimator_

gb_accuracy = accuracy_score(

    y_test,

    gb_best.predict(X_test)

)

joblib.dump(

    gb_best,

    "models/gradient_boosting_tuned.pkl"

)

results.append({

    "Model":"Gradient Boosting",

    "Accuracy":gb_accuracy,

    "Best Parameters":str(gb_grid.best_params_)

})

print(gb_grid.best_params_)

# =====================================================
# XGBoost
# =====================================================

print("\nTuning XGBoost...")

xgb = XGBClassifier(

    random_state=42,

    eval_metric="logloss"

)

xgb_parameters = {

    "n_estimators":[100,200],

    "learning_rate":[0.05,0.10],

    "max_depth":[3,5]

}

xgb_grid = GridSearchCV(

    xgb,

    xgb_parameters,

    cv=5,

    scoring="accuracy",

    n_jobs=-1

)

xgb_grid.fit(X_train,y_train)

xgb_best = xgb_grid.best_estimator_

xgb_accuracy = accuracy_score(

    y_test,

    xgb_best.predict(X_test)

)

joblib.dump(

    xgb_best,

    "models/xgboost_tuned.pkl"

)

results.append({

    "Model":"XGBoost",

    "Accuracy":xgb_accuracy,

    "Best Parameters":str(xgb_grid.best_params_)

})

print(xgb_grid.best_params_)

# =====================================================
# Save Report
# =====================================================

report = pd.DataFrame(results)

report.to_csv(

    "reports/hyperparameter_tuning_report.csv",

    index=False

)

print("\n")
print("=" * 70)
print("HYPERPARAMETER TUNING COMPLETED")
print("=" * 70)

print(report)