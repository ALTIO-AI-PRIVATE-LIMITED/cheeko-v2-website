#ifndef _APPLICATION_H_
#define _APPLICATION_H_
// Host simulator stand-in for main/application.h.
#include <sdkconfig.h>
#include <freertos/FreeRTOS.h>
#include <esp_timer.h>
#include <atomic>
#include <deque>
#include <functional>
#include <memory>
#include <mutex>
#include <string>
#include <string_view>
#include <utility>
#include <vector>
#include "device_state.h"
class AudioService {
public:
  void PlayToneSequence(const std::vector<std::pair<int, int>> &, int = 5000) {}
  void PlaySound(const std::string_view &) {}
  void Stop() {}
  bool IsIdle() { return true; }
  void EnableVoiceProcessing(bool) {}
  void EnableWakeWordDetection(bool) {}
  void ResetDecoder() {}
  void SetMuted(bool) {}
  bool IsAudioProcessorRunning() { return false; }
};
class Application {
public:
  static constexpr bool kAutoListeningSupported = false;
  static Application &GetInstance();
  DeviceState GetDeviceState() const { return state_; }
  void Schedule(std::function<void()> &&cb);
  void RunScheduled();
  void PlaySound(const std::string_view &) {}
  AudioService &GetAudioService() { return audio_; }
  void SetAutoListeningEnabled(bool e) { auto_listen_ = e; }
  bool IsAutoListeningEnabled() const { return auto_listen_; }
  void SetManualTalkInterruptEnabled(bool) {}
  bool UpgradeFirmware(const std::string &, const std::string & = "") { return false; }
  bool CanUseOnlineFeatures() const { return online_; }
  bool IsAccessPointConnected() const { return online_; }
  bool IsInternetUnavailable() const { return internet_down_; }
  void StartAiImagine() {}
  void StartDefaultListeningWithoutRfid() {}
  void StartMutedTalkWithoutRfid() {}
  DeviceState state_ = kDeviceStateIdle;
  bool online_ = true;
  bool internet_down_ = false;  // Wi-Fi up but the server unreachable
  bool auto_listen_ = true;
  AudioService audio_;
  std::deque<std::function<void()>> queue_;
};
#endif
