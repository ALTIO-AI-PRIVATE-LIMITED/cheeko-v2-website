#pragma once
#include <stdint.h>
#include <stddef.h>
#include "esp_err.h"
typedef uint32_t nvs_handle_t;
typedef enum { NVS_READONLY, NVS_READWRITE } nvs_open_mode_t;
typedef nvs_open_mode_t nvs_open_mode;
#ifdef __cplusplus
extern "C" {
#endif
esp_err_t nvs_open(const char *ns, nvs_open_mode_t m, nvs_handle_t *h);
void nvs_close(nvs_handle_t h);
esp_err_t nvs_commit(nvs_handle_t h);
esp_err_t nvs_erase_key(nvs_handle_t h, const char *k);
esp_err_t nvs_erase_all(nvs_handle_t h);
esp_err_t nvs_get_str(nvs_handle_t h, const char *k, char *out, size_t *len);
esp_err_t nvs_set_str(nvs_handle_t h, const char *k, const char *v);
esp_err_t nvs_get_blob(nvs_handle_t h, const char *k, void *out, size_t *len);
esp_err_t nvs_set_blob(nvs_handle_t h, const char *k, const void *v, size_t len);
esp_err_t nvs_get_i8(nvs_handle_t h, const char *k, int8_t *v);
esp_err_t nvs_set_i8(nvs_handle_t h, const char *k, int8_t v);
esp_err_t nvs_get_u8(nvs_handle_t h, const char *k, uint8_t *v);
esp_err_t nvs_set_u8(nvs_handle_t h, const char *k, uint8_t v);
esp_err_t nvs_get_i16(nvs_handle_t h, const char *k, int16_t *v);
esp_err_t nvs_set_i16(nvs_handle_t h, const char *k, int16_t v);
esp_err_t nvs_get_u16(nvs_handle_t h, const char *k, uint16_t *v);
esp_err_t nvs_set_u16(nvs_handle_t h, const char *k, uint16_t v);
esp_err_t nvs_get_i32(nvs_handle_t h, const char *k, int32_t *v);
esp_err_t nvs_set_i32(nvs_handle_t h, const char *k, int32_t v);
esp_err_t nvs_get_u32(nvs_handle_t h, const char *k, uint32_t *v);
esp_err_t nvs_set_u32(nvs_handle_t h, const char *k, uint32_t v);
esp_err_t nvs_get_i64(nvs_handle_t h, const char *k, int64_t *v);
esp_err_t nvs_set_i64(nvs_handle_t h, const char *k, int64_t v);
esp_err_t nvs_get_u64(nvs_handle_t h, const char *k, uint64_t *v);
esp_err_t nvs_set_u64(nvs_handle_t h, const char *k, uint64_t v);
#ifdef __cplusplus
}
#endif
