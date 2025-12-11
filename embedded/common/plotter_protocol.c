/**
 * @file plotter_protocol.c
 * @brief PlotterApp Communication Protocol Implementation
 *
 * @version 1.0
 * @date 2025-12-10
 */

#include "plotter_protocol.h"
#include <stdio.h>
#include <math.h>

int plotter_format_json_with_timestamp(const PlotDataPoint* point,
                                       char* buffer,
                                       size_t buffer_size,
                                       uint8_t precision)
{
    if (point == NULL || buffer == NULL || buffer_size < PLOTTER_BUFFER_SIZE) {
        return -1;
    }

    // Validate data point
    if (!plotter_validate_point(point)) {
        return -1;
    }

    // Format JSON string with timestamp
    int len = snprintf(buffer, buffer_size,
                      "{\"id\":%d,\"value\":%.*f,\"timestamp\":%.*f}\n",
                      point->id,
                      precision, point->value,
                      precision, point->timestamp);

    // Check if snprintf succeeded and didn't truncate
    if (len < 0 || (size_t)len >= buffer_size) {
        return -1;
    }

    return len;
}

int plotter_format_json_no_timestamp(uint8_t id,
                                     float value,
                                     char* buffer,
                                     size_t buffer_size,
                                     uint8_t precision)
{
    if (buffer == NULL || buffer_size < PLOTTER_BUFFER_SIZE) {
        return -1;
    }

    // Validate ID
    if (id > 255) {
        return -1;
    }

    // Check for NaN or Inf
    if (isnan(value) || isinf(value)) {
        return -1;
    }

    // Format JSON string without timestamp
    int len = snprintf(buffer, buffer_size,
                      "{\"id\":%d,\"value\":%.*f}\n",
                      id,
                      precision, value);

    // Check if snprintf succeeded and didn't truncate
    if (len < 0 || (size_t)len >= buffer_size) {
        return -1;
    }

    return len;
}

int plotter_format_plain(float value,
                        char* buffer,
                        size_t buffer_size,
                        uint8_t precision)
{
    if (buffer == NULL || buffer_size < 64) {
        return -1;
    }

    // Check for NaN or Inf
    if (isnan(value) || isinf(value)) {
        return -1;
    }

    // Format plain value
    int len = snprintf(buffer, buffer_size,
                      "%.*f\n",
                      precision, value);

    // Check if snprintf succeeded and didn't truncate
    if (len < 0 || (size_t)len >= buffer_size) {
        return -1;
    }

    return len;
}

int plotter_validate_point(const PlotDataPoint* point)
{
    if (point == NULL) {
        return 0;
    }

    // Check ID range (0-255 automatically valid for uint8_t)
    // No need to check upper bound since uint8_t max is 255

    // Check for NaN or Inf in value
    if (isnan(point->value) || isinf(point->value)) {
        return 0;
    }

    // Check for NaN or Inf in timestamp
    if (isnan(point->timestamp) || isinf(point->timestamp)) {
        return 0;
    }

    return 1;
}

PlotDataPoint plotter_create_point(uint8_t id, float value, uint32_t time_ms)
{
    PlotDataPoint point;
    point.id = id;
    point.value = value;
    point.timestamp = time_ms / 1000.0f;  // Convert milliseconds to seconds
    return point;
}
