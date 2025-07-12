import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import threading

class AnomalyDetector:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        self.model_lock = threading.Lock()

    def fit(self, training_data):
        """Train Isolation Forest on normal event data."""
        features = self._extract_features(training_data)
        scaled = self.scaler.fit_transform(features)

        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.model.fit(scaled)

    def predict(self, event):
        """Predict if an event is anomalous."""
        if not self.model:
            return False  # Model not trained yet

        features = self._extract_features([event])
        scaled = self.scaler.transform(features)

        with self.model_lock:
            result = self.model.predict(scaled)

        return result[0] == -1  # -1 means anomaly

    def _extract_features(self, events):
        return np.array([[e["cpu"], e["memory"], e["disk_io"]] for e in events])
