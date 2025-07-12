import random
import time
from datetime import datetime


def generate_event():
    base_cpu = random.gauss(50, 10)
    base_memory = random.gauss(30, 5)
    base_latency = random.gauss(100, 20)

    # Inject anomaly with 5% probability
    if random.random() < 0.05:
        base_cpu += random.uniform(50, 100)       # spike
        base_memory += random.uniform(40, 80)
        base_latency += random.uniform(300, 600)

    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "source": f"sensor-{random.randint(1,5)}",
        "cpu": round(base_cpu, 2),
        "memory": round(base_memory, 2),
        "latency": round(base_latency, 2),
    }


def stream_events(event_queue, stop_event, interval=0.1):
    """Continuously puts simulated events into the shared queue."""
    while not stop_event.is_set():
        event = generate_event()
        event_queue.put(event)
        time.sleep(interval)
