#pragma once
#include <stdio.h>
#include <stdlib.h>
#ifdef __cplusplus
extern "C" {
#endif
int fwsim_log_enabled(void);
#ifdef __cplusplus
}
#endif
#define FWSIM_LOG(lvl, tag, fmt, ...) do { if (fwsim_log_enabled()) fprintf(stderr, lvl " (%s) " fmt "\n", tag, ##__VA_ARGS__); } while (0)
#define ESP_LOGE(tag, fmt, ...) FWSIM_LOG("E", tag, fmt, ##__VA_ARGS__)
#define ESP_LOGW(tag, fmt, ...) FWSIM_LOG("W", tag, fmt, ##__VA_ARGS__)
#define ESP_LOGI(tag, fmt, ...) FWSIM_LOG("I", tag, fmt, ##__VA_ARGS__)
#define ESP_LOGD(tag, fmt, ...) do {} while (0)
#define ESP_LOGV(tag, fmt, ...) do {} while (0)
#define ESP_EARLY_LOGI ESP_LOGI
#define ESP_EARLY_LOGW ESP_LOGW
#define ESP_EARLY_LOGE ESP_LOGE
#define ESP_LOG_BUFFER_HEX(...) do {} while (0)
#define ESP_LOG_BUFFER_HEXDUMP(...) do {} while (0)
typedef enum { ESP_LOG_NONE, ESP_LOG_ERROR, ESP_LOG_WARN, ESP_LOG_INFO, ESP_LOG_DEBUG, ESP_LOG_VERBOSE } esp_log_level_t;
static inline void esp_log_level_set(const char *t, esp_log_level_t l) { (void)t; (void)l; }
