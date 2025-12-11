# Embedded Examples for PlotterApp

**Version 4.0** - PlatformIO ready examples for streaming sensor data to PlotterApp

## 🎯 Overview

This directory contains **PlotterLib**, a lightweight C++ library, and ready-to-use PlatformIO examples for various microcontroller platforms. The library provides a modern, flexible interface for sending sensor data without requiring external JSON libraries.

## 📁 Directory Structure

```
embedded/
├── common/                    # PlotterLib - Core library (PlatformIO compatible)
│   ├── plotter.h             # Main Plotter class
│   ├── plotter.cpp           # Implementation
│   ├── plotter_stream.h      # Abstract stream interface
│   ├── plotter_stm32.h       # STM32-specific streams
│   ├── library.json          # PlatformIO library manifest
│   ├── library.properties    # Arduino library properties
│   └── README.md             # Library documentation
├── arduino/                   # Arduino PlatformIO examples
│   ├── simple_analog_example/
│   │   ├── platformio.ini
│   │   └── src/main.cpp
│   └── multi_sensor_example/
│       ├── platformio.ini
│       └── src/main.cpp
├── esp32/                     # ESP32 PlatformIO examples
│   ├── serial_example/
│   │   ├── platformio.ini
│   │   └── src/main.cpp
│   └── wifi_mqtt_example/
│       ├── platformio.ini
│       └── src/main.cpp
└── stm32/                     # STM32 PlatformIO examples
    ├── usb_cdc_example/
    │   ├── platformio.ini
    │   └── src/main.cpp
    └── uart_example/
        ├── platformio.ini
        └── src/main.cpp
```

## 🚀 Quick Start

### Option 1: PlatformIO (Recommended)

```bash
# Clone or navigate to an example
cd embedded/arduino/simple_analog_example

# Build and upload
pio run -e uno -t upload

# Monitor serial output
pio device monitor
```

### Option 2: Arduino IDE

The library also works with Arduino IDE:

1. Copy `common/` folder to Arduino libraries as `PlotterLib`
2. Open any `.ino` file from the examples
3. Upload to your board

See [PlotterLib README](common/README.md) for detailed installation instructions.

## 🔧 PlotterLib Features

✅ **Extremely Lightweight**
- Only ~125 lines of code
- 74-78 bytes RAM per instance
- 2-3 KB Flash/ROM
- **85% smaller than ArduinoJson**

✅ **Modern C++ Architecture**
- Abstract `PlotterStream` interface
- Dependency injection pattern
- Easy to extend with new interfaces

✅ **Platform Support**
- Arduino (all boards)
- ESP32 (all variants)
- STM32 (all families)
- Any C++11 compatible platform

✅ **Flexible Communication**
- Serial, WiFi, MQTT, Bluetooth
- USB CDC, UART, SPI, I2C
- Custom stream implementations

## 📝 Basic Usage

```cpp
#include <Arduino.h>
#include <plotter.h>

Plotter plotter(Serial);  // Direct construction with Serial

void setup() {
    Serial.begin(115200);
    plotter.setStartTime(millis());
}

void loop() {
    float value = analogRead(A0) * 5.0 / 1023.0;
    plotter.send(0, value, millis());  // Channel 0
    delay(100);
}
```

## 📡 Data Format

PlotterLib automatically formats data as JSON:

```json
{"id":0,"value":3.14159,"timestamp":1.234567}
{"id":1,"value":2.71828}
```

- **id**: Channel ID (0-255)
- **value**: Sensor value (float, 6 decimals)
- **timestamp**: Optional timestamp in seconds (float, 6 decimals)

## 🎨 Examples by Platform

### Arduino Examples

| Example | Description | Boards |
|---------|-------------|--------|
| [simple_analog_example](arduino/simple_analog_example/) | Basic ADC reading | Uno, Nano, Mega |
| [multi_sensor_example](arduino/multi_sensor_example/) | Multiple channels | Uno, Nano, Mega |

**Build commands:**
```bash
cd arduino/simple_analog_example
pio run -e uno        # Arduino Uno
pio run -e nano       # Arduino Nano
pio run -e mega       # Arduino Mega
```

### ESP32 Examples

| Example | Description | Communication |
|---------|-------------|---------------|
| [serial_example](esp32/serial_example/) | USB CDC streaming | Serial/USB |
| [wifi_mqtt_example](esp32/wifi_mqtt_example/) | Wireless data | WiFi + MQTT |

**Build commands:**
```bash
cd esp32/serial_example
pio run -e esp32dev    # ESP32 DevKit
pio run -e esp32-s3    # ESP32-S3
pio run -e esp32-c3    # ESP32-C3
```

### STM32 Examples

| Example | Description | Communication |
|---------|-------------|---------------|
| [usb_cdc_example](stm32/usb_cdc_example/) | Virtual COM Port | USB CDC |
| [uart_example](stm32/uart_example/) | Serial adapter | UART |

**Build commands:**
```bash
cd stm32/usb_cdc_example
pio run -e nucleo_f401re    # Nucleo F401RE
pio run -e nucleo_f411re    # Nucleo F411RE
pio run -e bluepill_f103c8  # Blue Pill
```

## 🎓 Advanced Usage

### Custom Stream Implementation

Create custom communication interfaces by inheriting from `PlotterStream`:

```cpp
class MyCustomStream : public PlotterStream {
public:
    size_t write(const uint8_t* data, size_t length) override {
        // Your custom send implementation
        return my_send_function(data, length);
    }
};

MyCustomStream customStream;
Plotter plotter(customStream);
```

### Multiple Sensors Example

```cpp
void loop() {
    unsigned long currentTime = millis();

    float temperature = readTemperature();
    float humidity = readHumidity();
    float pressure = readPressure();

    // Send all channels with same timestamp
    plotter.send(0, temperature, currentTime);
    plotter.send(1, humidity, currentTime);
    plotter.send(2, pressure, currentTime);

    delay(100);
}
```

### ESP32 MQTT Streaming

```cpp
class MQTTStream : public PlotterStream {
    PubSubClient& client;
    const char* topic;
public:
    MQTTStream(PubSubClient& c, const char* t)
        : client(c), topic(t) {}

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

## ⚡ Performance

### Memory Footprint

| Platform | RAM Usage | Flash Usage | vs ArduinoJson |
|----------|-----------|-------------|----------------|
| Arduino (AVR) | 78 bytes | ~2.5 KB | -70% RAM |
| ESP32 | 78 bytes | ~2.0 KB | -70% RAM |
| STM32 | 74 bytes | ~2.0 KB | -70% RAM |

### Recommended Sampling Rates

| Platform | Interface | Max Rate | Recommended |
|----------|-----------|----------|-------------|
| Arduino | Serial | 200 Hz | 100 Hz |
| ESP32 | Serial | 500 Hz | 200 Hz |
| ESP32 | WiFi/MQTT | 200 Hz | 100 Hz |
| STM32 | USB CDC | 2000 Hz | 1000 Hz |
| STM32 | UART | 500 Hz | 200 Hz |

## 🔧 API Reference

See [PlotterLib README](common/README.md) for complete API documentation.

### Quick Reference

```cpp
// Constructors
Plotter plotter(Serial);              // Arduino Print object
Plotter plotter(customStream);        // Custom PlotterStream

// Configuration
plotter.setStartTime(millis());       // Set timestamp base
plotter.setTimestampEnabled(false);   // Disable timestamps

// Send data
plotter.send(id, value, millis());    // With auto timestamp
plotter.send(id, value, 1.234);       // With explicit timestamp
plotter.send(id, value);              // Without timestamp
```

## 🛠️ Troubleshooting

### PlatformIO Issues

**Library not found?**
```bash
# Clean and rebuild
pio run -t clean
pio run
```

**Symlink not working?**
- Windows: Run PlatformIO from elevated terminal
- Alternative: Copy `common/` to `lib/PlotterLib/` in your project

### Data Issues

**No data in PlotterApp?**
1. Check baud rate matches (115200)
2. Verify correct COM port
3. Ensure data ends with `\n`
4. Check JSON format

**Timestamps incorrect?**
1. Call `setStartTime()` in setup
2. Use consistent time source (millis() or HAL_GetTick())
3. Don't reset timer between samples

## 📖 Documentation

- [PlotterLib Documentation](common/README.md) - Complete library reference
- Platform examples include detailed comments
- See PlatformIO documentation for build system help

## 🔗 Related Links

- [PlatformIO](https://platformio.org/) - Build system
- [PlotterApp Documentation](../README.md) - Main application docs

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please submit PRs or open issues.

## 💡 Need Help?

- Check example code in `src/main.cpp` files
- Read [PlotterLib README](common/README.md)
- Open an issue on GitHub
