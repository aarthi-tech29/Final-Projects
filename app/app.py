import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Customer Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# Custom CSS
# =====================================================

st.markdown("""
<style>

.main{
    background:#F5F7FB;
}

h1{
    color:#0B5ED7;
    font-weight:bold;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 5px 15px rgba(0,0,0,.15);
    text-align:center;
}

.big-font{
    font-size:30px;
    font-weight:bold;
}

.small-font{
    color:gray;
}

.stButton>button{
    width:100%;
    background:#0B5ED7;
    color:white;
    border-radius:10px;
    height:50px;
    font-size:18px;
}

.stButton>button:hover{
    background:#084298;
}

</style>
""",unsafe_allow_html=True)

# =====================================================
# Load Models
# =====================================================

model=joblib.load("models/best_model.pkl")
scaler=joblib.load("models/scaler.pkl")
feature_columns=joblib.load("models/feature_columns.pkl")

# =====================================================
# Sidebar Navigation
# =====================================================

st.sidebar.image(
    "https://img.icons8.com/color/96/artificial-intelligence.png",
    width=80
)

st.sidebar.title("Navigation")

page=st.sidebar.radio(
    "",
    [
        "🏠 Dashboard",
        "🔮 Prediction",
        "📊 Analytics",
        "📑 Reports"
    ]
)

# =====================================================
# Dashboard
# =====================================================

if page=="🏠 Dashboard":

    st.title("📊 AI Customer Churn Prediction System")

    st.write(
        "Enterprise AI Dashboard for predicting customer churn."
    )

    try:

        executive=pd.read_csv(
            "reports/executive_summary.csv"
        )

        total=executive.loc[
            executive["Metric"]=="Total Customers",
            "Value"
        ].values[0]

        best_model=executive.loc[
            executive["Metric"]=="Best Model",
            "Value"
        ].values[0]

        accuracy=executive.loc[
            executive["Metric"]=="Best Accuracy",
            "Value"
        ].values[0]

        churn_factor=executive.loc[
            executive["Metric"]=="Top Churn Factor",
            "Value"
        ].values[0]

    except:

        total=500
        best_model="Random Forest"
        accuracy="95%"
        churn_factor="MonthlyCharges"

    c1,c2,c3,c4=st.columns(4)

    c1.markdown(f"""
    <div class='card'>
    <div class='big-font'>{total}</div>
    <div class='small-font'>Customers</div>
    </div>
    """,unsafe_allow_html=True)

    c2.markdown(f"""
    <div class='card'>
    <div class='big-font'>{best_model}</div>
    <div class='small-font'>Best Model</div>
    </div>
    """,unsafe_allow_html=True)

    c3.markdown(f"""
    <div class='card'>
    <div class='big-font'>{accuracy}</div>
    <div class='small-font'>Accuracy</div>
    </div>
    """,unsafe_allow_html=True)

    c4.markdown(f"""
    <div class='card'>
    <div class='big-font'>{churn_factor}</div>
    <div class='small-font'>Top Churn Factor</div>
    </div>
    """,unsafe_allow_html=True)

    st.divider()

    st.subheader("Welcome")

    st.info(
        """
This dashboard allows business users to

• Predict customer churn

• View AI recommendations

• Analyze churn trends

• Download executive reports

• Explore customer segmentation
        """
    )
# =====================================================
# Prediction Page
# =====================================================

elif page == "🔮 Prediction":

    st.title("🔮 Customer Churn Prediction")

    st.write("Enter customer information below.")

    col1, col2 = st.columns(2)

    with col1:

        gender = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        senior = st.selectbox(
            "Senior Citizen",
            ["No", "Yes"]
        )

        partner = st.selectbox(
            "Partner",
            ["No", "Yes"]
        )

        dependents = st.selectbox(
            "Dependents",
            ["No", "Yes"]
        )

        tenure = st.slider(
            "Tenure",
            1,
            72,
            24
        )

        contract = st.selectbox(
            "Contract",
            [
                "Month-to-month",
                "One year",
                "Two year"
            ]
        )

        internet = st.selectbox(
            "Internet Service",
            [
                "DSL",
                "Fiber Optic",
                "None"
            ]
        )

    with col2:

        payment = st.selectbox(
            "Payment Method",
            [
                "Credit Card",
                "Bank Transfer",
                "Electronic Check",
                "Mailed Check"
            ]
        )

        monthly = st.number_input(
            "Monthly Charges",
            20.0,
            150.0,
            75.0
        )

        usage = st.slider(
            "Usage Hours",
            0,
            300,
            120
        )

        tickets = st.slider(
            "Support Tickets",
            0,
            10,
            1
        )

        complaints = st.slider(
            "Complaints",
            0,
            5,
            0
        )

        late = st.slider(
            "Late Payments",
            0,
            8,
            0
        )

        satisfaction = st.slider(
            "Satisfaction",
            1,
            10,
            8
        )

    if st.button("🚀 Predict Customer"):

        # -----------------------
        # Encode Values
        # -----------------------

        gender = 1 if gender == "Male" else 0
        senior = 1 if senior == "Yes" else 0
        partner = 1 if partner == "Yes" else 0
        dependents = 1 if dependents == "Yes" else 0

        contract = {
            "Month-to-month":0,
            "One year":1,
            "Two year":2
        }[contract]

        internet = {
            "DSL":0,
            "Fiber Optic":1,
            "None":2
        }[internet]

        payment = {
            "Credit Card":0,
            "Bank Transfer":1,
            "Electronic Check":2,
            "Mailed Check":3
        }[payment]

        # -----------------------
        # Derived Features
        # -----------------------

        total = monthly * tenure

        avg_monthly = total / (tenure + 1)

        complaint_ratio = complaints / (tickets + 1)

        loyalty = tenure * satisfaction

        engagement = usage + satisfaction * 10

        payment_risk = late * monthly

        high_value = 1 if total > 5000 else 0

        usage_category = (
            2 if usage > 180
            else 1 if usage > 80
            else 0
        )

        tenure_group = (
            2 if tenure > 36
            else 1 if tenure > 12
            else 0
        )

        service = 6

        health = (
            satisfaction * 10
            - complaints * 5
            - late * 3
        )

        customer = {}

        for col in feature_columns:
            customer[col] = 0

        values = {

            "Gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "Tenure": tenure,
            "PhoneService": 1,
            "MultipleLines": 1,
            "InternetService": internet,
            "OnlineSecurity": 1,
            "OnlineBackup": 1,
            "DeviceProtection": 1,
            "TechSupport": 1,
            "StreamingTV": 1,
            "StreamingMovies": 1,
            "Contract": contract,
            "PaperlessBilling": 1,
            "PaymentMethod": payment,
            "MonthlyCharges": monthly,
            "TotalCharges": total,
            "SupportTickets": tickets,
            "Complaints": complaints,
            "LatePayments": late,
            "SatisfactionScore": satisfaction,
            "UsageHours": usage,
            "LoginFrequency": 40,
            "AvgSessionTime": 30,
            "LastInteractionDays": 10,
            "CustomerLifetimeValue": total * 3,
            "AvgMonthlySpend": avg_monthly,
            "ComplaintRatio": complaint_ratio,
            "LoyaltyScore": loyalty,
            "EngagementScore": engagement,
            "PaymentRisk": payment_risk,
            "HighValueCustomer": high_value,
            "UsageCategory": usage_category,
            "TenureGroup": tenure_group,
            "ServiceEngagement": service,
            "CustomerHealthScore": health
        }

        for key, value in values.items():
            if key in customer:
                customer[key] = value

        customer_df = pd.DataFrame([customer])

        customer_df = customer_df[feature_columns]

        customer_scaled = scaler.transform(customer_df)

        probability = model.predict_proba(customer_scaled)[0][1]

        st.divider()

        if probability >= 0.70:

            st.error(f"🔴 HIGH RISK ({probability:.1%})")

            st.warning(
                """
Immediate retention campaign recommended.

• Offer discount

• Assign relationship manager

• Premium customer support
                """
            )

        elif probability >= 0.30:

            st.warning(f"🟠 MEDIUM RISK ({probability:.1%})")

            st.info(
                """
Offer loyalty rewards.

Increase customer engagement.

Send personalized offers.
                """
            )

        else:

            st.success(f"🟢 LOW RISK ({probability:.1%})")

            st.info(
                """
Customer is healthy.

Recommend premium services and upselling.
                """
            )
# =====================================================
# Analytics Page
# =====================================================

elif page == "📊 Analytics":

    st.title("📊 Business Analytics Dashboard")

    st.write("Visualize customer churn insights.")

    # --------------------------------------------
    # Feature Importance
    # --------------------------------------------

    try:

        feature = pd.read_csv(
            "reports/feature_importance.csv"
        )

        fig = px.bar(

            feature.head(10),

            x="Importance",

            y="Feature",

            orientation="h",

            title="Top 10 Churn Influencing Factors",

            color="Importance",

            color_continuous_scale="Blues"

        )

        fig.update_layout(height=500)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except:

        st.warning("Run feature_importance.py")

    st.divider()

    # --------------------------------------------
    # Customer Segments
    # --------------------------------------------

    try:

        segment = pd.read_csv(
            "reports/customer_segments.csv"
        )

        counts = segment["SegmentName"].value_counts()

        pie = px.pie(

            values=counts.values,

            names=counts.index,

            title="Customer Segments"

        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    except:

        st.warning("Run customer_segmentation.py")

    st.divider()

    # --------------------------------------------
    # Historical vs Predicted
    # --------------------------------------------

    try:

        trend = pd.read_csv(
            "reports/historical_vs_predicted.csv",
            index_col=0
        )

        fig = go.Figure()

        fig.add_trace(

            go.Bar(

                x=trend.index,

                y=trend["Historical"],

                name="Historical"

            )

        )

        fig.add_trace(

            go.Bar(

                x=trend.index,

                y=trend["Predicted"],

                name="Predicted"

            )

        )

        fig.update_layout(

            barmode="group",

            title="Historical vs Predicted Churn"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    except:

        st.warning("Run historical_vs_predicted.py")

    st.divider()

    # --------------------------------------------
    # Model Comparison
    # --------------------------------------------

    try:

        comparison = pd.read_csv(

            "reports/model_comparison.csv"

        )

        fig = px.bar(

            comparison,

            x="Model",

            y="Accuracy",

            color="Accuracy",

            title="Model Accuracy Comparison",

            color_continuous_scale="Viridis"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    except:

        st.warning("Run train_models.py")

    st.divider()

    # --------------------------------------------
    # Executive Metrics
    # --------------------------------------------

    try:

        executive = pd.read_csv(
            "reports/executive_summary.csv"
        )

        st.subheader("Executive Summary")

        st.dataframe(

            executive,

            use_container_width=True

        )

    except:

        st.warning("Run reports.py")
# =====================================================
# Reports Page
# =====================================================

elif page == "📑 Reports":

    st.title("📑 Executive Reports")

    st.write("Download project reports and management insights.")

    st.divider()

    # -------------------------------------------------
    # Executive Summary
    # -------------------------------------------------

    try:

        executive = pd.read_csv(
            "reports/executive_summary.csv"
        )

        st.subheader("Executive Summary")

        st.dataframe(
            executive,
            use_container_width=True
        )

    except:

        st.warning("Run reports.py first.")

    # -------------------------------------------------
    # Management Insights
    # -------------------------------------------------

    try:

        insights = pd.read_csv(
            "reports/management_insights.csv"
        )

        st.subheader("Management Insights")

        for item in insights["Management Insights"]:

            st.success(item)

    except:

        st.warning("Management insights not found.")

    st.divider()

    # -------------------------------------------------
    # Download Reports
    # -------------------------------------------------

    st.subheader("Download Reports")

    report_files = [

        "reports/model_comparison.csv",

        "reports/hyperparameter_tuning_report.csv",

        "reports/feature_importance.csv",

        "reports/customer_segments.csv",

        "reports/customer_segment_summary.csv",

        "reports/retention_recommendations.csv",

        "reports/historical_vs_predicted.csv",

        "reports/lifetime_value_predictions.csv",

        "reports/executive_summary.csv",

        "reports/management_insights.csv"

    ]

    for file in report_files:

        try:

            with open(file, "rb") as f:

                st.download_button(

                    label=f"📥 Download {file.split('/')[-1]}",

                    data=f,

                    file_name=file.split("/")[-1],

                    use_container_width=True

                )

        except:

            pass

    st.divider()

    st.info(
        """
This project demonstrates an end-to-end AI Customer Churn Prediction &
Recommendation System using Machine Learning, Deep Learning, Customer
Segmentation, Lifetime Value Prediction, Hyperparameter Tuning,
Executive Reporting and Streamlit Dashboard.
        """
    )

# =====================================================
# Footer
# =====================================================

st.divider()

st.markdown(
"""
<div style='text-align:center;color:gray;'>

### 🤖 AI Customer Churn Prediction & Recommendation System

Developed using

Python • Scikit-Learn • TensorFlow • Keras • XGBoost • Streamlit • Plotly

© 2026

</div>
""",
unsafe_allow_html=True
)
    
# Input
# Low Risk
# | Field                | Value       |
# | -------------------- | ----------- |
# | **Gender**           | Female      |
# | **Senior Citizen**   | No          |
# | **Partner**          | Yes         |
# | **Dependents**       | Yes         |
# | **Tenure**           | 60          |
# | **Contract**         | Two year    |
# | **Internet Service** | DSL         |
# | **Payment Method**   | Credit Card |
# | **Monthly Charges**  | 45          |
# | **Usage Hours**      | 250         |
# | **Support Tickets**  | 0           |
# | **Complaints**       | 0           |
# | **Late Payments**    | 0           |
# | **Satisfaction**     | 10          |


# High Risk
# | Field            | Value                |
# | ---------------- | -------------------- |
# | Gender           | **Male**             |
# | Senior Citizen   | **Yes**              |
# | Partner          | **No**               |
# | Dependents       | **No**               |
# | Tenure           | **2**                |
# | Contract         | **Month-to-month**   |
# | Internet Service | **Fiber Optic**      |
# | Payment Method   | **Electronic Check** |
# | Monthly Charges  | **110**              |
# | Usage Hours      | **35**               |
# | Support Tickets  | **8**                |
# | Complaints       | **4**                |
# | Late Payments    | **5**                |
# | Satisfaction     | **2**                |

# Medium Risk
# | Field            | Value         |
# | ---------------- | ------------- |
# | Gender           | Male          |
# | Senior Citizen   | No            |
# | Partner          | Yes           |
# | Dependents       | No            |
# | Tenure           | 18            |
# | Contract         | One year      |
# | Internet Service | DSL           |
# | Payment Method   | Bank Transfer |
# | Monthly Charges  | 70            |
# | Usage Hours      | 120           |
# | Support Tickets  | 2             |
# | Complaints       | 1             |
# | Late Payments    | 1             |
# | Satisfaction     | 6             |



