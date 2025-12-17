# PlotterLib 3D Protocol Extension

**Version:** 4.1
**Date:** 2025-12-11

## Overview

PlotterLib now supports 3D data transmission for XYZ surface and scatter plots. This document describes the new API and protocol changes.

## New API Functions

### send3D() - Three Overloads

#### 1. Automatic Timestamp (Recommended)

```cpp
void send3D(uint8_t channelId, float yValue, float zValue, uint32_t currentTimeMs);
```

**Example:**
```cpp
plotter.send3D(0, temperature, pressure, millis());
```

**Output:**
```json
{"id":0,"value":25.5,"z":1013.2,"timestamp":1.234567}
```

#### 2. Explicit Timestamp

```cpp
void send3D(uint8_t channelId, float yValue, float zValue, float timestamp);
```

**Example:**
```cpp
plotter.send3D(0, temperature, pressure, 1.234);
```

**Output:**
```json
{"id":0,"value":25.5,"z":1013.2,"timestamp":1.234}
```

#### 3. No Timestamp

```cpp
void send3D(uint8_t channelId, float yValue, float zValue);
```

**Example:**
```cpp
plotter.send3D(0, temperature, pressure);
```

**Output:**
```json
{"id":0,"value":25.5,"z":1013.2}
```

## Protocol Format

### JSON Structure

```json
{
  "id": 0,           // Channel ID (0-255)
  "value": 25.5,     // Y-axis value
  "z": 1013.2,       // Z-axis value (NEW)
  "timestamp": 1.23  // X-axis value (optional, in seconds)
}
```

### Field Descriptions

| Field | Type | Range | Required | Description |
|-------|------|-------|----------|-------------|
| `id` | Integer | 0-255 | Yes | Channel/line identifier |
| `value` | Float | Any | Yes | Y-axis measurement |
| `z` | Float | Any | Optional | Z-axis value for 3D charts |
| `timestamp` | Float | > 0 | Optional | X-axis time in seconds |

## Complete Example

```cpp
#include <plotter.h>

Plotter plotter(Serial);

void setup() {
    Serial.begin(115200);
    plotter.setStartTime(millis());
}

void loop() {
    // Read 3D sensor data
    float temperature = readTemperature();  // Y-axis
    float pressure = readPressure();        // Z-axis
    unsigned long currentTime = millis();   // X-axis (auto-converted to seconds)

    // Send as 3D point
    plotter.send3D(0, temperature, pressure, currentTime);

    delay(100);
}
```

**Serial Output:**
```json
{"id":0,"value":25.500000,"z":1013.250000,"timestamp":0.100000}
{"id":0,"value":25.520000,"z":1013.280000,"timestamp":0.200000}
{"id":0,"value":25.480000,"z":1013.200000,"timestamp":0.300000}
```

## Memory Impact

- Buffer size increased from 64 to 80 bytes
- Maximum message length: ~70 characters
- RAM overhead: +16 bytes per Plotter instance

## Backward Compatibility

All existing `send()` functions remain unchanged:

```cpp
plotter.send(0, value, millis());     // 2D with timestamp
plotter.send(0, value, 1.234);        // 2D with explicit timestamp
plotter.send(0, value);               // 2D without timestamp
```

## Use Cases

### 3D Surface Plot
Track temperature variation over time and position:
```cpp
plotter.send3D(0, temperature, position, millis());
```

### 3D Scatter Plot
Visualize sensor fusion data:
```cpp
float accelX = readAccelX();
float accelY = readAccelY();
float accelZ = readAccelZ();

plotter.send3D(0, accelX, accelY, millis());  // XY plane
plotter.send3D(1, accelX, accelZ, millis());  // XZ plane
plotter.send3D(2, accelY, accelZ, millis());  // YZ plane
```

### Multi-Axis Robot Tracking
```cpp
float x = getXPosition();
float y = getYPosition();
float z = getZPosition();

plotter.send3D(0, y, z, millis());  // 3D path visualization
```

## PlotterApp Support

The PlotterApp Python backend automatically detects 3D data points:

```python
# PlotDataPoint now includes z_value
point = PlotDataPoint(
    id=0,
    value=25.5,
    z_value=1013.2,  # NEW
    timestamp=1.234
)

# Check if 3D
if point.is_3d():
    print(f"3D point: ({point.timestamp}, {point.value}, {point.z_value})")
```

## Chart Type Compatibility

| Chart Type | Dimensions | Protocol |
|------------|-----------|----------|
| XY Line | 2D | `send()` |
| XY Scatter | 2D | `send()` |
| XYZ Surface | 3D | `send3D()` |
| XYZ Scatter | 3D | `send3D()` |

## References

- Header: `embedded/common/plotter.h`
- Implementation: `embedded/common/plotter.cpp`
- Python Parser: `python/Backend/backend.py::_parse_data_point()`
- Data Structure: `python/Receiver/message.py::PlotDataPoint`
- Full Protocol: `python/Receiver/PROTOCOL.md`
