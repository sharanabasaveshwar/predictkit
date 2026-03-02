"""HealthScore — Single 0-100 machine health score from multiple sensors."""
from __future__ import annotations
from typing import Dict, Any

class HealthScore:
    """Weighted health score from multiple sensor readings.

    Example::

        health = HealthScore(sensors={
            "temperature": {"weight": 0.3, "ideal": 70, "max": 90},
            "vibration":   {"weight": 0.5, "ideal": 2.0, "max": 5.0},
        })
        score = health.calculate({"temperature": 85, "vibration": 4.2})
        # → 42  (poor health)
    """

    def __init__(self, sensors: Dict[str, Dict]):
        self.sensors = sensors
        total = sum(s.get("weight", 1) for s in sensors.values())
        for cfg in sensors.values():
            cfg["_w"] = cfg.get("weight", 1) / total

    def _sensor_score(self, value: float, ideal: float, maximum: float) -> float:
        if maximum <= ideal:
            return 100.0
        deviation = abs(value - ideal)
        normalized = min(deviation / (maximum - ideal), 1.0)
        return max(0.0, 100.0 * (1.0 - normalized))

    def calculate(self, readings: Dict[str, float]) -> float:
        total = 0.0
        for sensor, cfg in self.sensors.items():
            value = readings.get(sensor)
            if value is None:
                continue
            total += self._sensor_score(value, cfg.get("ideal", 0), cfg.get("max", 1)) * cfg["_w"]
        return round(total, 1)

    def explain(self, readings: Dict[str, float]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for sensor, cfg in self.sensors.items():
            value = readings.get(sensor)
            if value is None:
                result[sensor] = {"score": None, "reason": "no reading"}
                continue
            score = self._sensor_score(value, cfg.get("ideal", 0), cfg.get("max", 1))
            deviation = value - cfg.get("ideal", 0)
            result[sensor] = {
                "score": round(score, 1),
                "reason": f"{abs(deviation):.1f} {'above' if deviation > 0 else 'below'} ideal",
            }
        result["overall"] = self.calculate(readings)
        return result
