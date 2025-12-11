/**
 * @file main.cpp
 * @brief Arduino multi-channel example using Plotter class
 *
 * Demonstrates sending multiple sensor channels to PlotterApp.
 * PlatformIO project - compile with: pio run -e uno
 *
 * @version 4.0
 * @date 2025-12-11
 */

#include <Arduino.h>
#include <plotter.h>

#define SAMPLE_RATE_MS 100  // 10 Hz

Plotter plotter(Serial);  // Direct construction with Serial
unsigned long lastSample = 0;

void setup() {
    Serial.begin(115200);
    while (!Serial) {
        ; // Wait for serial port
    }

    // Set start time for timestamps
    plotter.setStartTime(millis());

    Serial.println("# Arduino Multi-Sensor Example");
    Serial.println("# Channel 0: Temperature");
    Serial.println("# Channel 1: Humidity");
    Serial.println("# Channel 2: Pressure");
}

void loop() {
    unsigned long currentTime = millis();

    if (currentTime - lastSample >= SAMPLE_RATE_MS) {
        lastSample = currentTime;

        // Simulate sensor readings
        float temperature = 20.0 + sin(currentTime / 1000.0) * 5.0;
        float humidity = 50.0 + cos(currentTime / 800.0) * 10.0;
        float pressure = 1013.25 + sin(currentTime / 1200.0) * 20.0;

        // Send all three channels
        plotter.send(0, temperature, currentTime);
        plotter.send(1, humidity, currentTime);
        plotter.send(2, pressure, currentTime);
    }
}
