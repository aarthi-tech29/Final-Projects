import os
import glob
import pandas as pd

print("=" * 70)
print("SUPPLY CHAIN ANALYTICS DASHBOARD")
print("=" * 70)

report_folder = "datasets/reports"

reports = glob.glob(os.path.join(report_folder, "*"))

print("\nGenerated Reports\n")

for report in reports:

    print(os.path.basename(report))

print("\n" + "=" * 70)

print("Daily Operational Summary")

print("=" * 70)

for report in reports:

    try:

        csv_files = glob.glob(os.path.join(report, "*.csv"))

        if len(csv_files) > 0:

            df = pd.read_csv(csv_files[0])

            print(f"{os.path.basename(report):30} Rows : {len(df)}")

    except:

        pass

print("\n" + "=" * 70)

print("Analytics Reports Exported Successfully")

print("=" * 70)