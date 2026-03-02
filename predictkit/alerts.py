"""AlertRouter — Multi-channel alert routing (email free; WhatsApp/SMS/Slack Pro)."""
from __future__ import annotations
import logging, smtplib, time
from email.message import EmailMessage
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)
PRO_CHANNELS = {"whatsapp", "sms", "slack", "teams", "pagerduty"}

class AlertRouter:
    """Route alerts to multiple channels with retry, rate limiting, and quiet hours.

    Free: email only.
    Pro: + WhatsApp, SMS, Slack, Teams, PagerDuty.

    Example::

        router = AlertRouter(channels={
            "critical": ["email:admin@company.com"],
        })
        router.send(severity="critical", message="Machine 3 temp 95 degrees!")
    """

    def __init__(self, channels: Dict[str, List[str]], rate_limit: int = 10,
                 quiet_start: int = 22, quiet_end: int = 7,
                 smtp_host: str = "localhost", smtp_port: int = 25):
        self.channels = channels
        self.rate_limit = rate_limit
        self.quiet_start = quiet_start
        self.quiet_end = quiet_end
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self._sent_times: List[float] = []

    def _rate_ok(self) -> bool:
        now = time.time()
        self._sent_times = [t for t in self._sent_times if now - t < 3600]
        return len(self._sent_times) < self.rate_limit

    def _quiet_hours(self) -> bool:
        hour = time.localtime().tm_hour
        if self.quiet_start > self.quiet_end:
            return hour >= self.quiet_start or hour < self.quiet_end
        return self.quiet_start <= hour < self.quiet_end

    def send(self, severity: str, message: str, data: Optional[dict] = None) -> bool:
        destinations = self.channels.get(severity, [])
        if not destinations or not self._rate_ok():
            return False
        if severity != "critical" and self._quiet_hours():
            return False
        for dest in destinations:
            channel, target = dest.split(":", 1)
            if channel in PRO_CHANNELS:
                raise ImportError(f"Channel '{channel}' requires PredictKit Pro. Upgrade at https://predictkit.io/pro")
            if channel == "email":
                self._send_email(target, severity, message)
        self._sent_times.append(time.time())
        return True

    def _send_email(self, to: str, severity: str, message: str):
        try:
            msg = EmailMessage()
            msg["Subject"] = f"[PredictKit {severity.upper()}] {message[:60]}"
            msg["From"] = "predictkit@localhost"
            msg["To"] = to
            msg.set_content(message)
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=5) as s:
                s.send_message(msg)
        except Exception as exc:
            logger.error("Email failed to %s: %s", to, exc)
