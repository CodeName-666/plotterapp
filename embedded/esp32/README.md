# ESP32 Examples for PlotterApp

WiFi-enabled microcontroller examples using the Plotter library for wireless sensor monitoring.

## 📋 Requirements

- ESP32 board (ESP32, ESP32-S2, ESP32-S3, ESP32-C3)
- Arduino IDE with ESP32 support
- WiFi network (for MQTT example)
- MQTT broker (for MQTT example)

## 📁 Examples

### 1. Serial Example
**File:** `serial_example/serial_example.ino`

Simple USB Serial streaming using the Plotter library.

**Best for:**
✅ Quick testing
✅ Development and debugging
✅ USB-powered applications

**Boards:**
- ESP32-S2 (native USB)
- ESP32-S3 (native USB)
- ESP32-C3 (native USB)
- Classic ESP32 (via USB-Serial chip)

---

### 2. WiFi + MQTT Example
**File:** `wifi_mqtt_example/wifi_mqtt_example.ino`

Wireless data streaming via MQTT using the Plotter library.

**Best for:**
✅ Remote sensor monitoring
✅ Multiple ESP32 devices
✅ IoT applications
✅ Wireless freedom

**Features:**
- WiFi connection management
- MQTT publish/subscribe
- Auto-reconnect
- Multiple sensor channels

**Required Libraries:**
- PubSubClient by Nick O'Leary

---

## 🔧 Setup Instructions

### Install ESP32 Support in Arduino IDE

1. **Open Arduino IDE Preferences**
   - File → Preferences

2. **Add ESP32 Board Manager URL**
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```

3. **Install ESP32 Boards**
   - Tools → Board → Boards Manager
   - Search "ESP32"
   - Install "esp32 by Espressif Systems"

4. **Select Your Board**
   - Tools → Board → ESP32 Arduino → Select your board

---

### Serial Example Setup

1. **Open Example**
   - Open `serial_example.ino` in Arduino IDE
   - The Plotter library will be referenced automatically

2. **Select Board**
   - ESP32-S3: "ESP32S3 Dev Module"
   - ESP32-C3: "ESP32C3 Dev Module"
   - Classic ESP32: "ESP32 Dev Module"

3. **Upload Sketch**
   - Click Upload
   - Wait for compilation and upload

4. **Connect in PlotterApp**
   - Connections → New → Serial
   - Select COM port
   - Baud: 115200
   - Start

---

### MQTT Example Setup

#### 1. Install Required Library

In Arduino IDE: Sketch → Include Library → Manage Libraries

Install:
- **PubSubClient** by Nick O'Leary

#### 2. Setup MQTT Broker

**Option A: Mosquitto (Local)**
```bash
# Windows
choco install mosquitto

# Linux
sudo apt-get install mosquitto mosquitto-clients

# macOS
brew install mosquitto
```

**Option B: Cloud MQTT Broker**
- [HiveMQ Cloud](https://www.hivemq.com/mqtt-cloud-broker/) - Free tier
- [CloudMQTT](https://www.cloudmqtt.com/) - Free tier
- [EMQX Cloud](https://www.emqx.com/en/cloud) - Free trial

#### 3. Configure WiFi & MQTT

Edit in `wifi_mqtt_example.ino`:
```cpp
// WiFi credentials
const char* WIFI_SSID = "YourWiFiName";
const char* WIFI_PASSWORD = "YourWiFiPassword";

// MQTT broker
const char* MQTT_BROKER = "192.168.1.100";  // Your broker IP
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC_TX = "sensor/data";
```

#### 4. Upload & Run

1. Connect ESP32 via USB
2. Upload sketch
3. Open Serial Monitor (115200 baud)
4. Watch for WiFi connection
5. Note IP address

#### 5. Configure PlotterApp

1. Connections → New → MQTT
2. Host: Your broker IP (same as in code)
3. Port: 1883
4. RX Topic: `sensor/data`
5. TX Topic: `sensor/command` (optional)
6. Create & Start
7. Data should stream wirelessly!

---

## 💻 Using the Plotter Library

### Serial Example

```cpp
#include "../../common/plotter.h"

PlotterClass plotter;

void serialSend(const char* data, uint16_t length) {
    Serial.write((const uint8_t*)data, length);
}

void setup() {
    Serial.begin(115200);

    // Initialize plotter with timestamps
    plotter.begin(serialSend, true);
    plotter.setStartTime(millis());
}

void loop() {
    unsigned long currentTime = millis();

    float value = readSensor();

    // Send data on channel 0
    plotter.send(0, value, currentTime);

    delay(100);  // 10 Hz
}
```

### MQTT Example

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include "../../common/plotter.h"

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
PlotterClass plotter;

void mqttSend(const char* data, uint16_t length) {
    char buffer[128];
    if (length < sizeof(buffer)) {
        memcpy(buffer, data, length);
        buffer[length] = '\0';
        mqttClient.publish("sensor/data", buffer);
    }
}

void setup() {
    // Connect WiFi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }

    // Setup MQTT
    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);

    // Initialize plotter
    plotter.begin(mqttSend, true);
    plotter.setStartTime(millis());
}

void loop() {
    if (!mqttClient.connected()) {
        reconnectMQTT();
    }
    mqttClient.loop();

    unsigned long currentTime = millis();
    float value = readSensor();

    plotter.send(0, value, currentTime);

    delay(100);
}
```

---

## 📊 MQTT Data Flow

```
ESP32 Sensor → WiFi → MQTT Broker → WiFi → PlotterApp
                ↓
            Internet (optional)
                ↓
        Other MQTT clients
```

---

## 🚀 Advanced Features

### Multiple ESP32 Devices

Each ESP32 can have different sensors:

**ESP32 #1 (Kitchen):**
```cpp
const char* MQTT_CLIENT_ID = "ESP32_Kitchen";
const char* MQTT_TOPIC_TX = "kitchen/sensors";
```

**ESP32 #2 (Bedroom):**
```cpp
const char* MQTT_CLIENT_ID = "ESP32_Bedroom";
const char* MQTT_TOPIC_TX = "bedroom/sensors";
```

In PlotterApp, create separate MQTT connections with different RX topics.

---

### Deep Sleep for Battery Power

```cpp
#define SLEEP_DURATION_SECONDS 60

void loop() {
    // Read sensors
    float value = readSensor();
    plotter.send(0, value, millis());

    // Go to deep sleep
    esp_sleep_enable_timer_wakeup(SLEEP_DURATION_SECONDS * 1000000);
    esp_deep_sleep_start();
}
```

---

### Real Sensor Integration

#### DHT22 Temperature & Humidity:
```cpp
#include <DHT.h>
#include "../../common/plotter.h"

#define DHT_PIN 4
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

#### BMP280 Pressure Sensor:
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

### WiFi won't connect?

1. **Check credentials** - Case-sensitive!
2. **2.4 GHz only** - ESP32 doesn't support 5 GHz
3. **Signal strength** - Move closer to router
4. **DHCP enabled** - Router must assign IP
5. **Check Serial Monitor** - Shows connection status

### MQTT connection fails?

1. **Broker running?** - Test with `mosquitto_sub -h localhost -t "#"`
2. **Firewall** - Allow port 1883
3. **IP address** - Use `ipconfig` (Windows) or `ifconfig` (Linux/Mac)
4. **Test with MQTT client** - Use MQTT.fx or MQTT Explorer

### Data not appearing in PlotterApp?

1. **Check MQTT topic** - Must match exactly
2. **Verify JSON format** - Check Serial Monitor output
3. **QoS level** - Try QoS 0 (default)
4. **Broker logs** - Check mosquitto logs

### ESP32 keeps rebooting?

1. **Power supply** - Use good USB cable and power source
2. **Brownout detector** - May trigger on weak power
3. **Check infinite loop** - Verify loop() has delay
4. **Monitor Serial** - Look for exception/stack trace

### Serial not working?

1. **Check USB cable** - Must be data cable
2. **Verify baud rate** - 115200 in both code and Serial Monitor
3. **Select correct board** - Tools → Board
4. **Check COM port** - Tools → Port

---

## 💡 Pro Tips

### WiFi Optimization:
```cpp
// Reduce power consumption
WiFi.setSleep(true);

// Set static IP (faster connect)
IPAddress local_IP(192, 168, 1, 100);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
WiFi.config(local_IP, gateway, subnet);
WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
```

### MQTT Optimization:
```cpp
// Increase keep-alive
mqttClient.setKeepAlive(60);

// Set buffer size for large messages
mqttClient.setBufferSize(512);

// QoS levels:
// 0 = At most once (fastest, may lose data)
// 1 = At least once (slower, no data loss)
// 2 = Exactly once (slowest, guaranteed)
```

### Performance:
- **Serial**: ~200 Hz max practical
- **MQTT WiFi**: ~100 Hz recommended
- **Battery life**: Deep sleep = days/weeks vs. hours

---

## 🔗 Resources

- [ESP32 Arduino Core](https://github.com/espressif/arduino-esp32)
- [PubSubClient Documentation](https://pubsubclient.knolleary.net/)
- [MQTT Specification](https://mqtt.org/)
- [ESP32 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)

---

## 🌐 MQTT Broker Options

### Local (Best for development):
- **Mosquitto** - Open source, lightweight
- **EMQX** - Enterprise features, scalable

### Cloud (Best for remote access):
- **HiveMQ Cloud** - Free tier, easy setup
- **AWS IoT Core** - AWS integration
- **Azure IoT Hub** - Azure integration

---

## 💡 Next Steps

1. **Start with Serial example** - Verify basic setup
2. **Test MQTT locally** - Install Mosquitto
3. **Add real sensors** - DHT22, BMP280, etc.
4. **Deploy multiple ESP32s** - Build sensor network
5. **Enable deep sleep** - For battery-powered applications
