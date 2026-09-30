#pragma once
#include "esp_err.h"
enum class BlufiProvisioningStatus { kAdvertising, kPhoneConnected, kPhoneDisconnected, kCredentialsReceived, kConnectingWifi, kWifiConnected, kWifiFailed, kBluetoothFailed };
class Blufi {
public:
  static constexpr const char *kDeviceName = "Cheeko AI";
  static Blufi &GetInstance() { static Blufi b; return b; }
  void RequestStart() {}
  esp_err_t deinit() { return ESP_OK; }
  using ProvisioningStatusCallback = void (*)(BlufiProvisioningStatus, const char *, void *);
  void SetProvisioningStatusCallback(ProvisioningStatusCallback, void *) {}
};
