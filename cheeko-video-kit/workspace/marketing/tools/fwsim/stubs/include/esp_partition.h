#pragma once
#include <stdint.h>
#include <stddef.h>
#include "esp_err.h"
typedef enum { ESP_PARTITION_TYPE_APP = 0, ESP_PARTITION_TYPE_DATA = 1, ESP_PARTITION_TYPE_ANY = 0xff } esp_partition_type_t;
typedef enum { ESP_PARTITION_SUBTYPE_APP_FACTORY = 0, ESP_PARTITION_SUBTYPE_APP_OTA_0 = 0x10, ESP_PARTITION_SUBTYPE_APP_OTA_1 = 0x11, ESP_PARTITION_SUBTYPE_DATA_OTA = 0, ESP_PARTITION_SUBTYPE_ANY = 0xff } esp_partition_subtype_t;
typedef struct { void *flash_chip; esp_partition_type_t type; esp_partition_subtype_t subtype; uint32_t address; uint32_t size; uint32_t erase_size; char label[17]; bool encrypted; bool readonly; } esp_partition_t;
typedef struct fwsim_part_it *esp_partition_iterator_t;
static inline const esp_partition_t *esp_partition_find_first(esp_partition_type_t t, esp_partition_subtype_t s, const char *l) { (void)t; (void)s; (void)l; return NULL; }
static inline esp_err_t esp_partition_read(const esp_partition_t *p, size_t o, void *d, size_t n) { (void)p; (void)o; (void)d; (void)n; return ESP_FAIL; }
