#pragma once
#include "esp_err.h"
#include "esp_partition.h"
#include "esp_app_desc.h"
typedef uint32_t esp_ota_handle_t;
typedef enum { ESP_OTA_IMG_NEW, ESP_OTA_IMG_PENDING_VERIFY, ESP_OTA_IMG_VALID, ESP_OTA_IMG_INVALID, ESP_OTA_IMG_ABORTED, ESP_OTA_IMG_UNDEFINED = -1 } esp_ota_img_states_t;
static inline const esp_partition_t *esp_ota_get_running_partition(void) { return NULL; }
static inline const esp_partition_t *esp_ota_get_boot_partition(void) { return NULL; }
static inline const esp_partition_t *esp_ota_get_next_update_partition(const esp_partition_t *p) { (void)p; return NULL; }
static inline esp_err_t esp_ota_get_state_partition(const esp_partition_t *p, esp_ota_img_states_t *s) { (void)p; *s = ESP_OTA_IMG_VALID; return ESP_OK; }
static inline esp_err_t esp_ota_get_partition_description(const esp_partition_t *p, esp_app_desc_t *d) { (void)p; (void)d; return ESP_FAIL; }
static inline esp_err_t esp_ota_mark_app_valid_cancel_rollback(void) { return ESP_OK; }
