# fwsim — render the real Cheeko device screens from firmware source

Compiles the firmware's own LVGL UI code (cheeko-os-v2) headless on macOS and saves every screen as a PNG (296×240 plus 4×). Built 2026-09-28 for marketing videos; first run rendered 180 screens from b05c95d (fix/internal-ram-strategy, FW 2.4.311).

Run (the path must NOT contain spaces, "Cheeko Master" breaks the build):

    cp -R "/Users/ravikumar/Cheeko Master/marketing/tools/fwsim" /tmp/fwsim && cd /tmp/fwsim && ./render.sh <commit>

Output: out/*.png, out/4x/, out/contact_sheet.png, out/index.md. Never touches the firmware repo's working tree (it `git archive`s the commit). Stubbed: audio, network, NVS; clock 10:30 AM, battery 80%, Wi-Fi connected. The Imagine result image and sample reply text are placeholders.
