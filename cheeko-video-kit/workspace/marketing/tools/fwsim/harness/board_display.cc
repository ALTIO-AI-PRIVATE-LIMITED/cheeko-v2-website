// Compiles the firmware's own CustomLcdDisplay (extracted verbatim from
// boards/cheeko-v2/cheeko_v2_board.cc by tools/extract.py) plus the Funny Voice
// name table, with the audio engine itself stubbed out.
#include <atomic>
#include <cstdio>
#include <cstring>
#include <ctime>
#include <functional>
#include <memory>
#include <string>

#include "application.h"
#include "assets/lang_config.h"
#include "board.h"
#include "cheeko_character_catalog.h"
#include "cheeko_os.h"
#include "cheeko_os_config.h"
#include "cheeko_templates.h"
#include "cheeko_theme.h"
#include "cheeko_voice_changer.h"
#include "config.h"
#include "display/lcd_display.h"
#include "settings.h"
#include <esp_log.h>
#include <esp_lvgl_port.h>
#include <esp_timer.h>

#define BOARD_TAG "CheekoV2Board"

// ---- Funny Voice engine: names are the firmware's, the DSP is not built.
#include "voice_table.inc"
CheekoVoiceChanger::CheekoVoiceChanger() = default;
CheekoVoiceChanger::~CheekoVoiceChanger() = default;
bool CheekoVoiceChanger::Initialize() { return true; }
bool CheekoVoiceChanger::StartRecording() { return true; }
void CheekoVoiceChanger::StopAndPlay(Voice) {}
void CheekoVoiceChanger::Cancel() {}

#include "custom_lcd_display.inc"

LcdDisplay *fwsim_create_display() {
  return new CustomLcdDisplay(nullptr, nullptr, DISPLAY_WIDTH, DISPLAY_HEIGHT,
                              DISPLAY_OFFSET_X, DISPLAY_OFFSET_Y,
                              DISPLAY_MIRROR_X, DISPLAY_MIRROR_Y,
                              DISPLAY_SWAP_XY);
}
CheekoOs *fwsim_cheeko_os(LcdDisplay *d) {
  return static_cast<CustomLcdDisplay *>(d)->fwsim_os();
}

void fwsim_card_reveal(LcdDisplay *d, int kind, const char *name) {
  static_cast<CustomLcdDisplay *>(d)->ShowCardReveal(
      static_cast<CustomLcdDisplay::CardKind>(kind), name);
}
void fwsim_card_feedback(LcdDisplay *d, const char *msg, bool err) {
  static_cast<CustomLcdDisplay *>(d)->ShowCardFeedback(msg, err);
}
void fwsim_download(LcdDisplay *d, const char *name, int cur, int total, int pct) {
  auto *c = static_cast<CustomLcdDisplay *>(d);
  if (name == nullptr) { c->HideDownloadProgress(); return; }
  c->SetDownloadProgress(name, cur, total, pct);
}
