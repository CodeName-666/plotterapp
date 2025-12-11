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
        z_value: Optional Z-axis value for 3D plots (XYZ charts)
    """
    id: int  # 0-255
    value: float
    timestamp: Optional[float] = None
    z_value: Optional[float] = None

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
        if self.z_value is not None and not isinstance(self.z_value, (int, float)):
            raise ValueError(f"Z-value must be numeric or None, got {type(self.z_value)}")

    def get_dimensions(self) -> int:
        """Get the number of dimensions in this data point.

        Returns:
            2 for 2D data (x, y), 3 for 3D data (x, y, z)
        """
        return 3 if self.z_value is not None else 2

    def is_3d(self) -> bool:
        """Check if this is a 3D data point.

        Returns:
            True if z_value is present, False otherwise
        """
        return self.z_value is not None


__all__ = ["PlotDataPoint"]
