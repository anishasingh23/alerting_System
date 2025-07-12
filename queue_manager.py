from queue import Queue

def create_shared_queue():
    """Creates a thread-safe queue for event processing."""
    return Queue(maxsize=1000)
