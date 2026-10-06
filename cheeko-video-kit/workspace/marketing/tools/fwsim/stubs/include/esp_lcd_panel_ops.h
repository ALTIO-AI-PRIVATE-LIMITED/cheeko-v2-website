#pragma once
#include "esp_lcd_types.h"
static inline esp_err_t esp_lcd_panel_draw_bitmap(esp_lcd_panel_handle_t p, int x0, int y0, int x1, int y1, const void *d) { (void)p; (void)x0; (void)y0; (void)x1; (void)y1; (void)d; return ESP_OK; }
static inline esp_err_t esp_lcd_panel_disp_on_off(esp_lcd_panel_handle_t p, bool on) { (void)p; (void)on; return ESP_OK; }
static inline esp_err_t esp_lcd_panel_del(esp_lcd_panel_handle_t p) { (void)p; return ESP_OK; }
static inline esp_err_t esp_lcd_panel_invert_color(esp_lcd_panel_handle_t p, bool on) { (void)p; (void)on; return ESP_OK; }
static inline esp_err_t esp_lcd_panel_mirror(esp_lcd_panel_handle_t p, bool x, bool y) { (void)p; (void)x; (void)y; return ESP_OK; }
static inline esp_err_t esp_lcd_panel_swap_xy(esp_lcd_panel_handle_t p, bool s) { (void)p; (void)s; return ESP_OK; }
