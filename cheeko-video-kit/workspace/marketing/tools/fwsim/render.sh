#!/bin/sh
# Render the Cheeko device screens for a firmware commit, headless, on macOS.
#   ./render.sh [commit]        (default b05c95d)
# Needs: git, cmake, ninja, clang, python3; Pillow for the contact sheet
# (PY=/path/to/python with Pillow, default the cheeko-v2-website venv).
# Never touches the repo's working tree: the commit is `git archive`d into
# ./src, with the local managed_components/lvgl__lvgl reused from the repo.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="${REPO:-/Users/ravikumar/Cheeko Master/cheeko-os-v2}"
COMMIT="${1:-b05c95d}"
PY="${PY:-/Users/ravikumar/Cheeko Master/cheeko-v2-website/.venv/bin/python}"
cd "$HERE"

echo "== extract $COMMIT"
rm -rf src && mkdir -p src gen/assets out
git -C "$REPO" archive "$COMMIT" | tar -x -C src
git -C "$REPO" rev-parse "$COMMIT" > gen/commit.txt

echo "== dependencies"
mkdir -p deps
[ -d deps/lvgl ] || cp -R "$REPO/managed_components/lvgl__lvgl" deps/lvgl
[ -d deps/xiaozhi-fonts ] || cp -R "$REPO/managed_components/78__xiaozhi-fonts" deps/xiaozhi-fonts
[ -f deps/cjson/cJSON.c ] || { mkdir -p deps/cjson; cp "$HOME/esp/esp-idf/components/json/cJSON/cJSON."[ch] deps/cjson/; }

echo "== generated sources"
( cd src && python3 scripts/gen_lang.py --language en-US --output main/assets/lang_config.h >/dev/null )
mv src/main/assets/lang_config.h gen/assets/lang_config.h
python3 tools/gen_lang_blobs.py gen/assets/lang_config.h gen/lang_blobs.c
python3 tools/apply_defaults.py src config/sdkconfig.base.h config/sdkconfig.h
# Harness patch: SD card paths "/sdcard/..." -> "./sdcard/..." (run dir).
find src/main \( -name "*.cc" -o -name "*.h" -o -name "*.c" \) -print0 | xargs -0 sed -i '' 's|"/sdcard|"./sdcard|g'
tools/extract_board.sh src gen

echo "== SD card image"
rm -rf sdcard && mkdir -p sdcard/cheeko
cp -R src/CHEEKO_SD_CARD_COPY/cheeko/. sdcard/cheeko/
cp -Rn src/sd_card_assets/cheeko/. sdcard/cheeko/ 2>/dev/null || true

echo "== build"
cmake -S . -B build -G Ninja -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ >/dev/null
ninja -C build fwsim

echo "== render"
rm -rf out && mkdir -p out
./build/fwsim out
for m in dinku robu; do
  ./build/fwsim out --mascot $m --group home --group menu --group talk --group voice
done
for th in 1 2 3; do   # Night, Ocean, Candy: home + menu, for the app's theme setting (V25)
  ./build/fwsim out --theme $th --group home --group menu
done

echo "== contact sheet + index"
"$PY" tools/sheet.py out --cols 6
python3 tools/make_index.py out tools/index_header.md
echo "done: $HERE/out"
