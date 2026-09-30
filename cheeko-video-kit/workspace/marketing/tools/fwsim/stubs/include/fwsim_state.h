#pragma once
// Scenario state the stubs report to the firmware UI (battery, Wi-Fi, clock).
#include <cstdint>
class Display;
constexpr int FWSIM_W = 296;
constexpr int FWSIM_H = 240;
struct FwsimState {
  int64_t now_us = 1000000;          // monotonic (esp_timer / lv_tick)
  int64_t wall_epoch = 0;            // wall clock seconds at now_us == 0
  Display *display = nullptr;
  const char *network_icon = nullptr;
  int battery_level = 80;
  bool charging = false;
  int battery_mv = 3950;
  bool fire_esp_timers = true;
};
extern FwsimState g_fwsim;
extern uint16_t g_fwsim_fb[FWSIM_H][FWSIM_W];
void fwsim_run_esp_timers();
void fwsim_nvs_set_int(const char *ns, const char *key, int64_t v);
void fwsim_nvs_set_str(const char *ns, const char *key, const char *v);
void fwsim_nvs_erase(const char *ns, const char *key);
