import subprocess
import os
import sys

print("=" * 70)
print("SUPPLY CHAIN ANALYTICS PIPELINE")
print("=" * 70)

scripts = [

    "clean_data.py",

    "transform_data.py",

    "supplier_analysis.py",

    "demand_forecasting.py",

    "inventory_prediction.py",

    "warehouse_analysis.py",

    "transportation_analysis.py",

    "seasonal_analysis.py",

    "procurement_planning.py"

]

current_dir = os.path.dirname(__file__)

for script in scripts:

    print("\n" + "=" * 70)
    print(f"Running {script}")
    print("=" * 70)

    script_path = os.path.join(current_dir, script)

    result = subprocess.run(

        [sys.executable, script_path],

        capture_output=True,

        text=True

    )

    print(result.stdout)

    if result.stderr:

        print(result.stderr)

print("\n" + "=" * 70)
print("PIPELINE COMPLETED")
print("=" * 70)