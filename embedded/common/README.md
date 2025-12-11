# PlotterLib - Embedded Sensor Data Streaming Library

**Version 4.0** - Lightweight C++ library for streaming sensor data to PlotterApp

## Features

✅ **Extremely Lightweight**
- Only ~125 lines of code (excluding comments)
- 74-78 bytes RAM per instance
- 2-3 KB Flash/ROM
- No external dependencies (no JSON libraries required)

✅ **Platform Support**
- Arduino (Uno, Nano, Mega, etc.)
- ESP32 (all variants)
- STM32 (all families)
- Any platform with C++11 compiler

✅ **Flexible Architecture**
- Abstract `PlotterStream` base class
- Easy to add new communication interfaces
- Supports Serial, WiFi, MQTT, USB CDC, UART, etc.

✅ **Simple API**
```cpp
Plotter plotter(Serial);
plotter.setStartTime(millis());
plotter.send(channelId, value, timestamp);
```

## Installation

### PlatformIO (Recommended)

Add to your `platformio.ini`:
```ini
lib_deps =
    PlotterLib=symlink://path/to/common
```

Or install from local folder:
```bash
cd your_project
pio lib install file://path/to/PlotterApp/embedded/common
```

### Arduino IDE

1. Copy the `common` folder to your Arduino libraries folder:
   - Windows: `Documents/Arduino/libraries/PlotterLib`
   - macOS: `~/Documents/Arduino/libraries/PlotterLib`
   - Linux: `~/Arduino/libraries/PlotterLib`

2. Restart Arduino IDE

3. Include in your sketch:
```cpp
#include <plotter.h>
```

## Quick Start

### Arduino/ESP32 (Serial)

```cpp
#include <Arduino.h>
#include <plotter.h>

Plotter plotter(Serial);

void setup() {
    Serial.begin(115200);
    plotter.setStartTime(millis());
}

void loop() {
    float value = analogRead(A0) * 5.0 / 1023.0;
    plotter.send(0, value, millis());
    delay(100);
}
```

### ESP32 (WiFi + MQTT)

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <plotter.h>

class MQTTStream : public PlotterStream {
    PubSubClient& client;
    const char* topic;
public:
    MQTTStream(PubSubClient& c, const char* t) : client(c), topic(t) {}

    size_t write(const uint8_t* data, size_t length) override {
        char buffer[128];
        if (length < sizeof(buffer) - 1) {
            memcpy(buffer, data, length);
            buffer[length] = '\0';
            return client.publish(topic, buffer) ? length : 0;
        }
        return 0;
    }
};

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
MQTTStream mqttStream(mqttClient, "sensor/data");
Plotter plotter(mqttStream);
```

### STM32 (USB CDC)

```cpp
#include "main.h"
#include <plotter.h>
#include <plotter_stm32.h>

CDCStream usbStream;
Plotter plotter(usbStream);

int main(void) {
    HAL_Init();
    // ... configure peripherals

    plotter.setStartTime(HAL_GetTick());

    while (1) {
        float voltage = read_adc() * 3.3f / 4095.0f;
        plotter.send(0, voltage, HAL_GetTick());
    }
}
```

## API Reference

### Class: Plotter

#### Constructors

```cpp
// Default constructor (must call begin() later)
Plotter();

// Arduino/ESP32 - Direct Print object
Plotter(Print& printObj, bool enableTimestamp = true);

// Custom stream implementation
Plotter(PlotterStream& outputStream, bool enableTimestamp = true);
```

#### Methods

```cpp
// Initialize with stream
void begin(PlotterStream& outputStream, bool enableTimestamp = true);
void begin(Print& printObj, bool enableTimestamp = true);  // Arduino only

// Set start time for timestamp calculation
void setStartTime(uint32_t startTime);

// Send data with automatic timestamp (ms → seconds)
void send(uint8_t channelId, float value, uint32_t currentTimeMs);

// Send data with explicit timestamp (seconds)
void send(uint8_t channelId, float value, float timestamp);

// Send data without timestamp (PlotterApp auto-generates)
void send(uint8_t channelId, float value);

// Enable/disable timestamps
void setTimestampEnabled(bool enable);
bool isTimestampEnabled() const;
```

### Class: PlotterStream (Abstract)

Implement this interface to add new communication methods:

```cpp
class PlotterStream {
public:
    virtual size_t write(const uint8_t* data, size_t length) = 0;
    virtual ~PlotterStream() {}
};
```

### STM32 Streams (plotter_stm32.h)

```cpp
// USB CDC stream
class CDCStream : public PlotterStream {
    size_t write(const uint8_t* data, size_t length) override;
};

// UART stream
class UARTStream : public PlotterStream {
    UARTStream(void* huart_handle, uint32_t txTimeout = 100);
    size_t write(const uint8_t* data, size_t length) override;
};
```

## Data Format

PlotterLib sends data in JSON format:

```json
{"id":0,"value":3.14,"timestamp":1.234}
{"id":1,"value":2.71}
```

- `id`: Channel ID (0-255)
- `value`: Sensor value (float, 6 decimal places)
- `timestamp`: Optional timestamp in seconds (float, 6 decimal places)

## Examples

See the example projects in the parent directories:

- `arduino/simple_analog_example/` - Basic Arduino ADC reading
- `arduino/multi_sensor_example/` - Multiple channels
- `esp32/serial_example/` - ESP32 USB CDC
- `esp32/wifi_mqtt_example/` - Wireless data streaming
- `stm32/usb_cdc_example/` - STM32 USB Virtual COM Port
- `stm32/uart_example/` - STM32 UART communication

## Building Examples

### PlatformIO

```bash
# Arduino Uno
cd arduino/simple_analog_example
pio run -e uno -t upload

# ESP32
cd esp32/serial_example
pio run -e esp32dev -t upload

# STM32
cd stm32/usb_cdc_example
pio run -e nucleo_f401re -t upload
```

### Arduino IDE

1. Open the `.ino` file in the example folder
2. Select your board and port
3. Click Upload

## Performance

### Memory Footprint

| Platform | RAM Usage | Flash Usage |
|----------|-----------|-------------|
| Arduino (AVR) | 78 bytes | ~2.5 KB |
| ESP32 | 78 bytes | ~2.0 KB |
| STM32 | 74 bytes | ~2.0 KB |

### CPU Usage

- Per `send()` call: <200 CPU cycles
- No dynamic memory allocation (except optional PrintStream wrapper)
- No heap fragmentation

### Comparison with ArduinoJson

| Metric | PlotterLib | ArduinoJson |
|--------|-----------|-------------|
| Flash Size | 2-3 KB | 15-20 KB |
| RAM Usage | 74-78 bytes | 200-500 bytes |
| CPU Cycles | <200 | 500-1000 |

## License

MIT License

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.

## Support

For questions and support, please open an issue on the GitHub repository.
