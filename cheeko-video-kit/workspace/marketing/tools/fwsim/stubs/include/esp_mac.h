#pragma once
#include <stdint.h>
#include <string.h>
#include "esp_err.h"
typedef enum { ESP_MAC_WIFI_STA, ESP_MAC_WIFI_SOFTAP, ESP_MAC_BT, ESP_MAC_ETH, ESP_MAC_BASE } esp_mac_type_t;
static inline esp_err_t esp_read_mac(uint8_t *m, esp_mac_type_t t) { (void)t; const uint8_t d[6] = {0x24, 0x6f, 0x28, 0x12, 0x34, 0x56}; memcpy(m, d, 6); return ESP_OK; }
static inline esp_err_t esp_efuse_mac_get_default(uint8_t *m) { return esp_read_mac(m, ESP_MAC_BASE); }
#define MACSTR "%02x:%02x:%02x:%02x:%02x:%02x"
#define MAC2STR(a) (a)[0], (a)[1], (a)[2], (a)[3], (a)[4], (a)[5]
