#pragma once
#include "esp_err.h"
typedef struct fwsim_pm_lock *esp_pm_lock_handle_t;
typedef enum { ESP_PM_CPU_FREQ_MAX, ESP_PM_APB_FREQ_MAX, ESP_PM_NO_LIGHT_SLEEP } esp_pm_lock_type_t;
static inline esp_err_t esp_pm_lock_create(esp_pm_lock_type_t t, int a, const char *n, esp_pm_lock_handle_t *h) { (void)t; (void)a; (void)n; *h = 0; return ESP_OK; }
static inline esp_err_t esp_pm_lock_acquire(esp_pm_lock_handle_t h) { (void)h; return ESP_OK; }
static inline esp_err_t esp_pm_lock_release(esp_pm_lock_handle_t h) { (void)h; return ESP_OK; }
static inline esp_err_t esp_pm_lock_delete(esp_pm_lock_handle_t h) { (void)h; return ESP_OK; }
