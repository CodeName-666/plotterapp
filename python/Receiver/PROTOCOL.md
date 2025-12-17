# PlotterApp Communication Protocol

**Version 4.0** - Data format specification for embedded-to-PlotterApp communication

## Overview

PlotterApp accepts sensor data in JSON format over various interfaces (Serial, MQTT, WiFi, Telnet). This document specifies the exact format and requirements.

## Data Formats

### Format 1: JSON with Timestamp (Recommended)

```json
{"id":0,"value":123.456789,"timestamp":1.234567}
```

**Fields:**
- `id` (required): Integer, 0-255, identifies the channel/line
- `value` (required): Float, the measurement value (Y-axis)
- `timestamp` (optional): Float, time in **seconds** (not milliseconds!)
- `z` (optional): Float, Z-axis value for 3D charts

**Use when:**
- You need precise timing
- Multiple sensors share the same timestamp
- Timestamp accuracy is critical

**3D Example:**
```json
{"id":0,"value":25.5,"z":10.2,"timestamp":1.234567}
```

### Format 2: JSON without Timestamp

```json
{"id":0,"value":123.456789}
```

**Fields:**
- `id` (required): Integer, 0-255
- `value` (required): Float (Y-axis)
- `z` (optional): Float, Z-axis value for 3D charts

**Auto-generated timestamp:**
- PlotterApp assigns timestamp based on arrival time
- Less accurate for burst data

**Use when:**
- Real-time streaming with regular intervals
- Timestamp precision is not critical

**3D Example:**
```json
{"id":0,"value":25.5,"z":10.2}
```

### Format 3: Plain Number (Legacy)

```
123.456789
```

**Limitations:**
- Only supports single channel (ID=0)
- Auto-generated timestamp
- No multi-sensor support

**Use when:**
- Quick testing
- Single sensor only
- Backward compatibility needed

## Format Requirements

### 1. JSON Structure

✅ **Valid:**
```json
{"id":0,"value":25.5,"timestamp":1.234}
{"id": 0, "value": 25.5, "timestamp": 1.234}
```

❌ **Invalid:**
```json
{'id':0,'value':25.5}              // Single quotes not allowed
{id:0,value:25.5}                  // Keys must be quoted
{"ID":0,"VALUE":25.5}              // Keys must be lowercase
```

### 2. Field Types

| Field | Type | Range | Required |
|-------|------|-------|----------|
| `id` | Integer | 0-255 | Yes |
| `value` | Float | Any | Yes |
| `timestamp` | Float | > 0 | Optional |
| `z` | Float | Any | Optional |

### 3. Newline Termination

Every message **must** end with `\n`:

```cpp
// Correct - embedded C++
Serial.println("{\"id\":0,\"value\":25.5}");
// or
Serial.write("{\"id\":0,\"value\":25.5}\n", 29);
```

### 4. Float Precision

Recommended: **6 decimal places** (`%.6f`)

```cpp
snprintf(buffer, size, "{\"id\":%d,\"value\":%.6f,\"timestamp\":%.6f}\n",
         id, value, timestamp);
```

### 5. Timestamp Units

⚠️ **Critical:** Timestamps must be in **seconds**, not milliseconds!

```cpp
// ❌ WRONG - milliseconds
float timestamp = millis();  // 1234567 ms

// ✅ CORRECT - seconds
float timestamp = millis() / 1000.0f;  // 1234.567 s
```

**Best practice with PlotterLib:**
```cpp
plotter.setStartTime(millis());       // Set once in setup()
plotter.send(0, value, millis());     // Library converts to seconds
```

## Examples

### Single Sensor

```cpp
#include <plotter.h>

Plotter plotter(Serial);

void setup() {
    Serial.begin(115200);
    plotter.setStartTime(millis());
}

void loop() {
    float temperature = readTemperature();
    plotter.send(0, temperature, millis());
    delay(100);
}
```

**Output:**
```json
{"id":0,"value":25.500000,"timestamp":0.100000}
{"id":0,"value":25.520000,"timestamp":0.200000}
{"id":0,"value":25.480000,"timestamp":0.300000}
```

### Multiple Sensors

```cpp
void loop() {
    unsigned long currentTime = millis();

    float temp = readTemperature();
    float humidity = readHumidity();
    float pressure = readPressure();

    // All with same timestamp
    plotter.send(0, temp, currentTime);
    plotter.send(1, humidity, currentTime);
    plotter.send(2, pressure, currentTime);

    delay(100);
}
```

**Output:**
```json
{"id":0,"value":25.500000,"timestamp":1.234567}
{"id":1,"value":60.200000,"timestamp":1.234567}
{"id":2,"value":1013.250000,"timestamp":1.234567}
```

### 3D Data (XYZ Charts)

```cpp
#include <plotter.h>

Plotter plotter(Serial);

void setup() {
    Serial.begin(115200);
    plotter.setStartTime(millis());
}

void loop() {
    float x_pos = readXPosition();
    float y_pos = readYPosition();
    float z_pos = readZPosition();

    // Send 3D data point: Y=y_pos, Z=z_pos, X=timestamp
    plotter.send3D(0, y_pos, z_pos, millis());

    delay(50);
}
```

**Output:**
```json
{"id":0,"value":12.500000,"z":5.200000,"timestamp":0.050000}
{"id":0,"value":12.480000,"z":5.250000,"timestamp":0.100000}
{"id":0,"value":12.460000,"z":5.300000,"timestamp":0.150000}
```

### Without Timestamp

```cpp
void loop() {
    float value = analogRead(A0) * 5.0 / 1023.0;
    plotter.send(0, value);  // No timestamp
    delay(100);
}
```

**Output:**
```json
{"id":0,"value":2.456000}
{"id":0,"value":2.458000}
{"id":0,"value":2.460000}
```

## Python Parsing Implementation

The Python backend parses data in `backend.py::_parse_data_point()`:

```python
def _parse_data_point(self, interface: str, payload: bytes) -> PlotDataPoint | None:
    """Parse received payload into a PlotDataPoint.

    Expected formats:
    1. JSON: {"id": 0-255, "value": float, "timestamp": float (optional), "z": float (optional)}
    2. JSON: {"id": 0-255, "value": float, "z": float (optional)}
    3. JSON: {"id": 0-255, "value": float}
    4. Plain number: float (fallback: id=0, auto-timestamp)
    """
    text = payload.decode("utf-8").strip()

    # Try JSON parsing
    try:
        decoded = json.loads(text)
        data_id = decoded.get("id")
        value = decoded.get("value")
        timestamp = decoded.get("timestamp")
        z_value = decoded.get("z")

        # Validate
        if not 0 <= data_id <= 255:
            return None

        return PlotDataPoint(
            id=data_id,
            value=float(value),
            timestamp=float(timestamp) if timestamp else None,
            z_value=float(z_value) if z_value else None
        )
    except json.JSONDecodeError:
        # Try as plain number
        return PlotDataPoint(id=0, value=float(text), timestamp=None)
```

## Validation Rules

### ID Validation
- Must be integer
- Range: 0-255 (uint8_t)
- Out of range → **rejected**

### Value Validation
- Must be numeric (int or float)
- NaN or Inf → **rejected**
- Converted to float

### Timestamp Validation
- Must be numeric (int or float) or `None`
- Must be positive
- Converted to float
- If omitted → auto-generated

## Error Handling

### Backend Behavior

**Invalid JSON:**
```
>> malformed{json}
<< Warning: cannot parse payload 'malformed{json}'
<< Tries plain number fallback
```

**Missing required field:**
```json
>> {"value":25.5}
<< Warning: missing 'id' field in JSON
<< Rejected
```

**ID out of range:**
```json
>> {"id":300,"value":25.5}
<< Warning: 'id' must be integer 0-255, got 300
<< Rejected
```

**Non-numeric value:**
```json
>> {"id":0,"value":"abc"}
<< Warning: 'value' must be numeric, got <class 'str'>
<< Rejected
```

### Best Practices

1. ✅ **Always validate before sending**
   ```cpp
   if (id >= 0 && id <= 255 && !isnan(value)) {
       plotter.send(id, value, timestamp);
   }
   ```

2. ✅ **Use consistent timestamp source**
   ```cpp
   // ✅ Good - consistent
   plotter.setStartTime(millis());

   // ❌ Bad - mixing sources
   plotter.setStartTime(HAL_GetTick());
   plotter.send(0, value, micros());  // Wrong!
   ```

3. ✅ **Test with PlotterApp first**
   - Send a few test points
   - Verify in PlotterApp UI
   - Check for warning messages

## Interface-Specific Notes

### Serial/USB CDC
- Baud rate: 115200 (recommended)
- Line buffering: Enabled
- Flow control: None

### MQTT
- Topic: User-configurable
- QoS: 0 (recommended for high-frequency data)
- Retained: false

### WiFi/Telnet
- Port: User-configurable
- Protocol: TCP
- Encoding: UTF-8

## Version History

### v4.0 (2025-12-11)
- Documented PlotterLib v4.0 protocol
- Added PlotterStream architecture
- Clarified timestamp units (seconds vs milliseconds)
- Added comprehensive examples

### v3.0
- JSON format standardized
- Added optional timestamp field

### v2.0
- Added multi-channel support via "id" field

### v1.0
- Initial plain number format

## References

- Embedded Library: `embedded/common/plotter.h`
- Protocol Header: `embedded/common/plotter_protocol.h`
- Python Parser: `python/Backend/backend.py::_parse_data_point()`
- Message Class: `python/Receiver/message.py::PlotDataPoint`
