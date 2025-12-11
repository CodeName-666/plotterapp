/**
 * @file serial_example.ino
 * @brief ESP32 Serial (USB) example using Plotter class
 *
 * Simple example using ESP32's USB CDC for data streaming.
 * Works with ESP32-S2, ESP32-S3, ESP32-C3 (have native USB).
 * For older ESP32, use USB-to-Serial adapter on GPIO1/GPIO3.
 *
 * @version 2.0
 * @date 2025-12-10
 */

#include "../../common/plotter.h"

#define SAMPLE_RATE_MS 50
#define ADC_PIN 34

Plotter plotter(Serial);  // Direct construction with Serial
unsigned long lastSample = 0;

void setup() {
    Serial.begin(115200);
    delay(1000);  // Wait for serial

    analogSetAttenuation(ADC_11db);  // 0-3.3V range

    // Set start time for timestamps
    plotter.setStartTime(millis());

    Serial.println("# ESP32 Serial PlotterApp Example");
}

void loop() {
    unsigned long currentTime = millis();

    if (currentTime - lastSample >= SAMPLE_RATE_MS) {
        lastSample = currentTime;

        // Read ADC
        int rawValue = analogRead(ADC_PIN);
        float voltage = (rawValue / 4095.0) * 3.3;

        // Send data point (channel 0)
        plotter.send(0, voltage, currentTime);
    }
}
