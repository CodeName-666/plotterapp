# Arduino Examples for PlotterApp

Simple Arduino examples using the Plotter library for sensor data streaming.

## 📋 Requirements

- Arduino board (Uno, Nano, Mega, Leonardo, etc.)
- Arduino IDE 1.8.x or 2.x
- USB cable

## 📁 Examples

### 1. Simple Analog Example
**File:** `simple_analog_example/simple_analog_example.ino`

Reads analog sensor from pin A0 and streams voltage values.

**Features:**
- Single channel (ID: 0)
- 10 Hz sampling rate
- Automatic timestamp calculation
- Voltage conversion (0-5V)

**Best for:**
✅ Quick testing
✅ Single sensor applications
✅ Learning the basics

---

### 2. Multi-Sensor Example
**File:** `multi_sensor_example/multi_sensor_example.ino`

Demonstrates streaming multiple sensor channels simultaneously.

**Features:**
- Three channels (Temperature, Humidity, Pressure)
- 10 Hz sampling rate
- Simulated sensor data
- Synchronized timestamps

**Best for:**
✅ Multi-channel data logging
✅ Multiple sensor applications
✅ Understanding channel management

---

## 🔧 Setup Instructions

### 1. Copy Plotter Library

The Plotter library is located in `embedded/common/`:
- `plotter.h`
- `plotter.cpp`

Arduino IDE will find these files automatically when you open the `.ino` file.

### 2. Open Example

1. Open Arduino IDE
2. Open desired example `.ino` file
3. The library files will be referenced automatically

### 3. Select Board and Port

1. **Tools → Board** - Select your Arduino board
2. **Tools → Port** - Select COM port

### 4. Upload Sketch

1. Click **Upload** button
2. Wait for compilation and upload
3. Open Serial Monitor to verify data output

### 5. Connect in PlotterApp

1. **Connections → New → Serial**
2. Select COM port (same as Arduino IDE)
3. Baud rate: **115200**
4. Click **Create** and **Start**
5. Data should start streaming!

---

## 💻 Using the Plotter Library

### Basic Setup

```cpp
#include "../../common/plotter.h"

PlotterClass plotter;

// Define send function for Serial
void serialSend(const char* data, uint16_t length) {
    Serial.write((const uint8_t*)data, length);
}

void setup() {
    Serial.begin(115200);
    while (!Serial) {
        ; // Wait for serial port (needed for Leonardo/Micro)
    }

    // Initialize plotter with timestamp support
    plotter.begin(serialSend, true);
    plotter.setStartTime(millis());
}
```

### Sending Data

```cpp
void loop() {
    unsigned long currentTime = millis();

    // Read sensor
    float value = analogRead(A0) * (5.0 / 1023.0);

    // Send data on channel 0
    plotter.send(0, value, currentTime);

    delay(100);  // 10 Hz
}
```

### Multiple Channels

```cpp
void loop() {
    unsigned long currentTime = millis();

    float temp = readTemperature();
    float humidity = readHumidity();

    // Send both channels with same timestamp
    plotter.send(0, temp, currentTime);
    plotter.send(1, humidity, currentTime);

    delay(100);
}
```

---

## 🔌 Hardware Connections

### Simple Analog Example

Connect analog sensor to **pin A0**:

```
Sensor Output → A0
Sensor VCC    → 5V
Sensor GND    → GND
```

**Example sensors:**
- Potentiometer (3-pin variable resistor)
- LM35 temperature sensor
- Light-dependent resistor (LDR) with voltage divider
- Analog accelerometer

### Real Sensor Examples

#### DHT22 Temperature & Humidity

Install library: **DHT sensor library** by Adafruit

```cpp
#include <DHT.h>
#include "../../common/plotter.h"

#define DHT_PIN 2
#define DHT_TYPE DHT22

DHT dht(DHT_PIN, DHT_TYPE);
PlotterClass plotter;

void serialSend(const char* data, uint16_t length) {
    Serial.write((const uint8_t*)data, length);
}

void setup() {
    Serial.begin(115200);
    dht.begin();

    plotter.begin(serialSend, true);
    plotter.setStartTime(millis());
}

void loop() {
    unsigned long currentTime = millis();

    float temp = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (!isnan(temp) && !isnan(humidity)) {
        plotter.send(0, temp, currentTime);
        plotter.send(1, humidity, currentTime);
    }

    delay(2000);  // DHT22 needs 2s between readings
}
```

#### BMP280 Pressure Sensor

Install library: **Adafruit BMP280 Library**

```cpp
#include <Adafruit_BMP280.h>
#include "../../common/plotter.h"

Adafruit_BMP280 bmp;
PlotterClass plotter;

void serialSend(const char* data, uint16_t length) {
    Serial.write((const uint8_t*)data, length);
}

void setup() {
    Serial.begin(115200);
    bmp.begin(0x76);

    plotter.begin(serialSend, true);
    plotter.setStartTime(millis());
}

void loop() {
    unsigned long currentTime = millis();

    float temp = bmp.readTemperature();
    float pressure = bmp.readPressure() / 100.0;  // hPa

    plotter.send(0, temp, currentTime);
    plotter.send(1, pressure, currentTime);

    delay(100);
}
```

---

## 🛠️ Troubleshooting

### Upload fails?

1. **Wrong board selected** - Verify board type in Tools → Board
2. **Wrong port** - Check COM port in Device Manager (Windows)
3. **Board not recognized** - Try different USB cable
4. **Permission denied** - Close Serial Monitor before upload

### No data in PlotterApp?

1. **Check COM port** - Must match Arduino IDE
2. **Verify baud rate** - Should be 115200
3. **Check Serial Monitor** - Data should appear as JSON lines
4. **Try different USB port** - Some ports have issues

### Data looks wrong?

1. **Timestamps jumping** - Ensure `setStartTime()` is called once in setup
2. **Values incorrect** - Check sensor wiring and voltage reference
3. **Missing data** - Reduce sample rate (increase delay)

### Compilation errors?

1. **"plotter.h not found"** - Ensure plotter.h and plotter.cpp are in common/ directory
2. **Include path wrong** - Use `#include "../../common/plotter.h"`
3. **Syntax errors** - Check C++ code for typos

---

## ⚡ Performance Tips

### Optimal Sample Rates

- **Arduino Uno/Nano**: 10-100 Hz recommended
- **Arduino Mega**: 10-200 Hz recommended
- **Arduino Leonardo**: 10-100 Hz recommended

Higher rates possible but may cause Serial buffer overflow.

### Reduce Serial Buffer Overflow

```cpp
// In loop(), add small delay
void loop() {
    // ... send data ...

    // Prevent buffer overflow
    Serial.flush();  // Wait for serial transmission to complete
    delay(10);       // Minimum delay between samples
}
```

### Multiple Channels Best Practice

Send all channels with the **same timestamp** for synchronized plotting:

```cpp
void loop() {
    unsigned long currentTime = millis();

    // Read ALL sensors first
    float sensor1 = readSensor1();
    float sensor2 = readSensor2();
    float sensor3 = readSensor3();

    // Then send ALL with same timestamp
    plotter.send(0, sensor1, currentTime);
    plotter.send(1, sensor2, currentTime);
    plotter.send(2, sensor3, currentTime);

    delay(100);
}
```

---

## 📊 Example Output

Serial Monitor should show:

```
# Arduino Multi-Sensor Example
# Channel 0: Temperature
# Channel 1: Humidity
# Channel 2: Pressure
{"id":0,"value":22.345000,"timestamp":0.100}
{"id":1,"value":55.234000,"timestamp":0.100}
{"id":2,"value":1013.250000,"timestamp":0.100}
{"id":0,"value":22.456000,"timestamp":0.200}
{"id":1,"value":55.123000,"timestamp":0.200}
{"id":2,"value":1013.300000,"timestamp":0.200}
```

---

## 🔗 Resources

- [Arduino Language Reference](https://www.arduino.cc/reference/en/)
- [Arduino Serial Documentation](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
- [Adafruit Sensor Libraries](https://github.com/adafruit)
- [PlotterApp Documentation](../../README.md)

---

## 💡 Next Steps

1. **Try the simple example** first to verify setup
2. **Modify the multi-sensor example** for your sensors
3. **Connect real sensors** using the hardware examples
4. **Experiment with sample rates** to find optimal performance
5. **Add more channels** for complex applications (up to 256 channels!)
