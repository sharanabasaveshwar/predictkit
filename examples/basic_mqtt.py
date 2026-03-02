"""Hello World: MQTT stream with PredictKit."""
from predictkit import SensorStream

stream = SensorStream(
    source="mqtt://localhost:1883",
    topics=["factory/machine1/temp"],
)
stream.subscribe(lambda msg: print(f"[{msg.topic}] {msg.value}"))
print("Connecting to MQTT broker… (Ctrl+C to stop)")
stream.start()
