"""
PredictKit — Python IoT SDK
Reduce 300+ lines of IoT boilerplate to 5 lines of production-ready code.

Example::

    from predictkit import SensorStream, AnomalyDetector
    stream   = SensorStream(source="mqtt://factory.local", topics=["temp"])
    detector = AnomalyDetector(model="zscore", threshold=80)
    stream.on_anomaly(detector, alert="email:admin@co.com")
    stream.start()
"""

__version__ = "0.2.0"
__author__ = "PredictKit Contributors"
__license__ = "MIT"

from predictkit.stream import SensorStream
from predictkit.normalizer import DataNormalizer
from predictkit.anomaly import AnomalyDetector
from predictkit.health import HealthScore
from predictkit.alerts import AlertRouter
from predictkit.cache import EdgeCache

__all__ = ["SensorStream", "DataNormalizer", "AnomalyDetector", "HealthScore", "AlertRouter", "EdgeCache"]
