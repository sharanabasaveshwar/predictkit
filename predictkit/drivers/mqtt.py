"""MQTT driver using Eclipse Paho (open-source, free tier)."""
from __future__ import annotations
import logging, time
from typing import Callable, List, Optional

logger = logging.getLogger(__name__)

class MQTTDriver:
    def __init__(self, source: str, topics: List[str], auth: Optional[tuple]):
        host_part = source.replace("mqtt://", "")
        parts = host_part.split(":")
        self.host = parts[0]
        self.port = int(parts[1]) if len(parts) > 1 else 1883
        self.topics = topics
        self.auth = auth
        self._client = None

    def connect(self):
        try:
            import paho.mqtt.client as mqtt
        except ImportError:
            raise ImportError("pip install predictkit[mqtt]  —  paho-mqtt required")
        self._client = mqtt.Client()
        if self.auth:
            self._client.username_pw_set(*self.auth)
        self._client.connect(self.host, self.port, keepalive=60)
        for topic in self.topics:
            self._client.subscribe(topic)
        logger.info("MQTT connected to %s:%s topics=%s", self.host, self.port, self.topics)

    def stream(self, dispatch_cb: Callable, running_fn: Callable) -> None:
        from predictkit.stream import SensorMessage
        def on_message(client, userdata, msg):
            try:
                value = float(msg.payload.decode())
            except (ValueError, UnicodeDecodeError):
                value = msg.payload.decode(errors="replace")
            dispatch_cb(SensorMessage(topic=msg.topic, value=value))
        self._client.on_message = on_message
        self._client.loop_start()
        while running_fn():
            time.sleep(0.1)
        self._client.loop_stop()

    def disconnect(self):
        if self._client:
            self._client.disconnect()
