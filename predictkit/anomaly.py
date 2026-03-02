"""AnomalyDetector — Plug-and-play ML anomaly detection.

Free models: zscore, moving_average
Pro models:  isolation_forest, lstm_autoencoder
"""
from __future__ import annotations
import statistics
from collections import deque
from typing import List, Optional

class AnomalyDetector:
    """Anomaly detection without requiring ML expertise.

    Example::

        detector = AnomalyDetector(model="zscore", threshold=80)
        detector.fit(historical_data)
        score = detector.predict(95.0)   # returns 0-100
    """

    PRO_MODELS = {"isolation_forest", "lstm_autoencoder"}

    def __init__(self, model: str = "zscore", threshold: float = 80, training_window: int = 1000):
        if model in self.PRO_MODELS:
            raise ImportError(f"Model '{model}' requires PredictKit Pro. Upgrade at https://predictkit.io/pro")
        self.model = model
        self.threshold = threshold
        self._history: deque = deque(maxlen=training_window)
        self._mean: Optional[float] = None
        self._std: Optional[float] = None

    def fit(self, data: List[float]) -> "AnomalyDetector":
        for v in data:
            self._history.append(v)
        self._update_stats()
        return self

    def _update_stats(self):
        if len(self._history) < 2:
            return
        self._mean = statistics.mean(self._history)
        self._std = statistics.stdev(self._history) or 1e-9

    def predict(self, value: float) -> float:
        """Return anomaly score 0-100. Higher = more anomalous."""
        self._history.append(value)
        self._update_stats()
        if self._mean is None:
            return 50.0
        if self.model == "zscore":
            z = abs((value - self._mean) / self._std)
            return min(z / 3.0 * 100, 100)
        if self.model == "moving_average":
            recent = list(self._history)[-10:]
            avg = statistics.mean(recent) if recent else self._mean
            deviation = abs(value - avg)
            max_seen = max(abs(v - self._mean) for v in self._history) or 1
            return min(deviation / max_seen * 100, 100)
        return 50.0
