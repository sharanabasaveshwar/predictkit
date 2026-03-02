"""Anomaly detection on a live MQTT stream."""
from predictkit import SensorStream, AnomalyDetector

detector = AnomalyDetector(model="zscore", threshold=75)
stream = SensorStream(source="mqtt://localhost:1883", topics=["factory/machine1/temp"])
stream.on_anomaly(detector, alert="email:ops@factory.local")
stream.start()
