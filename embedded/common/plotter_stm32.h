/**
 * @file plotter_stm32.h
 * @brief STM32-specific PlotterStream implementations
 *
 * Provides stream adapters for STM32 HAL USB CDC and UART.
 *
 * @version 4.0
 * @date 2025-12-11
 */

#ifndef PLOTTER_STM32_H
#define PLOTTER_STM32_H

#include "plotter.h"

#ifdef STM32
// STM32 HAL headers must be included before this file
// #include "main.h"
// #include "usbd_cdc_if.h"  // For USB CDC

/**
 * @brief PlotterStream implementation for STM32 USB CDC
 *
 * Example:
 * @code
 * CDCStream usbStream;
 * Plotter plotter(usbStream);
 * @endcode
 */
class CDCStream : public PlotterStream {
public:
    /**
     * @brief Default constructor
     */
    CDCStream() {}

    /**
     * @brief Write data via USB CDC
     *
     * @param data Pointer to data buffer
     * @param length Number of bytes to write
     * @return Number of bytes written (0 on error)
     */
    size_t write(const uint8_t* data, size_t length) override {
        // CDC_Transmit_FS returns USBD_OK (0) on success
        // We return the length if successful, 0 otherwise
        extern uint8_t CDC_Transmit_FS(uint8_t* Buf, uint16_t Len);
        if (CDC_Transmit_FS((uint8_t*)data, length) == 0) {
            return length;
        }
        return 0;
    }
};

/**
 * @brief PlotterStream implementation for STM32 UART
 *
 * Example:
 * @code
 * extern UART_HandleTypeDef huart2;
 * UARTStream uartStream(huart2);
 * Plotter plotter(uartStream);
 * @endcode
 */
class UARTStream : public PlotterStream {
private:
    void* huart;  // UART_HandleTypeDef* stored as void* to avoid HAL dependency in header
    uint32_t timeout;

public:
    /**
     * @brief Construct UART stream
     *
     * @param huart_handle Reference to UART_HandleTypeDef
     * @param txTimeout Transmit timeout in milliseconds (default: 100ms)
     */
    UARTStream(void* huart_handle, uint32_t txTimeout = 100)
        : huart(huart_handle), timeout(txTimeout) {}

    /**
     * @brief Write data via UART
     *
     * @param data Pointer to data buffer
     * @param length Number of bytes to write
     * @return Number of bytes written
     */
    size_t write(const uint8_t* data, size_t length) override {
        extern int HAL_UART_Transmit(void* huart, uint8_t* pData, uint16_t Size, uint32_t Timeout);
        if (HAL_UART_Transmit(huart, (uint8_t*)data, length, timeout) == 0) { // HAL_OK = 0
            return length;
        }
        return 0;
    }
};

#endif // STM32

#endif // PLOTTER_STM32_H
