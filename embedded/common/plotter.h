/**
 * @file plotter.h
 * @brief Plotter C++ class for sending data to PlotterApp
 *
 * Modern C++ interface using abstract base class for maximum flexibility.
 * Works with Arduino Print objects, custom streams, and STM32.
 *
 * @version 4.0
 * @date 2025-12-11
 */

#ifndef PLOTTER_H
#define PLOTTER_H

#include <stdint.h>
#include <stdio.h>
#include "plotter_stream.h"

/**
 * @brief Plotter class for streaming sensor data to PlotterApp
 *
 * Modern interface using dependency injection via PlotterStream.
 * Supports automatic JSON formatting and timestamp management.
 *
 * Example usage with Arduino:
 * @code
 * #include "plotter.h"
 *
 * Plotter plotter(Serial);
 *
 * void setup() {
 *     Serial.begin(115200);
 *     plotter.setStartTime(millis());
 * }
 *
 * void loop() {
 *     float value = analogRead(A0) * 5.0 / 1023.0;
 *     plotter.send(0, value, millis());
 *     delay(100);
 * }
 * @endcode
 *
 * Example with custom stream:
 * @code
 * class MyStream : public PlotterStream {
 * public:
 *     size_t write(const uint8_t* data, size_t length) override {
 *         // Custom implementation
 *         return my_send_function(data, length);
 *     }
 * };
 *
 * MyStream stream;
 * Plotter plotter(stream);
 * @endcode
 */
class Plotter {
private:
    PlotterStream* stream;     ///< Output stream
    uint32_t startTimeMs;      ///< Start time in milliseconds
    bool useTimestamp;         ///< Whether to include timestamps
    char buffer[80];           ///< Internal buffer for formatting (increased for 3D support)
    bool ownsStream;           ///< Whether we own the stream object

#ifdef ARDUINO
    PrintStream* printStream;  ///< Owned PrintStream wrapper
#endif

public:
    /**
     * @brief Default constructor
     *
     * Must call begin() before use.
     */
    Plotter();

#ifdef ARDUINO
    /**
     * @brief Construct with Arduino Print object
     *
     * Automatically creates a PrintStream wrapper.
     * Most convenient way to use Plotter on Arduino/ESP32.
     *
     * @param printObj Reference to Print object (Serial, WiFiClient, etc.)
     * @param enableTimestamp Whether to include timestamps (default: true)
     *
     * @code
     * Plotter plotter(Serial);
     * @endcode
     */
    Plotter(Print& printObj, bool enableTimestamp = true);
#endif

    /**
     * @brief Construct with PlotterStream
     *
     * Use this for custom stream implementations.
     *
     * @param outputStream Reference to PlotterStream implementation
     * @param enableTimestamp Whether to include timestamps (default: true)
     *
     * @code
     * MyCustomStream stream;
     * Plotter plotter(stream);
     * @endcode
     */
    Plotter(PlotterStream& outputStream, bool enableTimestamp = true);

    /**
     * @brief Destructor
     *
     * Automatically cleans up owned PrintStream if created.
     */
    ~Plotter();

    /**
     * @brief Initialize with PlotterStream
     *
     * @param outputStream Reference to PlotterStream implementation
     * @param enableTimestamp Whether to include timestamps (default: true)
     */
    void begin(PlotterStream& outputStream, bool enableTimestamp = true);

#ifdef ARDUINO
    /**
     * @brief Initialize with Arduino Print object
     *
     * @param printObj Reference to Print object
     * @param enableTimestamp Whether to include timestamps (default: true)
     */
    void begin(Print& printObj, bool enableTimestamp = true);
#endif

    /**
     * @brief Set the start time for timestamp calculation
     *
     * Call this once during initialization with the current time.
     * All subsequent timestamps will be relative to this start time.
     *
     * @param startTime Current time in milliseconds
     *
     * @code
     * plotter.setStartTime(millis());  // Arduino
     * plotter.setStartTime(HAL_GetTick());  // STM32
     * @endcode
     */
    void setStartTime(uint32_t startTime);

    /**
     * @brief Send data point with automatic timestamp
     *
     * Calculates timestamp automatically from current time and start time.
     * Timestamp is converted to seconds (floating point).
     *
     * @param channelId Channel ID (0-255)
     * @param value Sensor value
     * @param currentTimeMs Current time in milliseconds
     *
     * @code
     * plotter.send(0, temperature, millis());
     * plotter.send(1, humidity, millis());
     * @endcode
     */
    void send(uint8_t channelId, float value, uint32_t currentTimeMs);

    /**
     * @brief Send data point with explicit timestamp
     *
     * Use this for custom timestamp values in seconds.
     *
     * @param channelId Channel ID (0-255)
     * @param value Sensor value
     * @param timestamp Explicit timestamp in seconds
     *
     * @code
     * plotter.send(0, temperature, 1.234);
     * @endcode
     */
    void send(uint8_t channelId, float value, float timestamp);

    /**
     * @brief Send data point without timestamp
     *
     * PlotterApp will auto-generate timestamps based on arrival time.
     *
     * @param channelId Channel ID (0-255)
     * @param value Sensor value
     *
     * @code
     * plotter.send(0, temperature);
     * @endcode
     */
    void send(uint8_t channelId, float value);

    /**
     * @brief Send 3D data point with automatic timestamp
     *
     * For 3D charts (XYZ surface/scatter plots).
     * Calculates timestamp automatically from current time and start time.
     *
     * @param channelId Channel ID (0-255)
     * @param yValue Y-axis value (measurement value)
     * @param zValue Z-axis value (depth/height)
     * @param currentTimeMs Current time in milliseconds
     *
     * @code
     * plotter.send3D(0, temperature, pressure, millis());
     * @endcode
     */
    void send3D(uint8_t channelId, float yValue, float zValue, uint32_t currentTimeMs);

    /**
     * @brief Send 3D data point with explicit timestamp
     *
     * For 3D charts with custom timestamp values in seconds.
     *
     * @param channelId Channel ID (0-255)
     * @param yValue Y-axis value (measurement value)
     * @param zValue Z-axis value (depth/height)
     * @param timestamp Explicit timestamp in seconds
     *
     * @code
     * plotter.send3D(0, temperature, pressure, 1.234);
     * @endcode
     */
    void send3D(uint8_t channelId, float yValue, float zValue, float timestamp);

    /**
     * @brief Send 3D data point without timestamp
     *
     * For 3D charts. PlotterApp will auto-generate timestamps.
     *
     * @param channelId Channel ID (0-255)
     * @param yValue Y-axis value (measurement value)
     * @param zValue Z-axis value (depth/height)
     *
     * @code
     * plotter.send3D(0, temperature, pressure);
     * @endcode
     */
    void send3D(uint8_t channelId, float yValue, float zValue);

    /**
     * @brief Enable or disable timestamps
     *
     * @param enable True to include timestamps, false to omit
     */
    void setTimestampEnabled(bool enable);

    /**
     * @brief Check if timestamps are enabled
     *
     * @return True if timestamps are enabled
     */
    bool isTimestampEnabled() const;
};

#endif // PLOTTER_H
