#pragma once
#include <stddef.h>
static inline size_t esp_psram_get_size(void) { return 8u * 1024 * 1024; }
static inline int esp_psram_is_initialized(void) { return 1; }
