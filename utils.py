import logging
import csv
from threading import Lock
import os

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/alerts.log"),
            logging.StreamHandler()
        ]
    )




alert_file_path = "logs/alert_data.csv"
alert_file_lock = Lock()

def write_alert_to_csv(timestamp, source, alert_type, value, message):
    with alert_file_lock:
        file_exists = os.path.exists(alert_file_path)
        with open(alert_file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["timestamp", "source", "type", "value", "message"])
            writer.writerow([timestamp, source, alert_type, value, message])
