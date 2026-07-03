import mysql.connector


def store_to_mysql(df):
    """
    ==========================================================
           STORE CUSTOMER DATA IN MYSQL
    ==========================================================
    """

    print("\n" + "=" * 70)
    print("             STORING DATA INTO MYSQL")
    print("=" * 70)

    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aarthi123",      # <-- Change this
            database="CustomerDB"
        )

        cursor = connection.cursor()

        insert_query = """
        INSERT INTO customers
        (
            CustomerID,
            Name,
            Gender,
            Age,
            City,
            State,
            Country,
            Phone,
            Email,
            Orders,
            TotalPurchase,
            LastPurchase,
            Occupation,
            Income,
            Membership,
            RewardPoints,
            Status,
            CLV,
            PurchaseFrequency,
            Segment
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """

        inserted = 0
        skipped = 0

        for _, row in df.iterrows():

            # Check duplicate CustomerID
            cursor.execute(
                "SELECT CustomerID FROM customers WHERE CustomerID=%s",
                (int(row["CustomerID"]),)
            )

            if cursor.fetchone():
                skipped += 1
                continue

            values = (
                int(row["CustomerID"]),
                row["Name"],
                row["Gender"],
                int(row["Age"]),
                row["City"],
                row["State"],
                row["Country"],
                str(row["Phone"]),
                row["Email"],
                int(row["Orders"]),
                float(row["TotalPurchase"]),
                None if row["LastPurchase"] == "Not Available" else row["LastPurchase"],
                row["Occupation"],
                float(row["Income"]),
                row["Membership"],
                int(row["RewardPoints"]),
                row["Status"],
                float(row["CLV"]),
                float(row["PurchaseFrequency"]),
                row["Segment"]
            )

            cursor.execute(insert_query, values)
            inserted += 1

        connection.commit()

        print(f"\n✓ Records Inserted : {inserted}")
        print(f"✓ Duplicate Records Skipped : {skipped}")

        print("\nData successfully stored in MySQL.")

    except mysql.connector.Error as err:

        print("\nDatabase Error")
        print(err)

    finally:

        if 'cursor' in locals():
            cursor.close()

        if 'connection' in locals() and connection.is_connected():
            connection.close()

    print("=" * 70)