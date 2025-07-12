import threading
import logging
from alert_rules import apply_rules
from utils import write_alert_to_csv


class AlertWorker(threading.Thread):
    def __init__(self, worker_id, event_queue, stop_event, ml_detector=None):
        super().__init__(daemon=True)
        self.worker_id = worker_id
        self.event_queue = event_queue
        self.stop_event = stop_event
        self.ml_detector = ml_detector

    def run(self):
        while not self.stop_event.is_set():
            try:
                event = self.event_queue.get(timeout=1)
                alerts = apply_rules(event)

                if self.ml_detector and self.ml_detector.predict(event):
                    alerts.append("ML: Anomaly detected")

                if alerts:
                    for alert in alerts:
                        logging.warning(f"[ALERT][{event['source']}] {alert} @ {event['timestamp']}")
                        write_alert_to_csv(
                            timestamp=event["timestamp"],
                            source=event["source"],
                            alert_type=alert,
                            value=f"{event['cpu']:.2f} | {event['memory']:.2f} | {event['disk_io']:.2f}",
                            message="ML" if "ML" in alert else "Rule-based"
                        )
                else:
                    logging.info(f"[OK][{event['source']}] Event OK @ {event['timestamp']}")

                self.event_queue.task_done()

            except Exception:
                continue
