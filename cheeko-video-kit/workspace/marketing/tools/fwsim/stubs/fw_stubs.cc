// Host implementations of the ESP-IDF / board / service APIs the Cheeko UI
// code calls. Everything here is deliberately inert: no audio, no network, no
// tasks. Anything that affects what is DRAWN (battery, Wi-Fi, clock, device
// state) is read from fwsim_state so the harness can set it per scenario.
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <functional>
#include <map>
#include <string>
#include <vector>

#include "application.h"
#include "board.h"
#include "cheeko_analytics.h"
#include "cheeko_audio_session.h"
#include "cheeko_parent_app_sync.h"
#include "cheeko_telemetry.h"
#include "fwsim_state.h"
#include "ota.h"
#include "radio_player.h"
#include "system_info.h"
#include "wifi_manager.h"
#include <font_awesome.h>

#include <esp_app_desc.h>
#include <esp_lvgl_port.h>
#include <esp_timer.h>
#include <freertos/FreeRTOS.h>
#include <nvs.h>

FwsimState g_fwsim;

extern "C" int fwsim_log_enabled(void) {
  static int on = getenv("FWSIM_LOG") != nullptr;
  return on;
}

// ---------------------------------------------------------------- clock
extern "C" int64_t esp_timer_get_time(void) { return g_fwsim.now_us; }
extern "C" TickType_t xTaskGetTickCount(void) {
  return (TickType_t)(g_fwsim.now_us / 1000);
}

struct fwsim_esp_timer {
  esp_timer_create_args_t args;
  bool active = false;
  bool periodic = false;
  int64_t period_us = 0;
  int64_t due_us = 0;
};
static std::vector<fwsim_esp_timer *> g_esp_timers;

extern "C" esp_err_t esp_timer_create(const esp_timer_create_args_t *args,
                                      esp_timer_handle_t *out) {
  auto *t = new fwsim_esp_timer();
  t->args = *args;
  g_esp_timers.push_back(t);
  *out = t;
  return ESP_OK;
}
extern "C" esp_err_t esp_timer_start_once(esp_timer_handle_t t, uint64_t us) {
  t->active = true; t->periodic = false; t->due_us = g_fwsim.now_us + us;
  return ESP_OK;
}
extern "C" esp_err_t esp_timer_start_periodic(esp_timer_handle_t t, uint64_t us) {
  t->active = true; t->periodic = true; t->period_us = us; t->due_us = g_fwsim.now_us + us;
  return ESP_OK;
}
extern "C" esp_err_t esp_timer_restart(esp_timer_handle_t t, uint64_t us) {
  return t->periodic ? esp_timer_start_periodic(t, us) : esp_timer_start_once(t, us);
}
extern "C" esp_err_t esp_timer_stop(esp_timer_handle_t t) {
  if (t) t->active = false;
  return ESP_OK;
}
extern "C" esp_err_t esp_timer_delete(esp_timer_handle_t t) {
  for (auto &p : g_esp_timers) if (p == t) p = nullptr;
  delete t;
  return ESP_OK;
}
extern "C" bool esp_timer_is_active(esp_timer_handle_t t) { return t && t->active; }

// Fired from the harness pump (ESP_TIMER_TASK callbacks run on the same
// "thread" as LVGL here, which is fine: they take the display lock, which is
// a no-op).
void fwsim_run_esp_timers() {
  for (size_t i = 0; i < g_esp_timers.size(); ++i) {
    auto *t = g_esp_timers[i];
    if (t == nullptr || !t->active || t->due_us > g_fwsim.now_us) continue;
    if (t->periodic) t->due_us += t->period_us; else t->active = false;
    if (g_fwsim.fire_esp_timers && t->args.callback) t->args.callback(t->args.arg);
  }
}

// ---------------------------------------------------------------- misc esp
extern "C" uint32_t esp_random(void) {
  // Deterministic so re-runs produce identical screens.
  static uint32_t s = 0x12345678;
  s ^= s << 13; s ^= s >> 17; s ^= s << 5;
  return s;
}
extern "C" void esp_fill_random(void *buf, size_t len) {
  auto *p = static_cast<uint8_t *>(buf);
  for (size_t i = 0; i < len; ++i) p[i] = (uint8_t)esp_random();
}
extern "C" void esp_restart(void) {
  fprintf(stderr, "[fwsim] esp_restart() called - ignored\n");
}
extern "C" const esp_app_desc_t *esp_app_get_description(void) {
  static esp_app_desc_t d = [] {
    esp_app_desc_t x{};
    snprintf(x.version, sizeof(x.version), "%s", FWSIM_PROJECT_VER);
    snprintf(x.project_name, sizeof(x.project_name), "xiaozhi");
    snprintf(x.date, sizeof(x.date), "Sep 28 2026");
    snprintf(x.time, sizeof(x.time), "12:00:00");
    return x;
  }();
  return &d;
}

// ---------------------------------------------------------------- FreeRTOS
// Tasks are never started: the simulator is single-threaded and the UI code
// under test only spawns background work (downloads, audio, updates).
extern "C" {
BaseType_t xTaskCreate(TaskFunction_t, const char *n, uint32_t, void *, UBaseType_t, TaskHandle_t *h) {
  if (fwsim_log_enabled()) fprintf(stderr, "[fwsim] xTaskCreate(%s) not run\n", n);
  if (h) *h = (TaskHandle_t)0x1;
  return pdPASS;
}
BaseType_t xTaskCreatePinnedToCore(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, TaskHandle_t *h, BaseType_t) { return xTaskCreate(f, n, s, a, p, h); }
BaseType_t xTaskCreateWithCaps(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, TaskHandle_t *h, uint32_t) { return xTaskCreate(f, n, s, a, p, h); }
BaseType_t xTaskCreatePinnedToCoreWithCaps(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, TaskHandle_t *h, BaseType_t, uint32_t) { return xTaskCreate(f, n, s, a, p, h); }
TaskHandle_t xTaskCreateStatic(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, StackType_t *, StaticTask_t *) { TaskHandle_t h; xTaskCreate(f, n, s, a, p, &h); return h; }
TaskHandle_t xTaskCreateStaticPinnedToCore(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, StackType_t *st, StaticTask_t *tb, BaseType_t) { return xTaskCreateStatic(f, n, s, a, p, st, tb); }
void vTaskDelete(TaskHandle_t) {}
void vTaskDeleteWithCaps(TaskHandle_t) {}
void vTaskDelay(TickType_t) {}
void vTaskSuspend(TaskHandle_t) {}
void vTaskResume(TaskHandle_t) {}
TaskHandle_t xTaskGetCurrentTaskHandle(void) { return (TaskHandle_t)0x2; }
UBaseType_t uxTaskGetStackHighWaterMark(TaskHandle_t) { return 4096; }
UBaseType_t uxTaskPriorityGet(TaskHandle_t) { return 5; }
void vTaskPrioritySet(TaskHandle_t, UBaseType_t) {}
eTaskState eTaskGetState(TaskHandle_t) { return eDeleted; }
const char *pcTaskGetName(TaskHandle_t) { return "main"; }
BaseType_t xTaskNotifyGive(TaskHandle_t) { return pdPASS; }
uint32_t ulTaskNotifyTake(BaseType_t, TickType_t) { return 1; }
BaseType_t xTaskNotify(TaskHandle_t, uint32_t, eNotifyAction) { return pdPASS; }
BaseType_t xTaskNotifyWait(uint32_t, uint32_t, uint32_t *v, TickType_t) { if (v) *v = 0; return pdFALSE; }
void vTaskList(char *buf) { if (buf) buf[0] = 0; }
UBaseType_t uxTaskGetNumberOfTasks(void) { return 1; }
SemaphoreHandle_t xSemaphoreCreateMutex(void) { return (SemaphoreHandle_t)new int(1); }
SemaphoreHandle_t xSemaphoreCreateRecursiveMutex(void) { return xSemaphoreCreateMutex(); }
SemaphoreHandle_t xSemaphoreCreateBinary(void) { return xSemaphoreCreateMutex(); }
SemaphoreHandle_t xSemaphoreCreateCounting(UBaseType_t, UBaseType_t) { return xSemaphoreCreateMutex(); }
SemaphoreHandle_t xSemaphoreCreateMutexStatic(StaticSemaphore_t *) { return xSemaphoreCreateMutex(); }
SemaphoreHandle_t xSemaphoreCreateBinaryStatic(StaticSemaphore_t *) { return xSemaphoreCreateMutex(); }
BaseType_t xSemaphoreTake(SemaphoreHandle_t, TickType_t) { return pdTRUE; }
BaseType_t xSemaphoreGive(SemaphoreHandle_t) { return pdTRUE; }
BaseType_t xSemaphoreTakeRecursive(SemaphoreHandle_t, TickType_t) { return pdTRUE; }
BaseType_t xSemaphoreGiveRecursive(SemaphoreHandle_t) { return pdTRUE; }
BaseType_t xSemaphoreGiveFromISR(SemaphoreHandle_t, BaseType_t *) { return pdTRUE; }
void vSemaphoreDelete(SemaphoreHandle_t s) { delete (int *)s; }
UBaseType_t uxSemaphoreGetCount(SemaphoreHandle_t) { return 1; }
QueueHandle_t xQueueCreate(UBaseType_t, UBaseType_t) { return (QueueHandle_t)new int(0); }
BaseType_t xQueueSend(QueueHandle_t, const void *, TickType_t) { return pdTRUE; }
BaseType_t xQueueSendToBack(QueueHandle_t, const void *, TickType_t) { return pdTRUE; }
BaseType_t xQueueSendFromISR(QueueHandle_t, const void *, BaseType_t *) { return pdTRUE; }
BaseType_t xQueueOverwrite(QueueHandle_t, const void *) { return pdTRUE; }
BaseType_t xQueueReceive(QueueHandle_t, void *, TickType_t) { return pdFALSE; }
BaseType_t xQueueReset(QueueHandle_t) { return pdTRUE; }
UBaseType_t uxQueueMessagesWaiting(QueueHandle_t) { return 0; }
void vQueueDelete(QueueHandle_t q) { delete (int *)q; }
EventGroupHandle_t xEventGroupCreate(void) { return (EventGroupHandle_t)new uint32_t(0); }
EventBits_t xEventGroupSetBits(EventGroupHandle_t g, EventBits_t b) { return *(uint32_t *)g |= b; }
EventBits_t xEventGroupClearBits(EventGroupHandle_t g, EventBits_t b) { EventBits_t o = *(uint32_t *)g; *(uint32_t *)g &= ~b; return o; }
EventBits_t xEventGroupGetBits(EventGroupHandle_t g) { return *(uint32_t *)g; }
EventBits_t xEventGroupWaitBits(EventGroupHandle_t g, EventBits_t, BaseType_t, BaseType_t, TickType_t) { return *(uint32_t *)g; }
void vEventGroupDelete(EventGroupHandle_t g) { delete (uint32_t *)g; }
RingbufHandle_t xRingbufferCreate(size_t, RingbufferType_t) { return (RingbufHandle_t)new int(0); }
RingbufHandle_t xRingbufferCreateWithCaps(size_t s, RingbufferType_t t, uint32_t) { return xRingbufferCreate(s, t); }
void vRingbufferDelete(RingbufHandle_t r) { delete (int *)r; }
void vRingbufferDeleteWithCaps(RingbufHandle_t r) { delete (int *)r; }
BaseType_t xRingbufferSend(RingbufHandle_t, const void *, size_t, TickType_t) { return pdTRUE; }
void *xRingbufferReceive(RingbufHandle_t, size_t *n, TickType_t) { if (n) *n = 0; return nullptr; }
void *xRingbufferReceiveUpTo(RingbufHandle_t, size_t *n, TickType_t, size_t) { if (n) *n = 0; return nullptr; }
void vRingbufferReturnItem(RingbufHandle_t, void *) {}
size_t xRingbufferGetCurFreeSize(RingbufHandle_t) { return 0; }
}

// ---------------------------------------------------------------- NVS (RAM)
namespace {
struct NvsNs {
  std::map<std::string, std::string> str;
  std::map<std::string, int64_t> num;
};
std::map<std::string, NvsNs> &NvsStore() {
  static std::map<std::string, NvsNs> s;
  return s;
}
std::vector<std::string> &NvsHandles() {
  static std::vector<std::string> h{""};
  return h;
}
NvsNs &Ns(nvs_handle_t h) { return NvsStore()[NvsHandles()[h]]; }
template <typename T> esp_err_t GetNum(nvs_handle_t h, const char *k, T *v) {
  auto &m = Ns(h).num;
  auto it = m.find(k);
  if (it == m.end()) return ESP_ERR_NVS_NOT_FOUND;
  *v = (T)it->second;
  return ESP_OK;
}
template <typename T> esp_err_t SetNum(nvs_handle_t h, const char *k, T v) {
  Ns(h).num[k] = (int64_t)v;
  return ESP_OK;
}
}  // namespace
void fwsim_nvs_set_int(const char *ns, const char *key, int64_t v) { NvsStore()[ns].num[key] = v; }
void fwsim_nvs_set_str(const char *ns, const char *key, const char *v) { NvsStore()[ns].str[key] = v; }
void fwsim_nvs_erase(const char *ns, const char *key) { NvsStore()[ns].num.erase(key); NvsStore()[ns].str.erase(key); }
extern "C" {
esp_err_t nvs_open(const char *ns, nvs_open_mode_t, nvs_handle_t *h) {
  NvsHandles().push_back(ns);
  *h = (nvs_handle_t)(NvsHandles().size() - 1);
  return ESP_OK;
}
void nvs_close(nvs_handle_t) {}
esp_err_t nvs_commit(nvs_handle_t) { return ESP_OK; }
esp_err_t nvs_erase_key(nvs_handle_t h, const char *k) { Ns(h).num.erase(k); Ns(h).str.erase(k); return ESP_OK; }
esp_err_t nvs_erase_all(nvs_handle_t h) { Ns(h) = NvsNs(); return ESP_OK; }
esp_err_t nvs_get_str(nvs_handle_t h, const char *k, char *out, size_t *len) {
  auto &m = Ns(h).str;
  auto it = m.find(k);
  if (it == m.end()) return ESP_ERR_NVS_NOT_FOUND;
  size_t need = it->second.size() + 1;
  if (out == nullptr) { *len = need; return ESP_OK; }
  if (*len < need) return ESP_ERR_NVS_INVALID_LENGTH;
  memcpy(out, it->second.c_str(), need);
  *len = need;
  return ESP_OK;
}
esp_err_t nvs_set_str(nvs_handle_t h, const char *k, const char *v) { Ns(h).str[k] = v; return ESP_OK; }
esp_err_t nvs_get_blob(nvs_handle_t h, const char *k, void *out, size_t *len) {
  auto &m = Ns(h).str;
  auto it = m.find(k);
  if (it == m.end()) return ESP_ERR_NVS_NOT_FOUND;
  if (out == nullptr) { *len = it->second.size(); return ESP_OK; }
  if (*len < it->second.size()) return ESP_ERR_NVS_INVALID_LENGTH;
  memcpy(out, it->second.data(), it->second.size());
  *len = it->second.size();
  return ESP_OK;
}
esp_err_t nvs_set_blob(nvs_handle_t h, const char *k, const void *v, size_t len) { Ns(h).str[k] = std::string((const char *)v, len); return ESP_OK; }
esp_err_t nvs_get_i8(nvs_handle_t h, const char *k, int8_t *v) { return GetNum(h, k, v); }
esp_err_t nvs_set_i8(nvs_handle_t h, const char *k, int8_t v) { return SetNum(h, k, v); }
esp_err_t nvs_get_u8(nvs_handle_t h, const char *k, uint8_t *v) { return GetNum(h, k, v); }
esp_err_t nvs_set_u8(nvs_handle_t h, const char *k, uint8_t v) { return SetNum(h, k, v); }
esp_err_t nvs_get_i16(nvs_handle_t h, const char *k, int16_t *v) { return GetNum(h, k, v); }
esp_err_t nvs_set_i16(nvs_handle_t h, const char *k, int16_t v) { return SetNum(h, k, v); }
esp_err_t nvs_get_u16(nvs_handle_t h, const char *k, uint16_t *v) { return GetNum(h, k, v); }
esp_err_t nvs_set_u16(nvs_handle_t h, const char *k, uint16_t v) { return SetNum(h, k, v); }
esp_err_t nvs_get_i32(nvs_handle_t h, const char *k, int32_t *v) { return GetNum(h, k, v); }
esp_err_t nvs_set_i32(nvs_handle_t h, const char *k, int32_t v) { return SetNum(h, k, v); }
esp_err_t nvs_get_u32(nvs_handle_t h, const char *k, uint32_t *v) { return GetNum(h, k, v); }
esp_err_t nvs_set_u32(nvs_handle_t h, const char *k, uint32_t v) { return SetNum(h, k, v); }
esp_err_t nvs_get_i64(nvs_handle_t h, const char *k, int64_t *v) { return GetNum(h, k, v); }
esp_err_t nvs_set_i64(nvs_handle_t h, const char *k, int64_t v) { return SetNum(h, k, v); }
esp_err_t nvs_get_u64(nvs_handle_t h, const char *k, uint64_t *v) { return GetNum(h, k, v); }
esp_err_t nvs_set_u64(nvs_handle_t h, const char *k, uint64_t v) { return SetNum(h, k, v); }
}

// ---------------------------------------------------------------- lvgl port
uint16_t g_fwsim_fb[FWSIM_H][FWSIM_W];

static void FlushCb(lv_display_t *disp, const lv_area_t *area, uint8_t *px) {
  const int w = lv_area_get_width(area);
  const auto *src = reinterpret_cast<const uint16_t *>(px);
  for (int y = area->y1; y <= area->y2; ++y) {
    for (int x = area->x1; x <= area->x2; ++x) {
      if (x >= 0 && x < FWSIM_W && y >= 0 && y < FWSIM_H) {
        g_fwsim_fb[y][x] = src[(y - area->y1) * w + (x - area->x1)];
      }
    }
  }
  lv_display_flush_ready(disp);
}

static uint32_t TickCb(void) { return (uint32_t)(g_fwsim.now_us / 1000); }

extern "C" esp_err_t lvgl_port_init(const lvgl_port_cfg_t *) {
  lv_tick_set_cb(TickCb);
  return ESP_OK;
}
extern "C" lv_display_t *lvgl_port_add_disp(const lvgl_port_display_cfg_t *cfg) {
  lv_display_t *d = lv_display_create((int32_t)cfg->hres, (int32_t)cfg->vres);
  lv_display_set_color_format(d, LV_COLOR_FORMAT_RGB565);
  // The device renders in 20-line partial strips; a full-frame partial
  // buffer produces the same pixels without strip bookkeeping.
  const size_t bytes = cfg->hres * cfg->vres * 2;
  static uint8_t *buf = nullptr;
  if (buf == nullptr) buf = (uint8_t *)aligned_alloc(64, bytes);
  lv_display_set_buffers(d, buf, nullptr, bytes, LV_DISPLAY_RENDER_MODE_PARTIAL);
  lv_display_set_flush_cb(d, FlushCb);
  return d;
}
extern "C" bool lvgl_port_lock(uint32_t) { return true; }
extern "C" void lvgl_port_unlock(void) {}
extern "C" esp_err_t lvgl_port_stop(void) { return ESP_OK; }
extern "C" esp_err_t lvgl_port_resume(void) { return ESP_OK; }
extern "C" esp_err_t lvgl_port_remove_disp(lv_display_t *) { return ESP_OK; }

// ---------------------------------------------------------------- app/board
Application &Application::GetInstance() {
  static Application a;
  return a;
}
void Application::Schedule(std::function<void()> &&cb) { queue_.push_back(std::move(cb)); }
void Application::RunScheduled() {
  for (int guard = 0; guard < 64 && !queue_.empty(); ++guard) {
    auto cb = std::move(queue_.front());
    queue_.pop_front();
    cb();
  }
}

Board &Board::GetInstance() {
  static Board b;
  return b;
}
Display *Board::GetDisplay() { return g_fwsim.display; }
// Same rule as WifiBoard::GetNetworkStateIcon (boards/common/wifi_board.cc).
const char *Board::GetNetworkStateIcon() {
  auto &wifi = WifiManager::GetInstance();
  if (!wifi.IsConnected()) return FONT_AWESOME_WIFI_SLASH;
  int rssi = wifi.GetRssi();
  if (rssi >= -65) return FONT_AWESOME_WIFI;
  if (rssi >= -75) return FONT_AWESOME_WIFI_FAIR;
  return FONT_AWESOME_WIFI_WEAK;
}
bool Board::GetBatteryLevel(int &level, bool &charging, bool &discharging) {
  level = g_fwsim.battery_level;
  charging = g_fwsim.charging;
  discharging = !g_fwsim.charging;
  return true;
}
bool Board::GetBatteryDiagnostics(int &raw, int &adc_mv, int &battery_mv) {
  raw = g_fwsim.battery_level;
  adc_mv = 0;
  battery_mv = g_fwsim.battery_mv;
  return true;
}

// ---------------------------------------------------------------- services
CheekoAnalytics &CheekoAnalytics::GetInstance() { static CheekoAnalytics *a = reinterpret_cast<CheekoAnalytics *>(new char[sizeof(CheekoAnalytics)]()); return *a; }
void CheekoAnalytics::TrackAiTalkStart(const char *) {}
void CheekoAnalytics::TrackGameEnd(const char *, int) {}
void CheekoAnalytics::TrackGameStart(const char *) {}
void CheekoAnalytics::TrackRadioEnd(const char *, const char *, int) {}
void CheekoAnalytics::TrackRadioStart(const char *, int) {}

CheekoAudioSession::CheekoAudioSession() {}
CheekoAudioSession &CheekoAudioSession::GetInstance() { static CheekoAudioSession s; return s; }
bool CheekoAudioSession::CanAcquire(CheekoAudioOwner) const { return true; }
bool CheekoAudioSession::CanPlayTransientSound() const { return false; }
const char *CheekoAudioSession::OwnerName() const { return "none"; }

CheekoParentAppSync &CheekoParentAppSync::GetInstance() { static CheekoParentAppSync *p = reinterpret_cast<CheekoParentAppSync *>(new char[sizeof(CheekoParentAppSync)]()); return *p; }
void CheekoParentAppSync::PublishLocalSettingsChanged(const char *) {}

CheekoTelemetry &CheekoTelemetry::GetInstance() { static CheekoTelemetry *t = reinterpret_cast<CheekoTelemetry *>(new char[sizeof(CheekoTelemetry)]()); return *t; }
std::string CheekoTelemetry::CheekoMode() const { return "Home"; }
std::string CheekoTelemetry::ContentState() const { return "NoCard"; }
std::string CheekoTelemetry::DisplayOwner() const { return "Cheeko"; }
bool CheekoTelemetry::IsSdLoggingEnabled() const { return false; }
std::string CheekoTelemetry::LastResetReasonName() const { return "poweron"; }
void CheekoTelemetry::Log(const char *m) { if (fwsim_log_enabled()) fprintf(stderr, "[telemetry] %s\n", m); }
void CheekoTelemetry::Log(const char *m, const std::string &d) { if (fwsim_log_enabled()) fprintf(stderr, "[telemetry] %s %s\n", m, d.c_str()); }

Ota::Ota() {}
Ota::~Ota() {}
esp_err_t Ota::CheckVersion() { return ESP_FAIL; }
std::string Ota::GetCheckVersionUrl() { return "https://example.invalid/ota/"; }

RadioPlayer::~RadioPlayer() {}
bool RadioPlayer::Initialize(AudioCodec *) { return true; }
bool RadioPlayer::Play(const std::string &url) {
  current_url_ = url;
  state_ = State::kPlaying;
  if (on_state_changed_) on_state_changed_(state_);
  return true;
}
void RadioPlayer::Stop() {
  state_ = State::kStopped;
  if (on_state_changed_) on_state_changed_(state_);
}
void RadioPlayer::SetOnStateChanged(std::function<void(State)> cb) { on_state_changed_ = std::move(cb); }
const char *RadioPlayer::StateName(State s) {
  switch (s) {
    case State::kStopped: return "stopped";
    case State::kBuffering: return "buffering";
    case State::kPlaying: return "playing";
    default: return "error";
  }
}
const char *RadioPlayer::StateName() const { return StateName(state_); }

std::string SystemInfo::GetMacAddress() { return "24:6f:28:12:34:56"; }
std::string SystemInfo::GetUserAgent() { return "cheeko-v2/" FWSIM_PROJECT_VER; }
bool SystemInfo::GetCpuSummary(char *out, size_t len) { snprintf(out, len, "cpu 12%%"); return true; }
