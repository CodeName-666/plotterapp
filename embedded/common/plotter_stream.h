/**
 * @file plotter_stream.h
 * @brief Abstract stream interface for Plotter
 *
 * Defines the base interface for output streams used by Plotter.
 * Implement this interface to add support for new communication methods.
 *
 * @version 4.0
 * @date 2025-12-11
 */

#ifndef PLOTTER_STREAM_H
#define PLOTTER_STREAM_H

#include <stdint.h>
#include <stddef.h>

/**
 * @brief Abstract base class for output streams
 *
 * Implement this interface to add support for new communication methods.
 * The Plotter class uses this interface to send formatted data.
 *
 * Example implementation:
 * @code
 * class MyCustomStream : public PlotterStream {
 * public:
 *     size_t write(const uint8_t* data, size_t length) override {
 *         // Send data via your custom interface
 *         return my_send_function(data, length);
 *     }
 * };
 * @endcode
 */
class PlotterStream {
public:
    /**
     * @brief Write data to the stream
     *
     * @param data Pointer to data buffer
     * @param length Number of bytes to write
     * @return Number of bytes actually written
     */
    virtual size_t write(const uint8_t* data, size_t length) = 0;

    /**
     * @brief Virtual destructor
     */
    virtual ~PlotterStream() {}
};

// Arduino-specific stream wrapper
#ifdef ARDUINO
#include <Print.h>

/**
 * @brief Wrapper for Arduino Print objects (Serial, WiFiClient, etc.)
 *
 * Allows using any Arduino Print-compatible object with Plotter.
 * This wrapper is automatically used when constructing Plotter with
 * a Print object on Arduino platforms.
 *
 * Example:
 * @code
 * PrintStream stream(Serial);
 * Plotter plotter(stream);
 *
 * // Or use the convenience constructor:
 * Plotter plotter(Serial);  // Creates PrintStream internally
 * @endcode
 */
class PrintStream : public PlotterStream {
private:
    Print& printObj;

public:
    /**
     * @brief Construct a PrintStream from a Print object
     *
     * @param p Reference to Print object (Serial, WiFiClient, File, etc.)
     */
    PrintStream(Print& p) : printObj(p) {}

    /**
     * @brief Write data using Print::write()
     *
     * @param data Pointer to data buffer
     * @param length Number of bytes to write
     * @return Number of bytes written
     */
    size_t write(const uint8_t* data, size_t length) override {
        return printObj.write(data, length);
    }
};
#endif // ARDUINO

#endif // PLOTTER_STREAM_H
