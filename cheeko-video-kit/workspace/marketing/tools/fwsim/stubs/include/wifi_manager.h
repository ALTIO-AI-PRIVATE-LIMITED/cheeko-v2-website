#pragma once
#include <string>
// Simulated Wi-Fi: state is set by the harness (fwsim_state).
class WifiManager {
public:
  static WifiManager &GetInstance() { static WifiManager w; return w; }
  bool IsConnected() const { return connected; }
  std::string GetSsid() const { return ssid; }
  int GetRssi() const { return rssi; }
  std::string GetIpAddress() const { return "192.168.1.42"; }
  int GetChannel() const { return 6; }
  bool IsConfigMode() const { return false; }
  void StartStation() {}
  void StopStation() {}
  void StartConfigAp() {}
  void StopConfigAp() {}
  bool connected = true;
  std::string ssid = "HomeWiFi";
  int rssi = -52;
};
