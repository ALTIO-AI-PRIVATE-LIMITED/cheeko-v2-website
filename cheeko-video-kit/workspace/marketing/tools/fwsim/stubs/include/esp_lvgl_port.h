#pragma once
// Host stand-in for espressif/esp_lvgl_port: lvgl_port_add_disp() creates an
// lv_display whose flush callback copies into the simulator framebuffer.
#include "esp_err.h"
#include "esp_lcd_types.h"
#include "lvgl.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct {
  int task_priority;
  int task_stack;
  int task_affinity;
  int task_max_sleep_ms;
  unsigned task_stack_caps;
  int timer_period_ms;
} lvgl_port_cfg_t;
#define ESP_LVGL_PORT_INIT_CONFIG() { .task_priority = 4, .task_stack = 7168, .task_affinity = -1, .task_max_sleep_ms = 500, .task_stack_caps = 0, .timer_period_ms = 5 }
typedef struct {
  esp_lcd_panel_io_handle_t io_handle;
  esp_lcd_panel_handle_t panel_handle;
  esp_lcd_panel_handle_t control_handle;
  uint32_t buffer_size;
  bool double_buffer;
  uint32_t trans_size;
  uint32_t hres;
  uint32_t vres;
  bool monochrome;
  struct { bool swap_xy; bool mirror_x; bool mirror_y; } rotation;
  lv_color_format_t color_format;
  struct {
    unsigned int buff_dma : 1;
    unsigned int buff_spiram : 1;
    unsigned int sw_rotate : 1;
    unsigned int swap_bytes : 1;
    unsigned int full_refresh : 1;
    unsigned int direct_mode : 1;
  } flags;
} lvgl_port_display_cfg_t;
typedef struct { struct { unsigned bb_mode:1; unsigned avoid_tearing:1; } flags; } lvgl_port_display_rgb_cfg_t;
typedef struct { struct { unsigned avoid_tearing:1; } flags; } lvgl_port_display_dsi_cfg_t;
static inline lv_display_t *lvgl_port_add_disp_rgb(const lvgl_port_display_cfg_t *a, const lvgl_port_display_rgb_cfg_t *b) { (void)a; (void)b; return NULL; }
static inline lv_display_t *lvgl_port_add_disp_dsi(const lvgl_port_display_cfg_t *a, const lvgl_port_display_dsi_cfg_t *b) { (void)a; (void)b; return NULL; }
esp_err_t lvgl_port_init(const lvgl_port_cfg_t *cfg);
lv_display_t *lvgl_port_add_disp(const lvgl_port_display_cfg_t *cfg);
bool lvgl_port_lock(uint32_t timeout_ms);
void lvgl_port_unlock(void);
esp_err_t lvgl_port_stop(void);
esp_err_t lvgl_port_resume(void);
esp_err_t lvgl_port_remove_disp(lv_display_t *d);
#ifdef __cplusplus
}
#endif
