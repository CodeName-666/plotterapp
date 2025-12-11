/**
 * @file main.cpp
 * @brief Simple Arduino example using Plotter class
 *
 * Reads analog sensor and sends data to PlotterApp.
 * PlatformIO project - compile with: pio run -e uno
 *
 * @version 4.0
 * @date 2025-12-11
 */

#include <Arduino.h>
#include <plotter.h>

#define SAMPLE_RATE_MS 100  // 10 Hz
#define ANALOG_PIN A0

Plotter plotter(Serial);  // Direct construction with Serial
unsigned long lastSample = 0;

void setup() {
    Serial.begin(115200);
    while (!Serial) {
        ; // Wait for serial port
    }

    // Set start time for timestamps
    plotter.setStartTime(millis());

    Serial.println("# Arduino Simple Analog Example");
    Serial.println("# Reading from pin A0");
}

void loop() {
    unsigned long currentTime = millis();

    if (currentTime - lastSample >= SAMPLE_RATE_MS) {
        lastSample = currentTime;

        // Read analog sensor
        int rawValue = analogRead(ANALOG_PIN);
        float voltage = (rawValue / 1023.0) * 5.0;

        // Send data point (channel 0)
        plotter.send(0, voltage, currentTime);
    }
}
