import os
import random
import pandas as pd

random.seed(42)

NUM_CUSTOMERS = 500

genders = ["Male", "Female"]
yes_no = ["Yes", "No"]
internet_services = ["DSL", "Fiber Optic", "None"]
contracts = ["Month-to-month", "One year", "Two year"]
payments = [
    "Credit Card",
    "Bank Transfer",
    "Electronic Check",
    "Mailed Check"
]

records = []

for i in range(1, NUM_CUSTOMERS + 1):

    customer_id = f"CUST{i:04d}"

    gender = random.choice(genders)

    age = random.randint(18, 75)

    senior = 1 if age >= 60 else 0

    partner = random.choice(yes_no)

    dependents = random.choice(yes_no)

    tenure = random.randint(1, 72)

    phone_service = "Yes"

    multiple_lines = random.choice(yes_no)

    internet = random.choice(internet_services)

    online_security = random.choice(yes_no)

    online_backup = random.choice(yes_no)

    device_protection = random.choice(yes_no)

    tech_support = random.choice(yes_no)

    streaming_tv = random.choice(yes_no)

    streaming_movies = random.choice(yes_no)

    contract = random.choices(
        contracts,
        weights=[55, 25, 20]
    )[0]

    paperless = random.choice(yes_no)

    payment_method = random.choice(payments)

    monthly_charges = round(random.uniform(20, 120), 2)

    total_charges = round(monthly_charges * tenure + random.uniform(0, 100), 2)

    support_tickets = random.randint(0, 10)

    complaints = random.randint(0, 5)

    late_payments = random.randint(0, 8)

    satisfaction = random.randint(1, 10)

    usage_hours = random.randint(10, 300)

    login_frequency = random.randint(1, 120)

    avg_session = random.randint(5, 180)

    last_interaction = random.randint(0, 120)

    lifetime_value = round(random.uniform(500, 15000), 2)

    # -------- Churn Logic --------

    score = 0

    if contract == "Month-to-month":
        score += 4

    if tenure < 12:
        score += 3

    if complaints >= 3:
        score += 3

    if support_tickets >= 6:
        score += 2

    if late_payments >= 4:
        score += 2

    if satisfaction <= 4:
        score += 4

    if last_interaction > 60:
        score += 2

    if usage_hours < 60:
        score += 2

    if monthly_charges > 90:
        score += 1

    churn = "Yes" if score >= 9 else "No"

    records.append([
        customer_id,
        gender,
        senior,
        partner,
        dependents,
        tenure,
        phone_service,
        multiple_lines,
        internet,
        online_security,
        online_backup,
        device_protection,
        tech_support,
        streaming_tv,
        streaming_movies,
        contract,
        paperless,
        payment_method,
        monthly_charges,
        total_charges,
        support_tickets,
        complaints,
        late_payments,
        satisfaction,
        usage_hours,
        login_frequency,
        avg_session,
        last_interaction,
        lifetime_value,
        churn
    ])

columns = [
    "CustomerID",
    "Gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "Tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "SupportTickets",
    "Complaints",
    "LatePayments",
    "SatisfactionScore",
    "UsageHours",
    "LoginFrequency",
    "AvgSessionTime",
    "LastInteractionDays",
    "CustomerLifetimeValue",
    "Churn"
]

df = pd.DataFrame(records, columns=columns)

os.makedirs("data", exist_ok=True)

output_path = os.path.join("data", "customer_churn_dataset.csv")

df.to_csv(output_path, index=False)

print("=" * 60)
print("Customer Churn Dataset Generated Successfully")
print("=" * 60)
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")
print(f"Saved   : {output_path}")
print("=" * 60)

print(df.head())