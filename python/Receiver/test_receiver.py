"""Synthetic test receiver that generates a sine wave for the chart."""

from __future__ import annotations

import math
from typing import Any, Dict, Optional

from PySide6.QtCore import QTimer

from Logger import logger

from .receiver import Receiver


class TestReceiver(Receiver):
    """Produces periodic sine samples to exercise the chart pipeline."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(receiver_thread=None)
        self._settings: Dict[str, Any] = defaults.copy() if defaults else {}
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._t = 0.0
        if self._settings:
            super().config(self._settings)

    def _on_config_updated(self) -> None:
        # Restart timer with new interval when config changes.
        interval = int(self._settings.get("sample_ms", 50))
        if interval < 5:
            interval = 5
        self._timer.setInterval(interval)

    def config(self, config: Dict[str, Any]) -> None:
        self._settings.update(config or {})
        super().config(self._settings)

    def open_connection(self) -> bool:
        self._t = 0.0
        self._set_connected(True)
        self._timer.start()
        logger.log_info("TestReceiver started sine generator")
        return True

    def close_connection(self) -> None:
        self._timer.stop()
        self._set_connected(False)
        logger.log_info("TestReceiver stopped")

    def settings_valid(self) -> bool:
        return True

    def _tick(self) -> None:
        # Simple sine y(t) = A * sin(2*pi*f*t)
        amp = float(self._settings.get("amplitude", 1.0))
        freq = float(self._settings.get("frequency", 1.0))
        dt = self._timer.interval() / 1000.0
        self._t += dt
        y = amp * math.sin(2 * math.pi * freq * self._t)
        payload = f"{y}".encode("utf-8")
        self.new_data.emit(payload)


__all__ = ["TestReceiver"]
