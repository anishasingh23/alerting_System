import threading
import logging
from alert_rules import apply_rules
from utils import write_alert_to_csv

# NEW: Pass in ml_detector
def alert_worker(worker_id, event_queue, stop_event, ml_detector=None):
    while not stop_event.is_set():
        try:
            event = event_queue.get(timeout=1)

            alerts = apply_rules(event)

            # Use ML detector if provided
            if ml_detector and ml_detector.predict(event):
                alerts.append("🔍 ML: Anomaly detected")

            if alerts:
                for alert in alerts:
                    msg = f"[ALERT][{event['source']}] {alert} @ {event['timestamp']}"
                    logging.warning(msg)

                    # Determine alert type and value
                    if "CPU" in alert:
                        alert_type = "CPU"
                        value = event["cpu"]
                    elif "Memory" in alert:
                        alert_type = "Memory"
                        value = event["memory"]
                    elif "Disk" in alert:
                        alert_type = "Disk I/O"
                        value = event["disk"]
                    elif "ML" in alert:
                        alert_type = "ML"
                        value = "N/A"
                    else:
                        alert_type = "Other"
                        value = "N/A"

                    # Save to CSV
                    write_alert_to_csv(
                        timestamp=event["timestamp"],
                        source=event["source"],
                        alert_type=alert_type,
                        value=value,
                        message=alert
                    )
            else:
                logging.info(f"[OK][{event['source']}] Event OK @ {event['timestamp']}")

            event_queue.task_done()

        except Exception:
            continue
