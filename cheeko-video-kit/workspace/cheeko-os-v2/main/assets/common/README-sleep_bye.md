# sleep_bye.ogg — PLACEHOLDER AUDIO, REPLACE BEFORE RELEASE

`sleep_bye.ogg` is the line Cheeko says just before soft-off ("I think you are
busy. Press me when you want to play again. Bye bye!").

The file currently in this folder was generated with the macOS `say` voice as a
placeholder so the feature could be tested on hardware. **It is not a Cheeko
voice and must not ship.** Re-record it through the normal character-voice
pipeline, in the house style (Hinglish, warm, desi-relatable — see the content
style guide), then drop the new file here under the same name.

Constraints, so the code needs no change:
- Ogg/Opus, mono, 48 kHz (match the other files in this folder)
- Keep it under ~4 s, or raise `kSoftOffGoodbyeMs` in `cheeko_v2_board.cc`
- After replacing, run: `python3 scripts/gen_lang.py --language en-US --output main/assets/lang_config.h`
  then `idf.py reconfigure` (the CMake glob is evaluated at configure time)
