#!/bin/zsh
# Re-renders every PNG from the app's real widgets, as iPhone (iOS), into the
# website's assets/img/app-shots-ios/ (the older Android-look set in
# assets/img/app-shots/ is left alone for the videos that use it).
# Works on a throwaway copy of the repo; the owner's checkout is only read.
#
#   zsh run.sh            (env: OUT, REPO, COMMIT, SIM, FLUTTER to override)
set -e
HERE=${0:A:h}
OUT=${OUT:-"/Users/ravikumar/Cheeko Master/cheeko-v2-website/assets/img/app-shots-ios"}
REPO=${REPO:-"/Users/ravikumar/Cheeko Master/CheekoAI-Parent-App"}
COMMIT=${COMMIT:-d49af42}
SIM=${SIM:-"${HERE:h:h}/appsim"}
FLUTTER=${FLUTTER:-/opt/homebrew/bin/flutter}

if [[ ! -d "$SIM/lib" ]]; then
  mkdir -p "$SIM"
  git -C "$REPO" archive "$COMMIT" | tar -x -C "$SIM"
  rm -f "$SIM"/cheekoai-firebase-adminsdk-*.json
  # The lockfile needs Flutter >= 3.38. On the 3.32 SDK installed here, apply
  # the API-rename shims and let pub resolve again. Skip both on 3.38+.
  if ! "$FLUTTER" --version | grep -qE "Flutter 3\.(3[89]|[4-9][0-9])"; then
    rm -f "$SIM/pubspec.lock"
    (cd "$SIM" && patch -p1 < "$HERE/flutter-3.32-compat.patch")
  fi
  touch "$SIM/.env"   # declared as an asset in pubspec.yaml
  (cd "$SIM" && "$FLUTTER" pub get)
fi

rm -rf "$SIM/test/appshots"
mkdir -p "$SIM/test/appshots"
cp -R "$HERE"/*.dart "$HERE/support" "$HERE/media" "$SIM/test/appshots/"
mkdir -p "$OUT/setup"
(cd "$SIM" && APPSHOTS_OUT="$OUT" "$FLUTTER" test test/appshots/)

# Contact sheet: every phone-size capture, then the tall ones.
FONT="$SIM/assets/fonts/nunito-variable.ttf"
# The onboarding batch reuses three of the screens above.
cp "$OUT/09_pairing_code.png" "$OUT/setup/s09_code_empty.png"
cp "$OUT/09_pairing_code_entered.png" "$OUT/setup/s09_code_entered.png"
cp "$OUT/01_home.png" "$OUT/setup/s11_home_after_setup.png"
(cd "$OUT/setup" && rm -f contact_sheet.png && magick montage -font "$FONT" \
  -pointsize 22 -label '%t' $(cd "$OUT/setup" && ls s*.png) -tile 7x \
  -geometry 300x650+10+10 -background '#f3efe9' contact_sheet.png)

cd "$OUT"
TMP=$(mktemp -d)
magick montage -font "$FONT" -pointsize 22 -label '%t' \
  $(ls *.png | grep -v contact_sheet | grep -v _full) \
  -tile 7x -geometry 300x650+14+14 -background '#f3efe9' "$TMP/grid.png"
magick montage -font "$FONT" -pointsize 22 -label '%t' \
  $(ls *_full.png) \
  -tile 5x -geometry x1500+14+14 -background '#f3efe9' "$TMP/full.png"
magick "$TMP/grid.png" "$TMP/full.png" -background '#f3efe9' -gravity center \
  -append contact_sheet.png
rm -rf "$TMP"
echo "done: $OUT"
