#!/bin/sh
# Regenerate the verbatim board/voice extracts for the simulator.
# usage: tools/extract_board.sh <fw_root> <gen_dir>
set -e
FW="$1"; GEN="$2"; T="$(dirname "$0")"
B="$FW/main/boards/cheeko-v2"
python3 "$T/extract.py" "$B/cheeko_voice_changer.cc" "$GEN/voice_table.inc" \
  '^const CheekoVoiceChanger::VoiceInfo kVoices\[\]' \
  '^const CheekoVoiceChanger::VoiceInfo ?& ?CheekoVoiceChanger::GetVoiceInfo' \
  '^const char ?\* ?CheekoVoiceChanger::VoiceName' \
  '^const char ?\* ?CheekoVoiceChanger::VoiceEmoji'
python3 "$T/extract.py" "$B/cheeko_v2_board.cc" "$GEN/custom_lcd_display.inc" \
  '^namespace \{:::^\} // namespace' \
  '^class CustomLcdDisplay : public SpiLcdDisplay:::^\};'
# Harness-only accessor so the simulator can reach the display's CheekoOs.
python3 - "$GEN/custom_lcd_display.inc" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
i = s.rstrip().rfind("};")
s = s[:i] + "public:\n  // fwsim: harness accessor (not in firmware)\n  CheekoOs *fwsim_os() { return cheeko_os_.get(); }\n" + s[i:]
open(p, "w").write(s)
PY
python3 "$T/extract_haptics.py" "$B/cheeko_haptics.cc" "$GEN/haptics_names.cc"
