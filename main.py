import threading
import time
import os
import logging
from event_generator import stream_events, generate_event
from alert_worker import alert_worker
from queue_manager import create_shared_queue
from utils import setup_logging
from ml_model import AnomalyDetector

NUM_WORKERS = 4
RUN_DURATION_SECONDS = 25

def main():
    os.makedirs("logs", exist_ok=True)
    setup_logging()

    print("\n=== Real-Time Alerting System Started ===")
    print(f"Running for {RUN_DURATION_SECONDS} seconds...\n")
    print("[Sample Output Below]\n")

    event_queue = create_shared_queue()
    stop_event = threading.Event()

    # TRAIN THE ML MODEL
    logging.info("Training anomaly detector...")
    detector = AnomalyDetector()

    # Generate synthetic normal data to train
    normal_data = [generate_event() for _ in range(500)]
    detector.fit(normal_data)
    logging.info("Anomaly detector trained.")

    # Start worker threads
    workers = []
    for i in range(NUM_WORKERS):
        t = threading.Thread(
            target=alert_worker, args=(i, event_queue, stop_event, detector), daemon=True
        )
        t.start()
        workers.append(t)

    # Start event generator thread
    generator_thread = threading.Thread(
        target=stream_events, args=(event_queue, stop_event), daemon=True
    )
    generator_thread.start()

    # Let it run for a fixed duration
    try:
        time.sleep(RUN_DURATION_SECONDS)
    except KeyboardInterrupt:
        logging.info("Interrupted manually...")

    # Shutdown sequence
    logging.info("Shutting down system...")
    stop_event.set()
    generator_thread.join()
    for t in workers:
        t.join()

    logging.info("All threads stopped.")
    print("\n=== System Shutdown Completed ===\n")

if __name__ == "__main__":
    main()
