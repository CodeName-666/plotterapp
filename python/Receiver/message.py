"""Data structures for plot messages."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class PlotDataPoint:
    """Represents a single data point for plotting.

    Attributes:
        id: Unique identifier (0-255) for the measurement line
        value: Y-axis value (measurement value)
        timestamp: Optional X-axis value (time). If None, auto-increment will be used
    """
    id: int  # 0-255
    value: float
    timestamp: Optional[float] = None

    def __post_init__(self):
        """Validate data point after initialization."""
        if not isinstance(self.id, int):
            raise ValueError(f"ID must be an integer, got {type(self.id)}")
        if not 0 <= self.id <= 255:
            raise ValueError(f"ID must be between 0 and 255, got {self.id}")
        if not isinstance(self.value, (int, float)):
            raise ValueError(f"Value must be numeric, got {type(self.value)}")
        if self.timestamp is not None and not isinstance(self.timestamp, (int, float)):
            raise ValueError(f"Timestamp must be numeric or None, got {type(self.timestamp)}")


__all__ = ["PlotDataPoint"]
