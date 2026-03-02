"""Full-stack industrial monitoring — 5 lines of business logic."""
from predictkit import SensorStream, DataNormalizer, AnomalyDetector, HealthScore, AlertRouter

normalizer = DataNormalizer(schema={
    "temperature": {"field": ["temp_C", "TEMP_CEL", "temperature"], "unit": "celsius"},
    "vibration":   {"field": ["vib_mm_s", "vibration"], "unit": "mm/s"},
})
detector = AnomalyDetector(model="zscore", threshold=80)
health = HealthScore(sensors={
    "temperature": {"weight": 0.4, "ideal": 65, "max": 85},
    "vibration":   {"weight": 0.6, "ideal": 1.5, "max": 4.0},
})
router = AlertRouter(channels={"critical": ["email:manager@factory.com"]})
stream = SensorStream(source="mqtt://factory.local", topics=["machine/+/telemetry"])

def on_data(msg):
    data = normalizer.transform({msg.topic.split("/")[-1]: msg.value})
    score = health.calculate(data)
    if score < 40:
        router.send("critical", f"Machine health critical: {score}/100", data)

stream.subscribe(on_data)
stream.start()
