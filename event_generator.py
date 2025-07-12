import time
import random
from datetime import datetime


def generate_event():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "source": random.choice(["Server-A", "Server-B", "Server-C"]),
        "cpu": random.uniform(10, 100),
        "memory": random.uniform(10, 100),
        "disk_io": random.uniform(10, 100),
        "latency": random.uniform(10, 500),
    }


class EventGenerator:
    def __init__(self, event_queue, stop_event, interval=0.5):
        self.event_queue = event_queue
        self.stop_event = stop_event
        self.interval = interval

    def stream_events(self):
        while not self.stop_event.is_set():
            event = generate_event()
            self.event_queue.put(event)
            time.sleep(self.interval)
