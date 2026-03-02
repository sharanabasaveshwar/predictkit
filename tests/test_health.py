"""Tests for HealthScore."""
from predictkit.health import HealthScore

SENSORS = {
    "temperature": {"weight": 0.3, "ideal": 70, "max": 90},
    "vibration":   {"weight": 0.5, "ideal": 2.0, "max": 5.0},
    "pressure":    {"weight": 0.2, "ideal": 100, "max": 150},
}

def test_perfect_health():
    h = HealthScore(sensors=SENSORS)
    assert h.calculate({"temperature": 70, "vibration": 2.0, "pressure": 100}) == 100.0

def test_poor_health():
    h = HealthScore(sensors=SENSORS)
    assert h.calculate({"temperature": 85, "vibration": 4.2, "pressure": 120}) < 60

def test_explain_keys():
    h = HealthScore(sensors=SENSORS)
    b = h.explain({"temperature": 70, "vibration": 2.0, "pressure": 100})
    assert "overall" in b and "temperature" in b
