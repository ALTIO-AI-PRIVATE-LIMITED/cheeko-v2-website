// Force-included into every firmware C++ TU of the host simulator.
#pragma once
#include "sdkconfig.h"
#ifndef IRAM_ATTR
#define IRAM_ATTR
#endif
#define EXT_RAM_BSS_ATTR
#define EXT_RAM_NOINIT_ATTR
#define DRAM_ATTR
#define RTC_NOINIT_ATTR
#define RTC_DATA_ATTR
#define ESP_PLATFORM_SIM 1
#include <esp_heap_caps.h>
