#ifndef BOARD_H
#define BOARD_H
// Host simulator stand-in for main/boards/common/board.h. Only what the UI
// code calls; values come from the simulator's scenario state (fwsim_state.h).
#include <cstdint>
#include <functional>
#include <string>
#include <memory>
class AudioCodec;
class Display;
class Http {
public:
  void SetTimeout(int) {}
  void SetHeader(const std::string &, const std::string &) {}
  void SetContent(std::string) {}
  bool Open(const std::string &, const std::string &) { return false; }
  void Close() {}
  int GetStatusCode() { return 0; }
  std::string ReadAll() { return ""; }
};
class NetworkInterface {
public:
  virtual ~NetworkInterface() = default;
  std::unique_ptr<Http> CreateHttp(int = 0) { return nullptr; }
};
class Backlight {
public:
  void RestoreBrightness(bool = false) {}
  void SetBrightness(uint8_t b, bool = false) { brightness_ = b; }
  void SetBrightnessImmediate(uint8_t b) { brightness_ = b; }
  uint8_t brightness() const { return brightness_; }
  uint8_t brightness_ = 70;
};
enum class PowerSaveLevel { LOW_POWER, BALANCED, PERFORMANCE };
class Board {
public:
  static Board &GetInstance();
  Backlight *GetBacklight() { return &backlight_; }
  AudioCodec *GetAudioCodec() { return nullptr; }
  NetworkInterface *GetNetwork() { return &network_; }
  Display *GetDisplay();
  const char *GetNetworkStateIcon();
  bool GetBatteryLevel(int &level, bool &charging, bool &discharging);
  bool GetBatteryDiagnostics(int &raw, int &adc_mv, int &battery_mv);
  std::string GetBoardType() { return "cheeko-v2"; }
  std::string GetUuid() { return "00000000-sim"; }
  bool HasLocalMediaActivity() const { return false; }
  void OnParentSettingsUpdated() {}
  void RunPendingOnboarding() {}
  bool IsFirstBootOnboardingActive() const { return false; }
  void SetImagineResourceMode(bool) {}
  void SetPowerSaveLevel(PowerSaveLevel) {}
  Backlight backlight_;
  NetworkInterface network_;
};
#endif
