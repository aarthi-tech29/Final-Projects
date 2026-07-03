"""
=========================================================
AI CUSTOMER CHURN PREDICTION SYSTEM
Train Machine Learning Models
=========================================================
"""

import warnings
warnings.filterwarnings("ignore")

import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from imblearn.over_sampling import SMOTE

print("="*70)
print("AI CUSTOMER CHURN PREDICTION")
print("="*70)

# =====================================================
# Create folders
# =====================================================

os.makedirs("models",exist_ok=True)
os.makedirs("reports",exist_ok=True)

# =====================================================
# Load Dataset
# =====================================================

df=pd.read_csv("data/customer_churn_featured.csv")

print("\nDataset Loaded Successfully")
print(df.shape)

# =====================================================
# Encode Categorical Columns
# =====================================================

label_encoders={}

for column in df.select_dtypes(include="object").columns:

    if column=="CustomerID":
        continue

    encoder=LabelEncoder()

    df[column]=encoder.fit_transform(df[column])

    label_encoders[column]=encoder

# =====================================================
# Features
# =====================================================

X=df.drop(["CustomerID","Churn"],axis=1)

y=df["Churn"]

# Save feature names for future prediction

joblib.dump(
    list(X.columns),
    "models/feature_columns.pkl"
)

# =====================================================
# Split Dataset
# =====================================================

X_train,X_test,y_train,y_test=train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

print("\nTraining Shape :",X_train.shape)
print("Testing Shape  :",X_test.shape)

# =====================================================
# SMOTE
# =====================================================

smote=SMOTE(random_state=42)

X_train,y_train=smote.fit_resample(

    X_train,

    y_train

)

print("\nAfter SMOTE :",X_train.shape)

# =====================================================
# Scaling
# =====================================================

scaler=StandardScaler()

X_train=scaler.fit_transform(X_train)

X_test=scaler.transform(X_test)

joblib.dump(

    scaler,

    "models/scaler.pkl"

)

joblib.dump(

    label_encoders,

    "models/label_encoders.pkl"

)

# =====================================================
# Containers
# =====================================================

results=[]

trained_models={}

# =====================================================
# Helper Function
# =====================================================

def evaluate_model(name,model):

    model.fit(X_train,y_train)

    prediction=model.predict(X_test)

    probability=model.predict_proba(X_test)[:,1]

    accuracy=accuracy_score(y_test,prediction)

    precision=precision_score(y_test,prediction)

    recall=recall_score(y_test,prediction)

    f1=f1_score(y_test,prediction)

    roc=roc_auc_score(y_test,probability)

    print("\n"+"="*60)
    print(name)
    print("="*60)

    print("Accuracy :",round(accuracy,4))
    print("Precision:",round(precision,4))
    print("Recall   :",round(recall,4))
    print("F1 Score :",round(f1,4))
    print("ROC AUC  :",round(roc,4))

    print("\nConfusion Matrix")

    print(confusion_matrix(y_test,prediction))

    print("\nClassification Report")

    print(classification_report(y_test,prediction))

    trained_models[name]=model

    results.append({

        "Model":name,

        "Accuracy":accuracy,

        "Precision":precision,

        "Recall":recall,

        "F1 Score":f1,

        "ROC AUC":roc

    })

# =====================================================
# Logistic Regression
# =====================================================

evaluate_model(

    "Logistic Regression",

    LogisticRegression(

        max_iter=1000,

        random_state=42

    )

)

# =====================================================
# Decision Tree
# =====================================================

evaluate_model(

    "Decision Tree",

    DecisionTreeClassifier(

        random_state=42

    )

)

# =====================================================
# Random Forest
# =====================================================

evaluate_model(

    "Random Forest",

    RandomForestClassifier(

        n_estimators=200,

        random_state=42

    )

)
# =====================================================
# Gradient Boosting
# =====================================================

evaluate_model(

    "Gradient Boosting",

    GradientBoostingClassifier(

        random_state=42

    )

)

# =====================================================
# XGBoost
# =====================================================

evaluate_model(

    "XGBoost",

    XGBClassifier(

        random_state=42,

        eval_metric="logloss"

    )

)

# =====================================================
# TensorFlow Neural Network
# =====================================================

print("\n")
print("="*70)
print("TensorFlow Neural Network")
print("="*70)

import tensorflow as tf

tf.random.set_seed(42)

nn_model = tf.keras.Sequential([

    tf.keras.layers.Input(shape=(X_train.shape[1],)),

    tf.keras.layers.Dense(64, activation="relu"),

    tf.keras.layers.Dropout(0.30),

    tf.keras.layers.Dense(32, activation="relu"),

    tf.keras.layers.Dropout(0.20),

    tf.keras.layers.Dense(16, activation="relu"),

    tf.keras.layers.Dense(1, activation="sigmoid")

])

nn_model.compile(

    optimizer="adam",

    loss="binary_crossentropy",

    metrics=["accuracy"]

)

history = nn_model.fit(

    X_train,

    y_train,

    epochs=20,

    batch_size=32,

    validation_split=0.20,

    verbose=1

)

nn_probability = nn_model.predict(X_test)

nn_prediction = (nn_probability > 0.5).astype(int).flatten()

accuracy = accuracy_score(y_test, nn_prediction)

precision = precision_score(y_test, nn_prediction)

recall = recall_score(y_test, nn_prediction)

f1 = f1_score(y_test, nn_prediction)

roc = roc_auc_score(y_test, nn_probability)

print("\n")
print("="*60)
print("TensorFlow Results")
print("="*60)

print("Accuracy :", round(accuracy,4))
print("Precision:", round(precision,4))
print("Recall   :", round(recall,4))
print("F1 Score :", round(f1,4))
print("ROC AUC  :", round(roc,4))

print("\nConfusion Matrix")

print(confusion_matrix(y_test, nn_prediction))

print("\nClassification Report")

print(classification_report(y_test, nn_prediction))

trained_models["TensorFlow"] = nn_model

results.append({

    "Model":"TensorFlow",

    "Accuracy":accuracy,

    "Precision":precision,

    "Recall":recall,

    "F1 Score":f1,

    "ROC AUC":roc

})

# =====================================================
# Model Comparison
# =====================================================

comparison = pd.DataFrame(results)

comparison = comparison.sort_values(

    by="Accuracy",

    ascending=False

)

print("\n")
print("="*70)
print("MODEL COMPARISON")
print("="*70)

print(comparison)

comparison.to_csv(

    "reports/model_comparison.csv",

    index=False

)

best_model_name = comparison.iloc[0]["Model"]

print("\nBest Model :", best_model_name)

# =====================================================
# Save Models
# =====================================================

print("\nSaving Models...")

joblib.dump(
    trained_models["Logistic Regression"],
    "models/logistic_regression.pkl"
)

joblib.dump(
    trained_models["Decision Tree"],
    "models/decision_tree.pkl"
)

joblib.dump(
    trained_models["Random Forest"],
    "models/random_forest.pkl"
)

joblib.dump(
    trained_models["Gradient Boosting"],
    "models/gradient_boosting.pkl"
)

joblib.dump(
    trained_models["XGBoost"],
    "models/xgboost.pkl"
)

nn_model.save("models/tensorflow_model.keras")

# Save Best Model

if best_model_name != "TensorFlow":

    joblib.dump(

        trained_models[best_model_name],

        "models/best_model.pkl"

    )

print("All Models Saved Successfully")

# =====================================================
# Risk Category Function
# =====================================================

def risk_category(probability):

    if probability < 0.30:
        return "Low Risk"

    elif probability < 0.70:
        return "Medium Risk"

    return "High Risk"

# =====================================================
# Sample Prediction
# =====================================================

print("\n")
print("=" * 70)
print("SAMPLE CUSTOMER PREDICTION")
print("=" * 70)

sample = X_test[0].reshape(1, -1)

if best_model_name == "TensorFlow":

    probability = float(
        nn_model.predict(sample, verbose=0)[0][0]
    )

else:

    probability = trained_models[
        best_model_name
    ].predict_proba(sample)[0][1]

prediction = "Likely To Churn"

if probability < 0.50:

    prediction = "Not Likely To Churn"

print("Probability :", round(probability,4))
print("Prediction  :", prediction)
print("Risk Level  :", risk_category(probability))

# =====================================================
# Final Summary
# =====================================================

print("\n")
print("=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("Dataset Used")

print("✓ customer_churn_featured.csv")

print("\nModels Trained")

for model in comparison["Model"]:

    print("✓", model)

print("\nFiles Saved")

print("✓ scaler.pkl")

print("✓ label_encoders.pkl")

print("✓ feature_columns.pkl")

print("✓ best_model.pkl")

print("✓ tensorflow_model.keras")

print("\nReports")

print("✓ model_comparison.csv")

print("\nRequirements Completed")

print("✓ Requirement 1")
print("✓ Requirement 3")
print("✓ Requirement 4")
print("✓ Requirement 6")
print("✓ Requirement 7")
print("✓ Requirement 13")
print("✓ Requirement 15")

print("\nTrain Models Completed Successfully.")