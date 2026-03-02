"""SensorStream — Universal sensor data ingestion with auto-reconnect & buffering.

Free tier: MQTT only.
Pro tier: + OPC-UA, Modbus, HTTP REST, WebSocket.
"""
from __future__ import annotations
import time, logging
from dataclasses import dataclass, field
from collections import deque
from typing import Callable, Optional, List

logger = logging.getLogger(__name__)

@dataclass
class SensorMessage:
    topic: str
    value: float | str | dict
    timestamp: float = field(default_factory=time.time)
    raw: dict = field(default_factory=dict)

class SensorStream:
    """Universal sensor stream with auto-reconnect and offline buffering.

    Example::

        stream = SensorStream(
            source="mqtt://factory.local",
            topics=["machine1/temp", "machine1/vibration"],
            reconnect=True,
            buffer_size=5000,
        )
        stream.subscribe(lambda msg: print(msg.value))
        stream.start()
    """

    def __init__(self, source: str, topics: Optional[List[str]] = None,
                 auth: Optional[tuple] = None, reconnect: bool = True,
                 buffer_size: int = 10_000):
        self.source = source
        self.topics = topics or []
        self.auth = auth
        self.reconnect = reconnect
        self._buffer: deque = deque(maxlen=buffer_size)
        self._subscribers: List[Callable] = []
        self._anomaly_handlers: list = []
        self._running = False
        self._driver = self._create_driver()

    def _create_driver(self):
        scheme = self.source.split("://")[0].lower()
        if scheme == "mqtt":
            from predictkit.drivers.mqtt import MQTTDriver
            return MQTTDriver(self.source, self.topics, self.auth)
        if scheme in ("opcua", "modbus", "http", "ws"):
            raise ImportError(f"Protocol '{scheme}' requires PredictKit Pro. Upgrade at https://predictkit.io/pro")
        raise ValueError(f"Unsupported protocol scheme: {scheme}")

    def subscribe(self, callback: Callable[[SensorMessage], None]) -> None:
        self._subscribers.append(callback)

    def on_anomaly(self, detector, alert: Optional[str] = None) -> None:
        self._anomaly_handlers.append((detector, alert))

    def _dispatch(self, msg: SensorMessage) -> None:
        self._buffer.append(msg)
        for cb in self._subscribers:
            try:
                cb(msg)
            except Exception as exc:
                logger.error("Subscriber error: %s", exc)
        for detector, alert_dest in self._anomaly_handlers:
            score = detector.predict(msg.value)
            if score > detector.threshold and alert_dest:
                logger.warning("ANOMALY score=%.1f topic=%s → %s", score, msg.topic, alert_dest)

    def start(self, block: bool = True) -> None:
        """Start streaming. Blocks forever with auto-reconnect."""
        self._running = True
        backoff = 2
        while self._running:
            try:
                self._driver.connect()
                backoff = 2
                self._driver.stream(self._dispatch, lambda: self._running)
            except Exception as exc:
                if not self.reconnect:
                    raise
                logger.warning("Connection lost (%s). Retrying in %ds…", exc, backoff)
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)

    def stop(self) -> None:
        self._running = False
        self._driver.disconnect()
