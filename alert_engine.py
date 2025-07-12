import os
import time
import threading
import logging

from event_generator import EventGenerator
from alert_worker import AlertWorker
from queue_manager import create_shared_queue
from utils import setup_logging
from ml_model import AnomalyDetector


class AlertEngine:
    def __init__(self, num_workers=4, run_duration=25):
        self.num_workers = num_workers
        self.run_duration = run_duration
        self.event_queue = create_shared_queue()
        self.stop_event = threading.Event()
        self.workers = []
        self.generator = None
        self.detector = AnomalyDetector()

    def train_model(self):
        from event_generator import generate_event
        normal_data = [generate_event() for _ in range(500)]
        self.detector.fit(normal_data)
        logging.info("Anomaly detector trained.")

    def start(self):
        os.makedirs("logs", exist_ok=True)
        setup_logging()

        print("\n=== Real-Time Alerting System Started ===")
        print(f"Running for {self.run_duration} seconds...\n")
        print("[Sample Output Below]\n")

        logging.info("Training anomaly detector...")
        self.train_model()

        self.generator = EventGenerator(self.event_queue, self.stop_event)

        # Start Event Generator Thread
        generator_thread = threading.Thread(
            target=self.generator.stream_events, daemon=True
        )
        generator_thread.start()

        # Start Worker Threads
        for i in range(self.num_workers):
            worker = AlertWorker(i, self.event_queue, self.stop_event, self.detector)
            worker.start()
            self.workers.append(worker)

        try:
            time.sleep(self.run_duration)
        except KeyboardInterrupt:
            logging.info("Interrupted manually...")

        self.shutdown()

    def shutdown(self):
        logging.info("Shutting down system...")
        self.stop_event.set()
        for worker in self.workers:
            worker.join()
        logging.info("All threads stopped.")
        print("\n=== System Shutdown Completed ===\n")
