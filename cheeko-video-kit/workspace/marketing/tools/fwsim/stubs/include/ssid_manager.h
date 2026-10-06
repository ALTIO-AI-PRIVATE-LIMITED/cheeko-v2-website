#pragma once
#include <string>
#include <vector>
struct SsidItem { std::string ssid; std::string password; };
class SsidManager {
public:
  static SsidManager &GetInstance() { static SsidManager m; return m; }
  void Reload() {}
  void Clear() { list.clear(); }
  void AddSsid(const std::string &s, const std::string &p) { list.push_back({s, p}); }
  void RemoveSsid(int i) { if (i >= 0 && i < (int)list.size()) list.erase(list.begin() + i); }
  void SetDefaultSsid(int) {}
  const std::vector<SsidItem> &GetSsidList() const { return list; }
  std::vector<SsidItem> list{{"HomeWiFi", ""}, {"Grandma's House", ""}};
};
