import csv
import os
from datetime import datetime


class AILogger:

    def __init__(self, log_file="logs/ai_logs.csv"):

        self.log_file = log_file

        os.makedirs(
            os.path.dirname(log_file),
            exist_ok=True
        )

        if not os.path.exists(log_file):

            with open(
                log_file,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Timestamp",
                    "Module",
                    "Input",
                    "Output"
                ])

    def log(self, module, user_input, output):

        with open(
            self.log_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                module,
                str(user_input),
                str(output)
            ])