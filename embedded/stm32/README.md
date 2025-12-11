# STM32 Examples for PlotterApp

Professional microcontroller examples using the Plotter library for high-performance data acquisition.

## 📋 Requirements

- STM32 board (STM32F4, F7, H7, G4, etc.)
- STM32CubeIDE or STM32CubeMX + IDE
- USB cable or USB-to-Serial adapter

## 📁 Examples

### 1. USB CDC Example
**File:** `usb_cdc_example/main.c`

Stream data via USB CDC (Virtual COM Port) using the Plotter library.

**Advantages:**
✅ No external hardware needed
✅ High speed (up to 12 Mbps for Full Speed USB)
✅ No baud rate limitations
✅ Clean single-cable solution

**Supported Boards:**
- STM32F4 Discovery
- STM32F7 Nucleo
- STM32H7 boards
- Any STM32 with USB peripheral

---

### 2. UART Example
**File:** `uart_example/main.c`

Stream data via UART/Serial using the Plotter library.

**Advantages:**
✅ Works on all STM32 boards
✅ Long cable distances possible
✅ Galvanic isolation possible
✅ Simple hardware

**Hardware Needed:**
- USB-to-Serial adapter (FTDI, CH340, CP2102)

---

## 🔧 Setup Instructions

### 1. Create STM32CubeIDE Project

#### For USB CDC Example:

1. **Create New Project**
   - File → New → STM32 Project
   - Select your board/MCU
   - Name: "PlotterApp_USB_CDC"

2. **Configure in CubeMX (.ioc file)**
   - **Connectivity → USB_OTG_FS**: Device Only
   - **Middleware → USB_DEVICE**: Communication Device Class (CDC)
   - **Analog → ADC1**: Enable at least 1 channel (e.g., IN0)
   - **Clock Configuration**: Ensure USB clock is 48 MHz

3. **Generate Code**
   - Project → Generate Code

#### For UART Example:

1. **CubeMX Configuration**
   - **Connectivity → USART2** (or USART1, etc.)
   - Mode: Asynchronous
   - Baud Rate: 115200
   - Word Length: 8 Bits
   - Parity: None
   - Stop Bits: 1
   - **Analog → ADC1**: Enable channel

2. **Hardware Connections**
   ```
   STM32 TX (PA2) → RX of USB-Serial adapter
   STM32 RX (PA3) → TX of USB-Serial adapter
   STM32 GND      → GND of adapter
   ```

### 2. Add Plotter Library

1. **Copy files to project**:
   - Copy `plotter.h` and `plotter.cpp` from `embedded/common/` to your project's `Core/Src/` and `Core/Inc/`

2. **For C projects**: Rename `plotter.cpp` → `plotter.c`

3. **Add to project**:
   - Right-click project → Refresh
   - Files should appear in Project Explorer

### 3. Replace main.c

Replace the generated `main.c` with the example code from `usb_cdc_example/main.c` or `uart_example/main.c`.

Adjust paths:
```c
#include "plotter.h"  // Instead of "../../common/plotter.h"
```

### 4. Build & Flash

1. **Build**: Project → Build Project (Ctrl+B)
2. **Flash**: Run → Run (F11)
3. **Verify**: Check Serial Monitor or STM32CubeMonitor

### 5. Connect in PlotterApp

**For USB CDC:**
1. Connections → New → Serial
2. Select new COM port (e.g., COM5)
3. Baud: 115200 (doesn't matter for USB CDC but required)
4. Start connection

**For UART:**
1. Connections → New → Serial
2. Select USB-Serial adapter COM port
3. Baud: 115200
4. Start connection

---

## 💻 Using the Plotter Library

### Basic Setup (C)

```c
#include "main.h"
#include "usbd_cdc_if.h"  // For USB CDC
#include "plotter.h"

Plotter plotter;

// Send function for USB CDC
void usbSend(const char* data, uint16_t length) {
    CDC_Transmit_FS((uint8_t*)data, length);
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_USB_DEVICE_Init();
    MX_ADC1_Init();

    // Initialize plotter
    plotter_init(&plotter, usbSend, 1);  // 1 = use timestamps
    plotter_set_start_time(&plotter, HAL_GetTick());

    while (1) {
        // Main loop
    }
}
```

### Sending Data

```c
while (1) {
    uint32_t currentTime = HAL_GetTick();

    // Read ADC
    HAL_ADC_Start(&hadc1);
    if (HAL_ADC_PollForConversion(&hadc1, 10) == HAL_OK) {
        uint32_t rawValue = HAL_ADC_GetValue(&hadc1);
        float voltage = (rawValue / 4095.0f) * 3.3f;

        // Send data point on channel 0
        plotter_send(&plotter, 0, voltage, currentTime);
    }
    HAL_ADC_Stop(&hadc1);

    HAL_Delay(20);  // 50 Hz
}
```

### Multiple Channels

```c
while (1) {
    uint32_t currentTime = HAL_GetTick();

    // Read multiple channels
    float ch0 = readChannel(0);
    float ch1 = readChannel(1);

    // Send both with same timestamp
    plotter_send(&plotter, 0, ch0, currentTime);
    plotter_send(&plotter, 1, ch1, currentTime);

    HAL_Delay(50);
}
```

---

## 📊 Performance

### Typical Sample Rates:
- **USB CDC**: Up to 1000 Hz sampling
- **UART 115200**: Up to 200 Hz sampling
- **UART 921600**: Up to 500 Hz sampling

### With DMA:
- **USB CDC + DMA**: Up to 5000 Hz possible
- **ADC DMA circular**: Continuous high-speed acquisition

---

## 🚀 Advanced: DMA for High-Speed

### Enable ADC DMA in CubeMX:
1. ADC1 → DMA Settings → Add
2. DMA Request: ADC1
3. Mode: Circular
4. Data Width: Word

### Code Example:

```c
#define ADC_BUFFER_SIZE 100
uint32_t adcBuffer[ADC_BUFFER_SIZE];

void setup_adc_dma() {
    HAL_ADC_Start_DMA(&hadc1, adcBuffer, ADC_BUFFER_SIZE);
}

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    uint32_t currentTime = HAL_GetTick();

    // Process complete buffer
    for(int i = 0; i < ADC_BUFFER_SIZE; i++) {
        float voltage = (adcBuffer[i] / 4095.0f) * 3.3f;
        plotter_send(&plotter, 0, voltage, currentTime);
    }
}
```

---

## 🛠️ Troubleshooting

### USB CDC not recognized?

1. **Check USB cable** - Must be data cable, not charge-only
2. **Install STM32 VCP driver** - Usually auto-installs on Windows 10+
3. **Check CubeMX clock** - USB needs exactly 48 MHz
4. **Verify USB_DEVICE middleware** - Must be enabled in CubeMX
5. **Check Device Manager** - Should show "STM32 Virtual COM Port"

### UART not working?

1. **Check TX/RX crossover** - STM32 TX → Adapter RX, STM32 RX → Adapter TX
2. **Verify baud rate** - Must match in code and PlotterApp (115200)
3. **Check voltage levels** - STM32 is 3.3V, ensure adapter is compatible
4. **Test with loopback** - Connect TX to RX, should echo data

### No data in PlotterApp?

1. **Check Serial Monitor** - Open STM32CubeMonitor or PuTTY to see raw data
2. **Verify JSON format** - Should be: `{"id":0,"value":1.23,"timestamp":0.5}`
3. **Check COM port** - Use correct port in PlotterApp
4. **Reduce sample rate** - Try 10 Hz (100ms delay) first

### Compilation errors?

1. **"plotter.h not found"** - Copy plotter.h to `Core/Inc/`
2. **"undefined reference"** - Copy plotter.c to `Core/Src/` and rebuild
3. **CDC_Transmit_FS undefined** - Ensure USB_DEVICE middleware is enabled

---

## 💡 Tips

### Optimize USB CDC Performance:

Edit `usbd_cdc_if.c`:
```c
#define APP_TX_DATA_SIZE 2048  // Increase from default 512
```

### Use UART DMA for Better Performance:

```c
char buffer[64];
int len = snprintf(buffer, sizeof(buffer),
                  "{\"id\":0,\"value\":%.3f}\n", value);
HAL_UART_Transmit_DMA(&huart2, (uint8_t*)buffer, len);
```

### Multi-Channel Best Practice:

```c
uint32_t currentTime = HAL_GetTick();

// Read all sensors first
float sensor1 = readSensor1();
float sensor2 = readSensor2();

// Send all with same timestamp
plotter_send(&plotter, 0, sensor1, currentTime);
plotter_send(&plotter, 1, sensor2, currentTime);
```

---

## 📚 STM32CubeMX Configuration Checklist

### For USB CDC:
- ✅ USB_OTG_FS → Device Only
- ✅ USB_DEVICE → CDC class
- ✅ USB clock = 48 MHz
- ✅ ADC configured

### For UART:
- ✅ USART mode = Asynchronous
- ✅ Baud rate = 115200
- ✅ 8N1 settings
- ✅ GPIO pins configured

---

## 🔗 Resources

- [STM32CubeIDE Download](https://www.st.com/en/development-tools/stm32cubeide.html)
- [STM32CubeMX Manual](https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf)
- [HAL Driver Documentation](https://www.st.com/resource/en/user_manual/dm00105879-description-of-stm32f4-hal-and-ll-drivers-stmicroelectronics.pdf)
- [PlotterApp Documentation](../../README.md)

---

## 💡 Next Steps

1. **Start with USB CDC example** - Easiest setup
2. **Test with slow sample rate** - 10 Hz first
3. **Enable DMA** - For high-speed applications
4. **Add real sensors** - I2C, SPI, etc.
5. **Optimize performance** - Buffer, DMA, interrupts
