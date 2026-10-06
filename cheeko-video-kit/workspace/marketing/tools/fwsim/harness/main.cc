// Cheeko firmware screen renderer (host simulator).
//
// Builds the firmware's real display stack (CustomLcdDisplay -> SpiLcdDisplay
// -> LcdDisplay, which owns CheekoOs) against an in-memory 296x240 RGB565
// framebuffer, drives it through the same public entry points the board and
// Application use (Show/Rotate/Select/Back, SetStatus/SetEmotion/...), and
// writes a PNG of each resulting frame.
//
//   fwsim <out_dir> [--mascot cheeko|dinku|robu] [--theme 0-6] [--group NAME]...
//   --theme N: NVS cheeko/ui_theme = N (Sunny, Night, Ocean, Candy, Orange, White, Pink), files prefixed "theme<N>_"
//
// Every PNG gets a line in <out_dir>/shots.tsv: file, group, how, notes.

#include <sys/stat.h>
#include <sys/time.h>
#include <zlib.h>

#include <cmath>
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <functional>
#include <set>
#include <string>
#include <vector>

#include "application.h"
#include "cheeko_voice_changer.h"
#include "cheeko_theme.h"
#include "cheeko_settings_items.h"
#include "assets/lang_config.h"
#include "cheeko_mascot.h"
#include "cheeko_os.h"
#include "display/lcd_display.h"
#include "fwsim_state.h"
#include "wifi_manager.h"
#include "ssid_manager.h"
#include "lvgl_theme.h"
#include "lvgl_font.h"
LV_FONT_DECLARE(font_puhui_basic_20_4);
#include "cheeko_character_catalog.h"
#include "cheeko_game_catalog.h"
#include "boards/cheeko-v2/cheeko_sd_image_loader.h"

LcdDisplay *fwsim_create_display();
CheekoOs *fwsim_cheeko_os(LcdDisplay *d);

// ------------------------------------------------------------ wall clock
// Calls to time()/gettimeofday() from the firmware objects bind to these (the
// executable's own definitions win over libSystem at static link time).
static int64_t WallNow() { return g_fwsim.wall_epoch + g_fwsim.now_us / 1000000; }
extern "C" time_t time(time_t *t) {
  time_t v = (time_t)WallNow();
  if (t) *t = v;
  return v;
}
extern "C" int gettimeofday(struct timeval *tv, void *) {
  tv->tv_sec = (time_t)WallNow();
  tv->tv_usec = (suseconds_t)(g_fwsim.now_us % 1000000);
  return 0;
}

// ------------------------------------------------------------ PNG writer
static void PutU32(std::vector<uint8_t> &v, uint32_t x) {
  v.push_back(x >> 24); v.push_back(x >> 16); v.push_back(x >> 8); v.push_back(x);
}
static void Chunk(FILE *f, const char *type, const std::vector<uint8_t> &data) {
  std::vector<uint8_t> buf;
  PutU32(buf, (uint32_t)data.size());
  buf.insert(buf.end(), type, type + 4);
  buf.insert(buf.end(), data.begin(), data.end());
  uint32_t crc = crc32(0, buf.data() + 4, (uInt)(buf.size() - 4));
  PutU32(buf, crc);
  fwrite(buf.data(), 1, buf.size(), f);
}
static bool WritePng(const std::string &path) {
  std::vector<uint8_t> raw;
  raw.reserve((FWSIM_W * 3 + 1) * FWSIM_H);
  for (int y = 0; y < FWSIM_H; ++y) {
    raw.push_back(0);
    for (int x = 0; x < FWSIM_W; ++x) {
      const uint16_t p = g_fwsim_fb[y][x];
      const uint8_t r = (p >> 11) & 0x1F, g = (p >> 5) & 0x3F, b = p & 0x1F;
      raw.push_back((r << 3) | (r >> 2));
      raw.push_back((g << 2) | (g >> 4));
      raw.push_back((b << 3) | (b >> 2));
    }
  }
  uLongf zlen = compressBound(raw.size());
  std::vector<uint8_t> z(zlen);
  compress2(z.data(), &zlen, raw.data(), raw.size(), 9);
  z.resize(zlen);
  FILE *f = fopen(path.c_str(), "wb");
  if (!f) return false;
  static const uint8_t sig[8] = {137, 80, 78, 71, 13, 10, 26, 10};
  fwrite(sig, 1, 8, f);
  std::vector<uint8_t> ihdr;
  PutU32(ihdr, FWSIM_W); PutU32(ihdr, FWSIM_H);
  ihdr.push_back(8); ihdr.push_back(2); ihdr.push_back(0); ihdr.push_back(0); ihdr.push_back(0);
  Chunk(f, "IHDR", ihdr);
  Chunk(f, "IDAT", z);
  Chunk(f, "IEND", {});
  fclose(f);
  return true;
}

// ------------------------------------------------------------ simulator core
static std::string g_out;
static std::string g_group;
static FILE *g_tsv = nullptr;
static LcdDisplay *g_disp = nullptr;
static CheekoOs *g_os = nullptr;
static std::string g_prefix;  // e.g. "dinku_" for themed runs

// Advance simulated time, running LVGL timers/animations, esp_timers and the
// Application::Schedule queue exactly as the device's tasks would.
static void Pump(int ms) {
  const int step = 5;
  for (int t = 0; t < ms; t += step) {
    g_fwsim.now_us += step * 1000;
    lv_timer_handler();
    fwsim_run_esp_timers();
    Application::GetInstance().RunScheduled();
    // Application's 1 s clock timer (application.cc) refreshes the status bar.
    if ((g_fwsim.now_us / 1000) % 1000 < step) g_disp->UpdateStatusBar(true);
  }
}

static void Shot(const std::string &name, const std::string &how,
                 const std::string &notes = "") {
  lv_obj_invalidate(lv_screen_active());
  lv_obj_invalidate(lv_layer_top());
  lv_refr_now(nullptr);
  const std::string file = g_prefix + name + ".png";
  WritePng(g_out + "/" + file);
  fprintf(g_tsv, "%s\t%s\t%s\t%s\n", file.c_str(), g_group.c_str(), how.c_str(),
          notes.c_str());
  fflush(g_tsv);
  fprintf(stderr, "  %s\n", file.c_str());
}

// Input helpers: the board calls these on encoder detents / press / double
// click; each is followed by the settle time a person would wait.
static void Turn(int n, int settle = 400) {
  for (int i = 0; i < (n < 0 ? -n : n); ++i) {
    g_os->Rotate(n > 0);
    Pump(120);
  }
  Pump(settle);
}
static void Press(int settle = 600) { g_os->Select(); Pump(settle); }
static void BackBtn(int settle = 500) { g_os->Back(); Pump(settle); }
static void Home() {
  // Back out until CheekoOs hides itself (Back on the main menu resets every
  // menu cursor), then open the launcher again - lands on TALK.
  // A session (Talk/Imagine) leaves CheekoOs inactive with its cursor where
  // it was, so re-show first and back out from there.
  if (!g_os->IsActive()) { g_os->Show(); Pump(200); }
  for (int i = 0; i < 10 && g_os->IsActive(); ++i) { g_os->Back(); Pump(80); }
  g_os->Show();
  Pump(800);
}

// Application-equivalent display calls (the strings/emotions application.cc
// pushes for each device state in the menu-started, manual-mic Talk flow).
static void AppState(DeviceState st) { Application::GetInstance().state_ = st; }

// ------------------------------------------------------------ scenarios
static std::set<std::string> g_only;
static bool Want(const char *group) {
  g_group = group;
  return g_only.empty() || g_only.count(group);
}

static const char *kMenuNames[6] = {"talk", "imagine", "games", "funny_voice", "radio", "settings"};

static void ScenarioHomeIdle() {
  if (!Want("home")) return;
  Shot("00_boot", "LcdDisplay::SetupUI() boot page, before Application reaches Idle");
  // Board boot leaves the idle/clock home page up (Application: STANDBY).
  AppState(kDeviceStateIdle);
  g_disp->SetStatus(Lang::Strings::STANDBY);
  g_disp->SetEmotion("eyes_normal");
  Pump(1500);
  Shot("00_home_clock", "LcdDisplay idle page after SetStatus(STANDBY)",
       "clock/greeting from simulated wall time; battery/Wi-Fi from stub state");
}

static void ScenarioMenu() {
  if (!Want("menu")) return;
  g_os->Show();
  Pump(1500);
  for (int i = 0; i < 6; ++i) {
    if (i > 0) Turn(1, 900);
    char name[64];
    snprintf(name, sizeof(name), "01_menu_%d_%s", i + 1, kMenuNames[i]);
    Shot(name, "CheekoOs::Show() then Rotate(next) x" + std::to_string(i));
  }
  Home();
}


static const char *kCharIds[7] = {"cheeko", "quizzy", "tara", "nani", "mitthu", "chanda", "masti"};

static void TalkReturnHome() {
  AppState(kDeviceStateIdle);
  g_disp->SetStatus(Lang::Strings::STANDBY);
  g_disp->ClearChatMessages();
  g_disp->SetEmotion("eyes_normal");
  Pump(600);
  g_os->Show();
  Pump(800);
}

// Talk: the character carousel, then the session states the Application
// pushes for a menu-started (manual mic) conversation.
static void ScenarioTalk() {
  if (!Want("talk")) return;
  Home();
  Press(900);  // TALK -> picker (opens on Cheeko)
  const int n = CheekoCharacterListedCount();
  for (int i = 0; i < n; ++i) {
    if (i > 0) Turn(1, 900);
    const CheekoCharacterDefinition *c = CheekoCharacterAt(g_os->character_index_);
    std::string id = c && c->id ? c->id : std::to_string(i);
    char name[64];
    snprintf(name, sizeof(name), "02_talk_picker_%d_%s", i + 1, id.c_str());
    Shot(name, "TALK -> Select(); Rotate(next) x" + std::to_string(i));
  }
  // Session states for every character. The picker only lists the first
  // CheekoCharacterListedCount() characters; the rest are reached with an RFID
  // "Hello" card, which calls SelectCharacterById() before the session.
  const int nchars = g_prefix.empty() ? 7 : 1;  // themed runs: Cheeko only
  for (int ci = 0; ci < nchars; ++ci) {
    Home();
    const std::string id = std::to_string(ci + 1) + "_" + kCharIds[ci];
    const bool listed = ci < n;
    if (listed) {
      Press(700);
      Turn(ci, 700);
      Press(50);  // StartTalkWithoutCard(): SetStatus(CONNECTING) + hides overlay
    } else {
      for (int i = 0; i < 10 && g_os->IsActive(); ++i) { g_os->Back(); Pump(80); }
      g_os->SelectCharacterById(kCharIds[ci]);
      g_disp->BeginTalkSession();
      Pump(50);
    }
    const bool full = (ci == 0);
    if (full) {
      Pump(250);
      Shot("03_talk_" + id + "_1_loading", "picker Select() -> StartTalkWithoutCard (SetStatus CONNECTING)", "captured 250 ms in");
    }
    AppState(kDeviceStateConnecting);
    g_disp->SetStatus(Lang::Strings::CONNECTING);
    g_disp->SetEmotion("eyes_normal");
    g_disp->SetChatMessage("system", "");
    Pump(1500);
    if (full) Shot("03_talk_" + id + "_2_connecting", "Application kDeviceStateConnecting: SetStatus(CONNECTING), SetEmotion(eyes_normal)");
    AppState(kDeviceStateIdle);
    g_disp->SetStatus("Mic off");
    g_disp->SetEmotion("eyes_normal");
    Pump(1500);
    if (full) Shot("03_talk_" + id + "_3_ready_mic_off", "manual-mic idle between turns: SetStatus(\"Mic off\")");
    AppState(kDeviceStateListening);
    g_disp->SetStatus("User talking");
    g_disp->SetEmotion("eyes_listen");
    Pump(1500);
    Shot("03_talk_" + id + "_4_listening", "kDeviceStateListening (manual): SetStatus(\"User talking\"), SetEmotion(eyes_listen)");
    g_disp->SetStatus("Thinking...");
    g_disp->SetEmotion("eyes_normal");
    Pump(1500);
    Shot("03_talk_" + id + "_5_thinking", "stop-listening path: SetStatus(\"Thinking...\")");
    AppState(kDeviceStateSpeaking);
    g_disp->SetChatMessage("assistant", "The sky looks blue because sunlight bounces off tiny bits of air!");
    g_disp->SetStatus("Cheeko talking");
    g_disp->SetEmotion("happy");
    Pump(1500);
    Shot("03_talk_" + id + "_6_talking", "kDeviceStateSpeaking + on_playback_start: SetStatus(\"Cheeko talking\"), SetEmotion(happy), SetChatMessage(assistant, ...)",
         "reply text is sample copy (server-provided on device)");
    TalkReturnHome();
    (void)listed;
  }
  Home();
}

// Cheeko face expressions (the drawn face used by SetEmotion) on the talk page.
static void ScenarioFace() {
  if (!Want("face")) return;
  const char *emotions[] = {"neutral", "happy", "laughing", "funny", "sad", "angry", "crying",
                            "loving", "embarrassed", "surprised", "shocked", "thinking",
                            "winking", "cool", "relaxed", "delicious", "kissy", "confident",
                            "sleepy", "silly", "confused"};
  (void)emotions;
}

static void GameShot(const std::string &id, int idx) {
  char name[80];
  snprintf(name, sizeof(name), "05_game_%d_%s", idx + 1, id.c_str());
  Shot(name, "GAMES -> Rotate x" + std::to_string(idx) + " -> Select() (StartSelectedGame)");
}

static std::string Lower(std::string s) {
  for (auto &c : s) c = (c == ' ') ? '_' : (char)tolower(c);
  return s;
}

static void ScenarioGames() {
  if (!Want("games")) return;
  Home();
  Turn(2, 500);
  Press(1200);
  const int total = CheekoGameCount();  // == CheekoTotalGameCount (packs are not listed)
  for (int i = 0; i < total; ++i) {
    if (i > 0) Turn(1, 900);
    const CheekoGameDefinition *g = CheekoGameAt(i);
    std::string id = g && g->name ? Lower(g->name) : ("sdapp" + std::to_string(i));
    char name[80];
    snprintf(name, sizeof(name), "04_games_menu_%d_%s", i + 1, id.c_str());
    Shot(name, "MAIN GAMES -> Select(); Rotate(next) x" + std::to_string(i));
  }
  // Start each built-in game.
  const int builtin = CheekoGameCount();
  for (int i = 0; i < builtin; ++i) {
    Home();
    Turn(2, 300);
    Press(800);
    Turn(i, 500);
    const CheekoGameDefinition *g = CheekoGameAt(i);
    const std::string id = Lower(g->name);
    Press(1500);
    GameShot(id, i);
    if (id == "animal" || id == "numbers") {
      // Answer: wrong once, then correct every round until the session ends.
      auto &games = g_os->games_;
      int guard = 0;
      bool took_wrong = false, took_right = false;
      while (g_os->screen_ != CheekoOs::Screen::kGameResult && guard++ < 40) {
        int target = games.correct_option();
        if (!took_wrong) target = (target + 1) % 3;
        while (games.selected_option() != target) { g_os->Rotate(true); Pump(100); }
        g_os->Select();
        Pump(400);
        if (!took_wrong) { Shot("05_game_" + id + "_try_again", "answered a wrong option (Rotate to it, Select())"); took_wrong = true; }
        else if (!took_right) { Shot("05_game_" + id + "_correct", "answered the correct option"); took_right = true; }
        Pump(3500);
        static bool q2 = false;
        if (guard == 1) q2 = false;
        // (NUMBERS: skip questions whose three tiles collide - see index.md)
        const bool tiles_ok = id != "numbers" || games.number_target() - games.correct_option() + 2 <= 9;
        if (!q2 && guard >= 2 && tiles_ok && g_os->screen_ != CheekoOs::Screen::kGameResult) {
          Shot("05_game_" + id + "_question" + std::to_string(guard), "a later question, after the feedback screen");
          q2 = true;
        }
      }
      Pump(1500);
      Shot("06_game_result_" + id + "_one_wrong", "played a full session (1 wrong, rest correct) -> FinishQuizSession -> kGameResult");
      g_os->Select();  // "Press to play again"
      Pump(1500);
      guard = 0;
      while (g_os->screen_ != CheekoOs::Screen::kGameResult && guard++ < 40) {
        while (games.selected_option() != games.correct_option()) { g_os->Rotate(true); Pump(100); }
        g_os->Select();
        Pump(3900);
      }
      Pump(1500);
      Shot("06_game_result_" + id + "_perfect", "Select() play again, every answer correct -> kGameResult");
    }
    if (id == "piano") {
      g_os->Rotate(true); Pump(100); g_os->Rotate(true); Pump(100);
      g_os->Select(); Pump(80);
      Shot("05_game_piano_key_pressed", "Rotate x2, Select() - key lit while pressed");
    }
    if (id == "memory") {
      g_os->Select(); Pump(400);
      g_os->Rotate(true); Pump(100);
      g_os->Select(); Pump(300);
      Shot("05_game_memory_two_flipped", "Select() flip, Rotate, Select() flip");
    }
    if (id == "paint" || id == "trace") {
      // A finger stroke through the firmware's own touch path.
      for (int t = 0; t <= 40; ++t) {
        const double a = t / 40.0 * 6.283;
        g_os->DrawTouchPoint(true, 150 + (int)(60 * cos(a)), 120 + (int)(45 * sin(2 * a)));
        Pump(10);
      }
      g_os->DrawTouchPoint(false, 0, 0);
      Pump(300);
      Shot("05_game_" + id + "_stroke", "DrawTouchPoint() finger stroke (figure-8)", "stroke is synthetic touch input");
    }
    BackBtn(600);
  }
  Home();
}

static void ScenarioVoice() {
  if (!Want("voice")) return;
  Home();
  Turn(3, 500);
  Press(1200);
  const int n = CheekoVoiceChanger::VoiceCount();
  for (int i = 0; i < n; ++i) {
    if (i > 0) Turn(1, 900);
    Shot("07_funny_voice_" + std::to_string(i + 1) + "_" + Lower(CheekoVoiceChanger::VoiceName((CheekoVoiceChanger::Voice)g_os->voice_index_)),
         "FUNNY VOICE -> Select(); Rotate(next) x" + std::to_string(i));
  }
  g_os->VoiceHoldStart();
  Pump(700);
  Shot("07_funny_voice_recording", "VoiceHoldStart() (knob held)");
  Pump(800);
  g_os->VoiceHoldEnd();
  Pump(400);
  Shot("07_funny_voice_playing", "VoiceHoldEnd() after 1.5 s hold");
  BackBtn();
  Home();
}

static void ScenarioRadio() {
  if (!Want("radio")) return;
  Home();
  Turn(4, 500);
  Press(1200);
  const int stations = g_os->radio_controller_.StationCount();
  std::string first;
  for (int i = 0; i < stations; ++i) {
    if (i > 0) Turn(1, 700);
    char st[32]; snprintf(st, sizeof(st), "08_radio_station_%02d", i + 1);
    Shot(st, "RADIO -> Select(); Rotate(next) x" + std::to_string(i));
  }
  Press(1500);
  Shot("08_radio_playing", "Select() -> ToggleRadio (RadioPlayer stubbed to kPlaying)");
  BackBtn();
  // No Wi-Fi variant
  WifiManager::GetInstance().connected = false;
  Home(); Turn(4, 400); Press(1200);
  Shot("08_radio_no_wifi", "Wi-Fi disconnected, RADIO -> Select()");
  WifiManager::GetInstance().connected = true;
  BackBtn();
  Home();
}

static void ScenarioImagine() {
  if (!Want("imagine")) return;
  Home();
  Turn(1, 500);
  Press(50);  // StartAiImagine(): SetImagineStage("listening")
  Pump(1500);
  Shot("09_imagine_1_listening", "IMAGINE -> Select() -> StartAiImagine -> SetImagineStage(listening)");
  g_disp->SetChatMessage("user", "a dinosaur flying a kite");
  Pump(800);
  Shot("09_imagine_2_listening_transcript", "SetChatMessage(user, ...) live transcript", "prompt text is sample copy");
  g_disp->SetImagineGenerating(true);
  Pump(1500);
  Shot("09_imagine_3_painting", "SetImagineGenerating(true) -> \"Painting your idea...\"");
  g_disp->SetImagineStage("downloading");
  Pump(1200);
  Shot("09_imagine_4_downloading", "SetImagineStage(downloading) -> \"Here it comes!\"");
  auto img = CheekoSdImageLoader::Load("./sdcard/cheeko/wall/day.bin");
  g_disp->ShowImagineImage(std::move(img), "a dinosaur flying a kite");
  Pump(1500);
  Shot("09_imagine_5_result", "ShowImagineImage(image, caption)", "STAND-IN picture (home wallpaper) - on device this is the AI-generated image");
  g_disp->HideImagineImage();
  AppState(kDeviceStateIdle);
  Pump(500);
  // Offline card
  Application::GetInstance().online_ = false;
  WifiManager::GetInstance().connected = false;
  Home();
  Turn(1, 500);
  Press(1200);
  Shot("09_imagine_6_joining_wifi", "Wi-Fi off, saved networks exist: IMAGINE -> Select() -> kImagineOffline");
  BackBtn();
  {
    auto saved = SsidManager::GetInstance().list;
    SsidManager::GetInstance().list.clear();
    Home(); Turn(1, 500); Press(1200);
    Shot("09_imagine_6b_wifi_needed", "Wi-Fi off, no saved networks: IMAGINE -> Select() -> kImagineOffline");
    SsidManager::GetInstance().list = saved;
  }
  Application::GetInstance().online_ = true;
  WifiManager::GetInstance().connected = true;
  BackBtn();
  Application::GetInstance().internet_down_ = true;
  Home(); Turn(1, 500); Press(1200);
  Shot("09_imagine_7_server_resting", "server unreachable (IsInternetUnavailable): IMAGINE -> Select() -> kImagineOffline");
  Application::GetInstance().internet_down_ = false;
  BackBtn();
  Home();
}

static void ScenarioSettings() {
  if (!Want("settings")) return;
  Home();
  Turn(5, 500);
  Press(1000);
  for (int c = 0; c < 3; ++c) {
    if (c > 0) Turn(1, 700);
    Shot("10_settings_categories_" + std::to_string(c + 1), "SETTINGS -> Select(); Rotate x" + std::to_string(c));
  }
  // Into each category, walking every row.
  for (int c = 0; c < 3; ++c) {
    Home(); Turn(5, 300); Press(700);
    Turn(c, 400);
    Press(800);
    const bool dev = g_os->settings_.developer_mode();
    const int rows = CheekoSettingsCountIn(CheekoSettingsCategoryAt(c, dev), dev);
    for (int r = 0; r < rows && r < 1; ++r) {
      Shot("11_settings_cat" + std::to_string(c + 1) + "_row" + std::to_string(r + 1),
           "category " + std::to_string(c + 1) + ", Rotate x" + std::to_string(r));
    }
  }
  // My Cheeko sub-screens: Character, Themes, Brightness, Feel the buzzes.
  const char *subs[] = {"character", "themes", "brightness", "haptics_toggle", "feel_buzzes"};
  for (int r = 0; r < 5; ++r) {
    if (r == 3) continue;
    Home(); Turn(5, 300); Press(700); Press(700);
    Turn(r, 400);
    Press(1000);
    Shot(std::string("12_settings_") + subs[r], std::string("My Cheeko row ") + std::to_string(r + 1) + " -> Select()");
    if (r == 0) {
      for (int k = 1; k < 3; ++k) { Turn(1, 1000); Shot("12_settings_character_" + std::to_string(k + 1), "Character picker Rotate x" + std::to_string(k)); }
    }
    if (r == 1) {
      const int n = CheekoTheme::ThemeCount();
      for (int k = 1; k < n; ++k) { Turn(1, 800); Shot("12_settings_themes_" + std::to_string(k + 1), "Themes Rotate x" + std::to_string(k) + " (live preview)"); }
      Turn(1, 300);  // back to the persisted theme before leaving
    }
    BackBtn(500);
  }
  // Device: Wi-Fi setup (Bluetooth) screen and About
  Home(); Turn(5, 300); Press(700); Turn(1, 300); Press(700);
  Press(1500);
  Shot("13_settings_wifi_setup", "Device -> Set up Wi-Fi row -> Select() (Bluetooth provisioning screen)");
  BackBtn(800);
  Home();
}

static void ScenarioCards() {
  if (!Want("cards")) return;
  auto *d = g_disp;
  // Idle page underneath, as when a card is tapped at home.
  struct R { int kind; const char *name; const char *file; };
  extern void fwsim_card_reveal(LcdDisplay *, int, const char *);
  extern void fwsim_card_feedback(LcdDisplay *, const char *, bool);
  extern void fwsim_download(LcdDisplay *, const char *, int, int, int);
  const R reveals[] = {{1, "Cheeko", "14_card_reveal_hello_cheeko"}, {1, "Nani", "14_card_reveal_hello_nani"},
                       {2, "Hometown", "14_card_reveal_quest"}, {0, "", "14_card_reveal_discover"}};
  for (auto &r : reveals) {
    fwsim_card_reveal(d, r.kind, r.name);
    Pump(700);
    Shot(r.file, std::string("CustomLcdDisplay::ShowCardReveal(kind=") + std::to_string(r.kind) + ", \"" + r.name + "\")", "captured 700 ms into the reveal animation");
    Pump(1500);
  }
  fwsim_card_feedback(d, "Card not recognized", true);
  Pump(400);
  Shot("14_card_not_recognized", "ShowCardFeedback(\"Card not recognized\")");
  Pump(4000);
  fwsim_card_feedback(d, "Connect to Wi-Fi", false);
  Pump(400);
  Shot("14_card_connect_wifi", "ShowCardFeedback(\"Connect to Wi-Fi\", false)");
  Pump(4000);
  fwsim_download(d, "Animal Sounds", 2, 4, 60);
  Pump(800);
  Shot("14_card_downloading", "SetDownloadProgress(\"Animal Sounds\", 2, 4, 60%)");
  fwsim_download(d, nullptr, 0, 0, -1);
  Pump(800);
}

static void ScenarioCardTalkIdle() {
  if (!Want("cards")) return;
  g_disp->SetAiCardConnecting(true);
  Pump(1200);
  Shot("14_card_talk_connecting", "idle page, SetAiCardConnecting(true) (AI character card warming up)");
  g_disp->SetAiCardConnecting(false);
  g_disp->SetAiCardKnobPrompt(true);
  Pump(1200);
  Shot("14_card_talk_knob_prompt", "idle page, SetAiCardKnobPrompt(true) (card session idle, waiting for a press)");
  g_disp->SetAiCardKnobPrompt(false);
  Pump(800);
}

static void ScenarioBattery() {
  if (!Want("battery")) return;
  g_fwsim.charging = true; g_fwsim.battery_level = 46;
  Pump(2500);
  Shot("15_home_charging", "idle page, GetBatteryLevel -> 46% charging");
  g_fwsim.charging = false; g_fwsim.battery_level = 5; g_fwsim.battery_mv = 3500;
  Pump(8000);
  Shot("15_low_battery", "idle page, GetBatteryLevel -> 5% discharging (UpdateStatusBar low-battery latch)");
  g_fwsim.battery_level = 80; g_fwsim.battery_mv = 3950;
  Pump(8000);
}

static void ScenarioOnboarding() {
  if (!Want("onboarding")) return;
  g_os->ShowOnboarding();
  Pump(1500);
  const char *names[] = {"intro", "turn", "press", "back", "tap", "swipe", "card", "card_ok", "done"};
  for (int st = 0; st <= 8; ++st) {
    if (st > 0) { g_os->EnterOnboardingStep((uint8_t)st); Pump(1500); }
    Shot("16_onboarding_" + std::to_string(st + 1) + "_" + names[st], "ShowOnboarding(); EnterOnboardingStep(" + std::to_string(st) + ")");
  }
  g_os->StopOnboardingTimer();
  g_os->Back();
  Pump(800);
}

static void ScenarioWifiPrompt() {
  if (!Want("wifiprompt")) return;
  g_os->ShowStartupWifiPrompt();
  Pump(1200);
  Shot("17_startup_wifi_prompt", "CheekoOs::ShowStartupWifiPrompt()");
  Turn(1, 600);
  Shot("17_startup_wifi_prompt_2", "startup prompt, Rotate(next)");
  Home();
}

int main(int argc, char **argv) {
  if (argc < 2) {
    fprintf(stderr, "usage: fwsim <out_dir> [--mascot id] [--group g]...\n");
    return 2;
  }
  g_out = argv[1];
  std::string mascot = "cheeko";
  int theme = -1;
  for (int i = 2; i < argc; ++i) {
    if (!strcmp(argv[i], "--mascot") && i + 1 < argc) mascot = argv[++i];
    else if (!strcmp(argv[i], "--group") && i + 1 < argc) g_only.insert(argv[++i]);
    else if (!strcmp(argv[i], "--theme") && i + 1 < argc) theme = atoi(argv[++i]);
  }
  mkdir(g_out.c_str(), 0755);
  setenv("TZ", "UTC", 1);
  tzset();
  // 2026-09-28 10:30:00 (displayed as local time; TZ=UTC).
  g_fwsim.wall_epoch = 1790591400;
  const std::string tsv = g_out + "/shots.tsv";
  g_tsv = fopen(tsv.c_str(), "a");

  if (mascot != "cheeko") {
    fwsim_nvs_set_str("cheeko", "mascot", mascot.c_str());
    g_prefix = mascot + "_";
  }
  if (theme >= 0) {   // the parent app's theme sync writes this key (cheeko_theme.h)
    fwsim_nvs_set_int("cheeko", "ui_theme", theme);
    g_prefix += "theme" + std::to_string(theme) + "_";
  }

  g_disp = fwsim_create_display();
  g_fwsim.display = g_disp;
  g_disp->SetupUI();
  // Assets::Apply (assets.cc): the assets partition's text font
  // (ASSETS_TEXT_FONT = font_puhui_basic_20_4 for cheeko-v2) replaces the
  // 14 px builtin on both themes, then the current theme is re-applied.
  {
    auto f = std::make_shared<LvglBuiltInFont>(&font_puhui_basic_20_4);
    auto &tm = LvglThemeManager::GetInstance();
    tm.GetTheme("light")->set_text_font(f);
    tm.GetTheme("dark")->set_text_font(f);
    if (g_disp->GetTheme() != nullptr) g_disp->SetTheme(g_disp->GetTheme());
  }
  g_os = fwsim_cheeko_os(g_disp);
  Pump(500);

  ScenarioHomeIdle();
  ScenarioMenu();
  ScenarioTalk();
  ScenarioGames();
  ScenarioVoice();
  ScenarioRadio();
  ScenarioImagine();
  ScenarioSettings();
  ScenarioOnboarding();
  ScenarioWifiPrompt();
  // home page again for overlays that sit on it
  if (g_os->IsActive()) { for (int i = 0; i < 6; ++i) { g_os->Back(); Pump(80); } }
  Pump(800);
  ScenarioCards();
  ScenarioCardTalkIdle();
  ScenarioBattery();

  fclose(g_tsv);
  return 0;
}
