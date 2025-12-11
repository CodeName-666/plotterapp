/**
 * @file plotter.cpp
 * @brief Implementation of Plotter class
 *
 * @version 4.0
 * @date 2025-12-11
 */

#include "plotter.h"
#include <stdio.h>

// Default constructor
Plotter::Plotter()
    : stream(nullptr)
    , startTimeMs(0)
    , useTimestamp(true)
    , ownsStream(false)
#ifdef ARDUINO
    , printStream(nullptr)
#endif
{
}

#ifdef ARDUINO
// Constructor with Print object
Plotter::Plotter(Print& printObj, bool enableTimestamp)
    : stream(nullptr)
    , startTimeMs(0)
    , useTimestamp(enableTimestamp)
    , ownsStream(true)
    , printStream(new PrintStream(printObj))
{
    stream = printStream;
}
#endif

// Constructor with PlotterStream
Plotter::Plotter(PlotterStream& outputStream, bool enableTimestamp)
    : stream(&outputStream)
    , startTimeMs(0)
    , useTimestamp(enableTimestamp)
    , ownsStream(false)
#ifdef ARDUINO
    , printStream(nullptr)
#endif
{
}

// Destructor
Plotter::~Plotter() {
#ifdef ARDUINO
    if (ownsStream && printStream) {
        delete printStream;
        printStream = nullptr;
    }
#endif
}

// Begin with PlotterStream
void Plotter::begin(PlotterStream& outputStream, bool enableTimestamp) {
#ifdef ARDUINO
    // Clean up any existing owned stream
    if (ownsStream && printStream) {
        delete printStream;
        printStream = nullptr;
    }
#endif

    stream = &outputStream;
    useTimestamp = enableTimestamp;
    startTimeMs = 0;
    ownsStream = false;
}

#ifdef ARDUINO
// Begin with Print object
void Plotter::begin(Print& printObj, bool enableTimestamp) {
    // Clean up any existing owned stream
    if (ownsStream && printStream) {
        delete printStream;
    }

    printStream = new PrintStream(printObj);
    stream = printStream;
    useTimestamp = enableTimestamp;
    startTimeMs = 0;
    ownsStream = true;
}
#endif

void Plotter::setStartTime(uint32_t startTime) {
    startTimeMs = startTime;
}

void Plotter::send(uint8_t channelId, float value, uint32_t currentTimeMs) {
    if (!stream) return;

    int len;

    if (useTimestamp) {
        float timestamp = (currentTimeMs - startTimeMs) / 1000.0f;
        len = snprintf(buffer, sizeof(buffer),
                      "{\"id\":%d,\"value\":%.6f,\"timestamp\":%.6f}\n",
                      channelId, value, timestamp);
    } else {
        len = snprintf(buffer, sizeof(buffer),
                      "{\"id\":%d,\"value\":%.6f}\n",
                      channelId, value);
    }

    if (len > 0 && len < (int)sizeof(buffer)) {
        stream->write((const uint8_t*)buffer, len);
    }
}

void Plotter::send(uint8_t channelId, float value, float timestamp) {
    if (!stream) return;

    int len = snprintf(buffer, sizeof(buffer),
                      "{\"id\":%d,\"value\":%.6f,\"timestamp\":%.6f}\n",
                      channelId, value, timestamp);

    if (len > 0 && len < (int)sizeof(buffer)) {
        stream->write((const uint8_t*)buffer, len);
    }
}

void Plotter::send(uint8_t channelId, float value) {
    if (!stream) return;

    int len = snprintf(buffer, sizeof(buffer),
                      "{\"id\":%d,\"value\":%.6f}\n",
                      channelId, value);

    if (len > 0 && len < (int)sizeof(buffer)) {
        stream->write((const uint8_t*)buffer, len);
    }
}

void Plotter::setTimestampEnabled(bool enable) {
    useTimestamp = enable;
}

bool Plotter::isTimestampEnabled() const {
    return useTimestamp;
}
