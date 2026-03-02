# PredictKit 🔧

> **Python + C IoT SDK — reduce 300 lines of boilerplate to 5**

[![PyPI version](https://img.shields.io/pypi/v/predictkit)](https://pypi.org/project/predictkit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

---

## The Problem

Every IoT developer spends 60–70% of project time writing the same boilerplate:
MQTT reconnection logic, sensor data normalisation, anomaly detection pipelines,
alert routing. Over and over, project after project.

## The Solution

```python
from predictkit import SensorStream, AnomalyDetector

stream   = SensorStream(source="mqtt://factory.local", topics=["temp", "vibration"])
detector = AnomalyDetector(model="zscore", threshold=80)
stream.on_anomaly(detector, alert="email:admin@company.com")
stream.start()   # Runs forever — auto-reconnect, buffering, error handling included
```

**That replaces ~300 lines of production code.**

---

## Installation

```bash
pip install predictkit          # zero-dependency core
pip install predictkit[mqtt]    # + MQTT support (paho-mqtt)
pip install predictkit[ml]      # + ML anomaly detection (scikit-learn)
pip install predictkit[all]     # + everything
```

---

## Six Core Modules

| Module | What it saves | Free tier |
|---|---|---|
| `SensorStream` | MQTT ingestion, auto-reconnect, buffering (~500 lines) | MQTT ✅ |
| `DataNormalizer` | Multi-brand sensor unification (~300 lines) | ✅ |
| `AnomalyDetector` | Plug-and-play ML anomaly detection (~400 lines) | Z-score ✅ |
| `HealthScore` | 0–100 machine health score (~250 lines) | ✅ |
| `AlertRouter` | Multi-channel alerts with retry & rate-limiting (~200 lines) | Email ✅ |
| `EdgeCache` | Offline-first SQLite + cloud sync (~350 lines) | ✅ |

**Total: ~2,000 lines of battle-tested code, available as 5-line imports.**

---

## Quick Examples

### Anomaly Detection
```python
from predictkit import AnomalyDetector

detector = AnomalyDetector(model="zscore", threshold=80)
detector.fit(historical_temps)
score = detector.predict(current_temp)   # 0–100
```

### Multi-Brand Sensor Normalisation
```python
from predictkit import DataNormalizer

n = DataNormalizer(schema={
    "temperature": {"field": ["temp_C", "TEMP_CEL", "temperature"], "unit": "celsius"},
})
normalized = n.transform(raw_sensor_data)
```

### Machine Health Score
```python
from predictkit import HealthScore

health = HealthScore(sensors={
    "temperature": {"weight": 0.3, "ideal": 70, "max": 90},
    "vibration":   {"weight": 0.5, "ideal": 2.0, "max": 5.0},
})
score = health.calculate({"temperature": 85, "vibration": 4.2})
# → 42  (poor health)
```

---

## Pro Features

| Feature | Free | Pro (₹4,999 one-time) |
|---|---|---|
| MQTT protocol | ✅ | ✅ |
| OPC-UA / Modbus / HTTP | ❌ | ✅ |
| Z-score anomaly detection | ✅ | ✅ |
| Isolation Forest (ML) | ❌ | ✅ |
| WhatsApp / SMS / Slack alerts | ❌ | ✅ |
| Priority support | ❌ | ✅ |

[**→ Get Pro License**](https://predictkit.io/pro)

---

## License

MIT — see [LICENSE](LICENSE).
