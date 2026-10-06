"""Copy Cheeko marketing videos into the shared Drive folder, one folder per video, one sub-folder per stage.

Drive folder: "My Drive/cheeko ai videos" (https://drive.google.com/drive/folders/1UKxS504Qrz3kz__yzoQxep8K_Viz4-BR),
synced to this Mac by Google Drive for desktop, so writing here uploads it.

Usage:  python publish_to_drive.py            # (re)build every video in VIDEOS
        python publish_to_drive.py V05         # one video
Safe to re-run: files are overwritten, nothing outside the managed names is deleted.
"""
import shutil, subprocess, sys, os, json, re
from pathlib import Path

DRIVE = Path.home() / "Library/CloudStorage/GoogleDrive-ravi.ramp36@gmail.com/My Drive/cheeko ai videos"
REPO = Path("/Users/ravikumar/Cheeko Master/cheeko-v2-website")
MKT = Path("/Users/ravikumar/Cheeko Master/marketing")

# id, title, slug, repo folder, format, seconds, status, voice, notes
VIDEOS = [
    ("V01", "Everything Cheeko Does", "Everything-Cheeko-Does", "brag-output", "Film", 22.0, "Final draft",
     "No voiceover (music only)", "All 8 features in 22s: cards, Talk, Imagine, Games, Languages, Radio, Funny Voice, Parent app."),
    ("V02", "Hand Them Cheeko", "Hand-Them-Cheeko", "brag-output-2026-09-28-095057", "Film", 22.5, "Final draft",
     "No voiceover (music only)", "The cards: \"Kid bored? Skip the phone. Hand them Cheeko.\" Story, rhyme and game cards go in."),
    ("V03", "No Tantrum", "No-Tantrum", "brag-output-2026-09-28-reel", "Reel", 31.45, "Final draft",
     "MiniMax speech-2.8-hd, English_Upbeat_Woman, a different emotion per line",
     "\"Took the phone away... and NO tantrum?!\" Fast feature tour for Instagram Reels."),
    ("V04", "Built to END", "Built-to-END", "brag-output-2026-09-28-made-to-end", "Reel", 34.61, "Final draft",
     "MiniMax speech-2.8-hd, English_Upbeat_Woman, a different emotion per line",
     "\"Your phone is built to never end. Cheeko? Built to END!\" The screen that stops."),
    ("V05", "Made in India", "Made-in-India", "brag-output-2026-09-28-made-in-india", "Reel", 37.09, "Final draft",
     "MiniMax speech-2.8-hd, English_Upbeat_Woman, a different emotion per line",
     "\"Guess this sound!\" Pressure cooker hook, Sounds Around Me card, Nani, Imagine, languages, built by Indian parents."),
    ("V06", "Five Minutes", "Five-Minutes", "brag-output-2026-09-29-five-minutes", "Reel", 34.36, "Final draft",
     "MiniMax speech-2.8-hd, English_Upbeat_Woman at 1.08x (the phone) + hindi_female_2_v1 (Nani), a different emotion per line",
     "2D sticker ad in Ravi's family sticker style. The family phone narrates: \"five minutes\" became dinner, football and ONE MORE, then Cheeko showed up. Music: Envato Elements \"Sneaky Pizzicato Comedy\" by Korolkov."),
    ("V03-HI", "No Tantrum (Hindi)", "No-Tantrum-Hindi", "brag-output-2026-09-28-reel-hi", "Reel", 28.2, "Final draft",
     "MiniMax speech-2.8-hd, hindi_male_1_v2, a different emotion per line", "Hindi version of V03."),
    ("V04-HI", "Built to END (Hindi)", "Built-to-END-Hindi", "brag-output-2026-09-28-made-to-end-hi", "Reel", 31.26, "Final draft",
     "MiniMax speech-2.8-hd, hindi_male_1_v2, a different emotion per line", "Hindi version of V04."),
    ("V05-HI", "Made in India (Hindi)", "Made-in-India-Hindi", "brag-output-2026-09-28-made-in-india-hi", "Reel", 37.4, "Final draft",
     "MiniMax speech-2.8-hd, hindi_male_1_v2, a different emotion per line", "Hindi version of V05."),
]
VIDEOS.append(("V07", "Little Moments More Connection", "Little-Moments-More-Connection", "brag-output-2026-09-29-little-moments", "Reel", 26.82, "Draft for review", "MiniMax speech-2.8-hd, English_Upbeat_Woman, per-line emotions", "Illustrated family situations, corrected product reference, original music."))

VIDEOS.append(("V08", "Tiny CEO", "Tiny-CEO", "brag-output-2026-09-29-tiny-ceo", "Reel", 33.79, "Draft for review", "MiniMax speech-2.8-hd, English_Upbeat_Woman, per-line emotions", "Original sarcastic parent-facing reel: child inherits an adult feed. Three-crayon portfolio callback; original comedy music."))
VIDEOS.append(("V09", "Tiny Adults", "Tiny-Adults", "brag-output-2026-09-29-tiny-adults", "Reel", 43.89, "Final draft",
     "MiniMax speech-2.8-hd: narrator English_Upbeat_Woman 1.1x + five kid voices 1.12x (Strong-WilledBoy, PlayfulGirl, UpsetGirl, SadTeen, Soft-spokenGirl)",
     "2D sticker ad. Phone-raised kids at a 7th birthday act like tiny adults (CEO, influencer, news anchor, WhatsApp uncle, burnt out), freeze, rewind, Cheeko turns them back into kids. Music: Envato Elements \"Quirky Fun Sports Party Dance\" by SunChannelMusic."))

# One feature per video (V11-V18), English + Hindi, 2026-09-29. Built from marketing/tools/feature (template) + feature_lines*.json.
VIDEOS.append(("V11", "Ask Anything", "Ask-Anything", "brag-output-2026-09-29-talk", "Reel", 26.84, "Final draft", "MiniMax narrator English_Upbeat_Woman; characters Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, kid English_LovelyGirl, grandma English_Wiselady (MiniMax); Mitthu loongnorahu, Quizzy loongivyhu (Qwen)", "One feature per video: Ask Anything."))
VIDEOS.append(("V11-HI", "Ask Anything (Hindi)", "Ask-Anything-Hindi", "brag-output-2026-09-29-talk-hi", "Reel", 31.22, "Final draft", "MiniMax Hindi: narrator hindi_male_1_v2; Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, Mitthu English_Upbeat_Woman, Quizzy hindi_female_1_v2, kid English_LovelyGirl, grandma hindi_female_2_v1 (all language_boost Hindi)", "One feature per video: Ask Anything. Hindi version."))
VIDEOS.append(("V12", "Imagine", "Imagine", "brag-output-2026-09-29-imagine", "Reel", 25.93, "Final draft", "MiniMax narrator English_Upbeat_Woman; characters Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, kid English_LovelyGirl, grandma English_Wiselady (MiniMax); Mitthu loongnorahu, Quizzy loongivyhu (Qwen)", "One feature per video: Imagine."))
VIDEOS.append(("V12-HI", "Imagine (Hindi)", "Imagine-Hindi", "brag-output-2026-09-29-imagine-hi", "Reel", 26.62, "Final draft", "MiniMax Hindi: narrator hindi_male_1_v2; Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, Mitthu English_Upbeat_Woman, Quizzy hindi_female_1_v2, kid English_LovelyGirl, grandma hindi_female_2_v1 (all language_boost Hindi)", "One feature per video: Imagine. Hindi version."))
VIDEOS.append(("V13", "Funny Voice", "Funny-Voice", "brag-output-2026-09-29-funny-voice", "Reel", 32.38, "Final draft", "MiniMax narrator English_Upbeat_Woman; characters Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, kid English_LovelyGirl, grandma English_Wiselady (MiniMax); Mitthu loongnorahu, Quizzy loongivyhu (Qwen)", "One feature per video: Funny Voice."))
VIDEOS.append(("V13-HI", "Funny Voice (Hindi)", "Funny-Voice-Hindi", "brag-output-2026-09-29-funny-voice-hi", "Reel", 37.99, "Final draft", "MiniMax Hindi: narrator hindi_male_1_v2; Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, Mitthu English_Upbeat_Woman, Quizzy hindi_female_1_v2, kid English_LovelyGirl, grandma hindi_female_2_v1 (all language_boost Hindi)", "One feature per video: Funny Voice. Hindi version."))
VIDEOS.append(("V14", "Offline Games", "Offline-Games", "brag-output-2026-09-29-games", "Reel", 27.03, "Final draft", "MiniMax narrator English_Upbeat_Woman; characters Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, kid English_LovelyGirl, grandma English_Wiselady (MiniMax); Mitthu loongnorahu, Quizzy loongivyhu (Qwen)", "One feature per video: Offline Games."))
VIDEOS.append(("V14-HI", "Offline Games (Hindi)", "Offline-Games-Hindi", "brag-output-2026-09-29-games-hi", "Reel", 27.45, "Final draft", "MiniMax Hindi: narrator hindi_male_1_v2; Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, Mitthu English_Upbeat_Woman, Quizzy hindi_female_1_v2, kid English_LovelyGirl, grandma hindi_female_2_v1 (all language_boost Hindi)", "One feature per video: Offline Games. Hindi version."))
VIDEOS.append(("V15", "Grandmas Voice", "Grandmas-Voice", "brag-output-2026-09-29-grandmas-voice", "Reel", 26.49, "Final draft", "MiniMax narrator English_Upbeat_Woman; characters Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, kid English_LovelyGirl, grandma English_Wiselady (MiniMax); Mitthu loongnorahu, Quizzy loongivyhu (Qwen)", "One feature per video: Grandmas Voice."))
VIDEOS.append(("V15-HI", "Grandmas Voice (Hindi)", "Grandmas-Voice-Hindi", "brag-output-2026-09-29-grandmas-voice-hi", "Reel", 28.95, "Final draft", "MiniMax Hindi: narrator hindi_male_1_v2; Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, Mitthu English_Upbeat_Woman, Quizzy hindi_female_1_v2, kid English_LovelyGirl, grandma hindi_female_2_v1 (all language_boost Hindi)", "One feature per video: Grandmas Voice. Hindi version."))
VIDEOS.append(("V16", "Nani Storyteller", "Nani-Storyteller", "brag-output-2026-09-29-nani", "Reel", 31.43, "Final draft", "MiniMax narrator English_Upbeat_Woman; characters Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, kid English_LovelyGirl, grandma English_Wiselady (MiniMax); Mitthu loongnorahu, Quizzy loongivyhu (Qwen)", "One feature per video: Nani Storyteller."))
VIDEOS.append(("V16-HI", "Nani Storyteller (Hindi)", "Nani-Storyteller-Hindi", "brag-output-2026-09-29-nani-hi", "Reel", 34.91, "Final draft", "MiniMax Hindi: narrator hindi_male_1_v2; Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, Mitthu English_Upbeat_Woman, Quizzy hindi_female_1_v2, kid English_LovelyGirl, grandma hindi_female_2_v1 (all language_boost Hindi)", "One feature per video: Nani Storyteller. Hindi version."))
VIDEOS.append(("V17", "Quizzy", "Quizzy", "brag-output-2026-09-29-quizzy", "Reel", 25.16, "Final draft", "MiniMax narrator English_Upbeat_Woman; characters Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, kid English_LovelyGirl, grandma English_Wiselady (MiniMax); Mitthu loongnorahu, Quizzy loongivyhu (Qwen)", "One feature per video: Quizzy."))
VIDEOS.append(("V17-HI", "Quizzy (Hindi)", "Quizzy-Hindi", "brag-output-2026-09-29-quizzy-hi", "Reel", 26.44, "Final draft", "MiniMax Hindi: narrator hindi_male_1_v2; Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, Mitthu English_Upbeat_Woman, Quizzy hindi_female_1_v2, kid English_LovelyGirl, grandma hindi_female_2_v1 (all language_boost Hindi)", "One feature per video: Quizzy. Hindi version."))
VIDEOS.append(("V18", "Mitthu English Teacher", "Mitthu-English-Teacher", "brag-output-2026-09-29-mitthu", "Reel", 37.6, "Final draft", "MiniMax narrator English_Upbeat_Woman; characters Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, kid English_LovelyGirl, grandma English_Wiselady (MiniMax); Mitthu loongnorahu, Quizzy loongivyhu (Qwen)", "One feature per video: Mitthu English Teacher."))
VIDEOS.append(("V18-HI", "Mitthu English Teacher (Hindi)", "Mitthu-English-Teacher-Hindi", "brag-output-2026-09-29-mitthu-hi", "Reel", 35.27, "Final draft", "MiniMax Hindi: narrator hindi_male_1_v2; Cheeko English_PlayfulGirl, Nani English_Graceful_Lady, Mitthu English_Upbeat_Woman, Quizzy hindi_female_1_v2, kid English_LovelyGirl, grandma hindi_female_2_v1 (all language_boost Hindi)", "One feature per video: Mitthu English Teacher. Hindi version."))

VIDEOS.append(("V19", "Parent App", "Parent-App", "brag-output-2026-09-29-parent-app", "Reel", 38.45, "Final draft", "MiniMax English_Upbeat_Woman narrator, 1.1x", "Parent app: safety and control. Real app screens rendered from the Flutter widgets."))
VIDEOS.append(("V19-HI", "Parent App (Hindi)", "Parent-App-Hindi", "brag-output-2026-09-29-parent-app-hi", "Reel", 42.55, "Final draft", "MiniMax hindi_male_1_v2 narrator, 1.1x", "Parent app: safety and control. Real app screens rendered from the Flutter widgets."))

# Getting Started series (V20-V24), 2026-09-29
VIDEOS.append(("V20", "Meet Cheeko", "Meet-Cheeko", "brag-output-2026-09-29-meet-cheeko", "Reel", 51.79, "Draft for review", "MiniMax English_Upbeat_Woman narrator 1.05x, Cheeko English_PlayfulGirl", "Getting Started part 1 of 4. Re-render with the other parts at the end."))

VIDEOS.append(("V21", "Switch On and Learn to Play", "Switch-On-and-Learn-to-Play", "brag-output-2026-09-29-switch-on", "Reel", 43.17, "Draft for review", "MiniMax English_Upbeat_Woman narrator 1.05x, Cheeko English_PlayfulGirl", "Getting Started part 2 of 4."))

VIDEOS.append(("V22", "Connect Cheeko", "Connect-Cheeko", "brag-output-2026-09-29-connect", "Reel", 43.53, "Draft for review", "MiniMax English_Upbeat_Woman narrator 1.05x, Cheeko English_PlayfulGirl", "Getting Started part 3 of 4."))
VIDEOS.append(("V23", "Your First Five Minutes", "Your-First-Five-Minutes", "brag-output-2026-09-29-first-five-minutes", "Reel", 44.07, "Draft for review", "MiniMax English_Upbeat_Woman narrator 1.05x, Cheeko English_PlayfulGirl, kid English_LovelyGirl", "Getting Started part 4 of 4."))
# Cheeko App Guide (V25), parent app walkthrough, 2026-09-29
VIDEOS.append(("V25.1", "App Guide Home", "App-Guide-Home", "brag-output-2026-09-29-app-home", "Reel", 35.61, "Draft for review", "MiniMax English_Upbeat_Woman narrator 1.05x", "Cheeko App Guide part 1 of 5. Real app screens rendered as iOS on an iPhone body."))
VIDEOS.append(("V25.2", "App Guide Device", "App-Guide-Device", "brag-output-2026-09-29-app-device", "Reel", 35.84, "Draft for review", "MiniMax English_Upbeat_Woman narrator 1.05x", "Cheeko App Guide part 2 of 5. Real app screens rendered as iOS on an iPhone body."))
VIDEOS.append(("V25.3", "App Guide Analytics", "App-Guide-Analytics", "brag-output-2026-09-29-app-analytics", "Reel", 25.83, "Draft for review", "MiniMax English_Upbeat_Woman narrator 1.05x", "Cheeko App Guide part 3 of 5. Real app screens rendered as iOS on an iPhone body."))
VIDEOS.append(("V25.4", "App Guide Gallery and Custom Cards", "App-Guide-Gallery-and-Custom-Cards", "brag-output-2026-09-29-app-gallery-cards", "Reel", 30.56, "Draft for review", "MiniMax English_Upbeat_Woman narrator 1.05x", "Cheeko App Guide part 4 of 5. Real app screens rendered as iOS on an iPhone body."))
VIDEOS.append(("V25.5", "App Guide Profile", "App-Guide-Profile", "brag-output-2026-09-29-app-profile", "Reel", 37.42, "Draft for review", "MiniMax English_Upbeat_Woman narrator 1.05x", "Cheeko App Guide part 5 of 5. Real app screens rendered as iOS on an iPhone body."))
VIDEOS.append(("V25.1-HI", "App Guide Home (Hindi)", "App-Guide-Home-Hindi", "brag-output-2026-09-29-app-home-hi", "Reel", 40.43, "Draft for review", "MiniMax hindi_male_1_v2 narrator 1.08x", "Cheeko App Guide part 1 of 5, Hindi. App screens stay English (the app has no Hindi UI)."))
VIDEOS.append(("V25.2-HI", "App Guide Device (Hindi)", "App-Guide-Device-Hindi", "brag-output-2026-09-29-app-device-hi", "Reel", 39.16, "Draft for review", "MiniMax hindi_male_1_v2 narrator 1.08x", "Cheeko App Guide part 2 of 5, Hindi. App screens stay English (the app has no Hindi UI)."))
VIDEOS.append(("V25.3-HI", "App Guide Analytics (Hindi)", "App-Guide-Analytics-Hindi", "brag-output-2026-09-29-app-analytics-hi", "Reel", 29.16, "Draft for review", "MiniMax hindi_male_1_v2 narrator 1.08x", "Cheeko App Guide part 3 of 5, Hindi. App screens stay English (the app has no Hindi UI)."))
VIDEOS.append(("V25.4-HI", "App Guide Gallery and Custom Cards (Hindi)", "App-Guide-Gallery-and-Custom-Cards-Hindi", "brag-output-2026-09-29-app-gallery-cards-hi", "Reel", 34.07, "Draft for review", "MiniMax hindi_male_1_v2 narrator 1.08x", "Cheeko App Guide part 4 of 5, Hindi. App screens stay English (the app has no Hindi UI)."))
VIDEOS.append(("V25.5-HI", "App Guide Profile (Hindi)", "App-Guide-Profile-Hindi", "brag-output-2026-09-29-app-profile-hi", "Reel", 42.06, "Draft for review", "MiniMax hindi_male_1_v2 narrator 1.08x", "Cheeko App Guide part 5 of 5, Hindi. App screens stay English (the app has no Hindi UI)."))
VIDEOS.append(("V25", "Cheeko App Guide", "Cheeko-App-Guide", "brag-output-2026-09-29-app-guide-full", "Film", 156.46, "Draft for review", "MiniMax English_Upbeat_Woman narrator 1.05x", "All five App Guide parts stitched (stitch_series.py): vertical plus a 16:9 cut with chapter list."))
VIDEOS.append(("V26", "Make Your Own Card", "Make-Your-Own-Card", "brag-output-2026-09-30-make-your-own", "Reel", 60.6, "Draft for review", "MiniMax English_Upbeat_Woman narrator, Mom English_CalmWoman, Grandma English_Wiselady, kid English_LovelyGirl", "The whole custom card flow in the app, the card into the back pocket, then loved ones, favourites and again and again. New design."))
VIDEOS.append(("V25-HI", "Cheeko App Guide (Hindi)", "Cheeko-App-Guide-Hindi", "brag-output-2026-09-29-app-guide-full-hi", "Film", 176.08, "Draft for review", "MiniMax hindi_male_1_v2 narrator 1.08x", "All five Hindi App Guide parts stitched: vertical plus a 16:9 cut with chapter list."))

ARCHIVE = ("X01", "Manifesto (rejected)", "Manifesto-REJECTED", "brag-output-2026-09-28-manifesto", "Film", 37.5, "Rejected",
           "Sarvam bulbul:v3 kavya", "Too slow and too calm for Reels, same girl twice in one collage. Kept for reference only.")


# A series lives in its own Drive folder with everything it needs: plan, every part (1 Script ... 5 Source, incl. the
# images each part uses), and its own Ready to post. The main Ready to post and root stay for standalone videos.
SERIES = {"Onboarding Cheeko": {"ids": ("V20", "V21", "V22", "V23", "V24"), "plan": "getting-started-series-plan.md",
                                "plan_name": "Onboarding Cheeko - plan and scripts (V20-V24).md"},
          "Cheeko App Guide": {"ids": ("V25", "V25.1", "V25.2", "V25.3", "V25.4", "V25.5"), "plan": "app-walkthrough-plan.md",
                               "plan_name": "Cheeko App Guide - plan and script (V25).md"}}


def _root_for(vid):
    for name, sr in SERIES.items():
        if vid.replace("-HI", "") in sr["ids"]: return DRIVE / name
    return DRIVE


def _assets_used(src, dst):
    """Copy every image a feature spec.js points at (plus the device frame and logo) into dst, keeping assets/img paths."""
    import re as _re
    img = REPO / "assets/img"; names = {"device_current.png", "logo.png", "device_live_screen_mask.png"}
    for q in _re.findall(r"'([A-Za-z0-9_./-]+)'", (src / "work/spec.js").read_text()):
        for cand in (q, f"fw-screens/{q}.png"):
            if (img / cand).is_file(): names.add(cand)
    for n in sorted(names):
        (dst / n).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(img / n, dst / n)
    return len(names)


def run(*a):
    subprocess.run([str(x) for x in a], check=True)


def mp3(src, dst, br="160k"):
    run("ffmpeg", "-y", "-loglevel", "error", "-i", src, "-c:a", "libmp3lame", "-b:a", br, dst)


def contact_sheet(mp4, dst, secs):
    # one frame every ~1.5s, 6 across: the "test frames" view we check before every final render
    n = max(6, int(secs / 1.5))
    rows = (n + 5) // 6
    run("ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-vf",
        f"fps={n}/{secs},scale=270:-1,tile=6x{rows}:padding=6:color=white", "-frames:v", "1", "-q:v", "3", dst)


def build(v, root):
    vid, title, slug, repo_dir, fmt, secs, status, voice, notes = v
    src = REPO / repo_dir
    base = root / f"{vid} {title}"
    s1, s2, s3, s4, s5 = (base / n for n in ("1 Script", "2 Voice", "3 Test", "4 Final", "5 Source"))
    for d in (s1, s2, s3, s4, s5):
        d.mkdir(parents=True, exist_ok=True)
    stem = f"Cheeko_{vid}_{slug}_{fmt}_9x16_{round(secs)}s"

    # 1 Script
    shutil.copy2(src / "brag-plan.md", s1 / f"{vid} {title} - script and shot list.md")
    shutil.copy2(src / "share-copy.txt", s1 / f"{vid} {title} - Instagram caption.txt")
    # plain voiceover text, one line per clip, for pasting into any TTS tool
    import json as _j, re as _re
    hindi = vid.endswith("-HI"); _vbase = vid.replace("-HI", "")
    spec = _lines_for(vid, repo_dir)
    if spec:
        txt = "\n".join(_re.sub(r"\s*\([a-z][a-z -]*\)", "", l[-3]).strip() for l in spec["lines"] if l[-3].strip()) + "\n"   # drop (laughs), (sighs)...
        (s1 / f"{vid} voiceover text (for TTS) - {'Hindi' if hindi else 'English'}.txt").write_text(txt)

    # 2 Voice: raw takes, the tightened VO the video uses, music-only bed
    vo = src / "work/vo"
    if vo.exists():
        if (vo / "clips").exists():   # current voice: one clip per line, each with its own emotion
            (s2 / "Lines (one clip per line)").mkdir(exist_ok=True)
            for f in sorted((vo / "clips").glob("*.mp3")):
                shutil.copy2(f, s2 / "Lines (one clip per line)" / f.name)
        else:
            for f in sorted(vo.glob("take*.mp3")) + sorted(vo.glob("card*.mp3")):
                shutil.copy2(f, s2 / f"{vid} voice take - {f.stem}.mp3")
        if (vo / "radiant.wav").exists() and not (vo / "clips").exists():
            mp3(vo / "radiant.wav", s2 / f"{vid} voice take - full.mp3")
        if (vo / "vo-tight.wav").exists():
            mp3(vo / "vo-tight.wav", s2 / f"{vid} voiceover - FINAL (tightened).mp3")
    if (src / "work/music-only.wav").exists():
        mp3(src / "work/music-only.wav", s2 / f"{vid} music only (no voice).mp3")
    if (src / "voice-samples").exists():
        for f in sorted((src / "voice-samples").rglob("*")):
            if f.is_file():
                shutil.copy2(f, s2 / f"voice sample - {f.name}")

    # 3 Test: frame contact sheet of the render
    contact_sheet(src / "brag.mp4", s3 / f"{vid} test frames - every 1.5s.jpg", secs)

    # 4 Final
    shutil.copy2(src / "brag.mp4", s4 / f"{stem}.mp4")
    shutil.copy2(src / "brag.jpg", s4 / f"{stem}_poster.jpg")
    if (src / "thumbnail.jpg").exists():   # designed Reel cover (1080x1920), made by cheeko-v2-website/thumbs-work/make_thumbs.mjs
        shutil.copy2(src / "thumbnail.jpg", s4 / f"{stem}_thumbnail.jpg")
    shutil.copy2(src / "share-copy.txt", s4 / f"{stem}_caption.txt")
    stem16 = stem.replace("_9x16_", "_16x9_")   # full films (stitch_series.py): 16:9 cut for YouTube and the website
    if (src / "brag-16x9.mp4").exists(): shutil.copy2(src / "brag-16x9.mp4", s4 / f"{stem16}.mp4")
    if (src / "thumbnail-16x9.jpg").exists(): shutil.copy2(src / "thumbnail-16x9.jpg", s4 / f"{stem16}_thumbnail.jpg")
    if (src / "work/chapters.txt").exists(): shutil.copy2(src / "work/chapters.txt", s4 / f"{stem16}_youtube_chapters.txt")

    # 5 Source: enough to re-render (renders, stills and WAVs are rebuilt, not stored)
    for f in ("compose.html", "spec.js", "timing.js", "timing.json", "cues.json", "cues.mjs", "synth.py", "mix.py", "cut_panels.py", "cut_stickers.py", "review_sheet.py", "render.mjs", "stills.mjs", "finish.sh", "pw.mjs", "sheet.py", "warp.json", "stitch.json", "chapters.txt"):
        if (src / "work" / f).exists():
            shutil.copy2(src / "work" / f, s5 / f)
    # sticker videos (V06+): sticker art, real device sounds and the licensed music track
    for d, name in (("stickers", "stickers"), ("sfx", "sfx"), ("music", "music (licensed, Envato Elements)")):
        if (src / "work" / d).is_dir():
            shutil.copytree(src / "work" / d, s5 / name, dirs_exist_ok=True)
    if root != DRIVE and root.parent == DRIVE and (src / "work/spec.js").exists():
        _assets_used(src, s5 / "assets used (assets-img)")
    lines_spec = _lines_for(vid, repo_dir)
    if lines_spec:
        (s5 / "voice-lines.json").write_text(json.dumps(lines_spec, ensure_ascii=False, indent=1))
    (base / "TECHNICAL.md").write_text(_technical(vid, title, repo_dir, fmt, secs, voice, stem, src, lines_spec))
    # superseded finals (older length in the name) move out of the way instead of sitting next to the new one
    for f in list(s4.iterdir()):
        if f.is_file() and not f.name.startswith(stem) and not f.name.startswith(stem.replace("_9x16_", "_16x9_")):
            (s4 / "older versions").mkdir(exist_ok=True); shutil.move(str(f), str(s4 / "older versions" / f.name))
    (s5 / "README.txt").write_text(
        f"Source for {vid} {title}. Lives in the website repo at cheeko-v2-website/{repo_dir}/work/.\n"
        "Re-render with the cheeko-video skill: node render.mjs ffmpeg <seconds>, then bash finish.sh ffmpeg <seconds> <poster-time>.\n")

    (base / "STATUS.txt").write_text(
        f"{vid} {title}\nStatus: {status}\nFormat: {fmt}, vertical 1080x1920, {secs}s\nVoice: {voice}\n{notes}\n"
        f"Final file: 4 Final/{stem}.mp4\nRepo folder: cheeko-v2-website/{repo_dir}\n")
    return vid, title, fmt, secs, status, voice, stem


def _lines_for(vid, repo_dir):
    hindi = vid.endswith("-HI"); base = vid.replace("-HI", "")
    # feature Reels (V11-V18): lines live in feature_lines*.json, keyed by slug instead of dir
    ff = Path(__file__).with_name("feature_lines_hi.json" if hindi else "feature_lines.json")
    if ff.exists():
        spec = json.loads(ff.read_text()).get(base)
        if spec and "brag-output-2026-09-29-" + spec["slug"] + ("-hi" if hindi else "") == repo_dir:
            return {"dir": repo_dir, "lines": [[l[1], l[2], 0, l[3]] for l in spec["lines"]]}
    f = Path(__file__).with_name("vo_lines_hi.json" if hindi else "vo_lines.json")
    if not f.exists(): return None
    spec = json.loads(f.read_text()).get(base)
    return spec if spec and spec["dir"] + ("-hi" if hindi else "") == repo_dir else None


def _technical(vid, title, repo_dir, fmt, secs, voice, stem, src, lines_spec):
    if (src / "work/stitch.json").exists():     # a full film stitched from series parts (stitch_series.py)
        cfg = json.loads((src / "work/stitch.json").read_text())
        name = next((n for n, sr in SERIES.items() if vid.replace("-HI", "") in sr["ids"]), "")
        return "\n".join([f"# {vid} {title}: technical notes", "",
            f"The {len(cfg['parts'])} parts of {name or 'the series'} stitched into one film by `marketing/tools/stitch_series.py`.", "",
            f"- Vertical: `4 Final/{stem}.mp4`. 16:9 for YouTube and the website: `4 Final/{stem.replace('_9x16_', '_16x9_')}.mp4` (the vertical film centred in a Cheeko frame, title left, chapter list right, lit for the current chapter; frame page `marketing/tools/stitch/series_frame.html`).",
            f"- Parts, in order: " + ", ".join(f"`{p}`" for p in cfg["parts"]) + ". Each part but the last is cut 1.2 s after its last voice line, so its \"Next\" card becomes the chapter card.",
            "- YouTube chapters: `" + stem.replace("_9x16_", "_16x9_") + "_youtube_chapters.txt`.", "",
            "## Rebuild", "", "Re-render any part first (its own folder), then:", "", "```bash",
            'cd "/Users/ravikumar/Cheeko Master/marketing/tools"',
            f"../../cheeko-v2-website/.venv/bin/python stitch_series.py stitch/<config>.json   # config copy: 5 Source/stitch.json",
            "```", ""])
    comp = (src / "work/compose.html").read_text()
    assets = sorted(set(re.findall(r"\.\./\.\./assets/img/([^'\")]+\.(?:png|jpe?g|svg))", comp)))
    hindi = vid.endswith("-HI")
    L = [f"# {vid} {title}: technical notes", "",
         f"Reference for rebuilding or changing this video. The general pipeline is in `00 Plan/HOW WE MAKE CHEEKO VIDEOS.md`.", "",
         "| | |", "|---|---|",
         f"| Format | {fmt}, vertical 1080x1920, 30 fps, {secs}s |",
         f"| Voice | {voice} |",
         f"| Source folder (Mac) | `/Users/ravikumar/Cheeko Master/cheeko-v2-website/{repo_dir}/` (work/ = source) |",
         f"| Repo | Craftech360-projects/cheeko-v2-website, branch claude/website-launch-video-3xp8rq |",
         f"| Final file | `4 Final/{stem}.mp4` (+ `_thumbnail.jpg`, `_poster.jpg`, `_caption.txt`) |", "",
         "## Files in 5 Source", "",
         "- `compose.html`: the whole video as one page. `window.render(t)` draws frame `t`; `const CAPS` = word captions; `<script id=\"warp\">` maps real time to the scene timeline so scenes follow the voice.",
         ("- `mix.py`: voiceover + sound effects (real Cheeko sounds in `sfx/`, synthesised pops and stamps) + the licensed track in `music (licensed, Envato Elements)`, ducked under the voice, writes `music-final.wav`. `stickers/` holds the sticker art (`cut_panels.py` cuts the storyboard panels)."
          if (src / "work/mix.py").exists() else
          "- `synth.py`: original music and sound effects (numpy), ducked under `vo/vo-tight.wav`, writes `music-final.wav`."),
         "- `warp.json`: voice anchors (`new` = seconds in the final video, `old` = seconds in the composition) and total duration.",
         "- `voice-lines.json`: every voice line with its emotion, old start time and gap (the input to `build_vo.py`).",
         "- `render.mjs`, `stills.mjs`, `sheet.py`, `finish.sh`, `pw.mjs`: render, check and finish scripts.", ""]
    if lines_spec:
        L += ["## Voice lines", "", "| # | Emotion | Line |", "|---|---|---|"]
        for i, l in enumerate(lines_spec["lines"]):
            L.append(f"| {i:02d} | {l[-4]} | {l[-3]} |")
        L += ["", "Clips are in `2 Voice/Lines (one clip per line)`, one mp3 per line, named by line number.", ""]
    L += ["## Rebuild", "", "```bash", f'cd "/Users/ravikumar/Cheeko Master/cheeko-v2-website/{repo_dir}/work"']
    if lines_spec:
        L += ["# after changing a voice line: record it on the dev box (MiniMax, see HOW WE MAKE CHEEKO VIDEOS), put all clips in one folder, then",
              f'( cd "/Users/ravikumar/Cheeko Master/marketing/tools" && VIDS={vid.replace("-HI", "")} ../../cheeko-v2-website/.venv/bin/python build_vo.py <clips dir>{" vo_lines_hi.json -hi" if hindi else ""} )']
        if hindi: L += ['( cd "/Users/ravikumar/Cheeko Master/marketing/tools" && python3 make_hindi.py )   # Hindi captions, text and warp']
        L += ["D=$(python3 -c \"import json;print(json.load(open('warp.json'))['dur'])\")"]
    else:
        L += [f"D={secs}"]
    mixer = (src / "work/mix.py").exists()
    L += ["../../.venv/bin/python mix.py              # voice + sfx + licensed music" if mixer else "../../.venv/bin/python synth.py            # music",
          "node stills.mjs 1 5 10 15 && ../../.venv/bin/python sheet.py 4   # check frames",
          f"node render.mjs ffmpeg $D && bash finish.sh ffmpeg $D {1.2 if vid == 'V09' else 2.9}   # poster = the hook frame" if mixer else
          "node render.mjs ffmpeg $D && bash finish.sh ffmpeg $D $(python3 -c \"print(round($D-0.5,2))\")",
          f'( cd ../../thumbs-work && node make_thumbs.mjs {repo_dir} )   # thumbnail',
          '( cd "/Users/ravikumar/Cheeko Master/marketing/tools" && ../../cheeko-v2-website/.venv/bin/python publish_to_drive.py )', "```", "",
          "## Assets used", ""] + [f"- `assets/img/{a}`" for a in assets] + [""]
    if hindi:
        L += ["## Hindi notes", "", "Captions and fixed text come from `make_hindi.py`. The device screens stay as the firmware draws them: the firmware has no Devanagari font, so Hindi text on the device shows blank (see `fw-screens/*_hi_*`).", ""]
    return "\n".join(L)


def _ready_to_post(rows):
    """Ready to post/English and /Hindi: one folder per video holding only its video, thumbnail and caption.
    Standalone videos go in the main Ready to post; a series keeps its own inside its folder."""
    for root in [DRIVE] + [DRIVE / n for n in SERIES]:
        for lang in ("English", "Hindi"):
            d = root / "Ready to post" / lang
            if root == DRIVE: d.mkdir(parents=True, exist_ok=True)
            if d.exists():
                for f in d.iterdir():                 # these folders are fully managed by the script
                    shutil.rmtree(f) if f.is_dir() else f.unlink()
    for vid, title, fmt, secs, status, voice, stem in rows:
        if status == "Rejected": continue
        lang = "Hindi" if vid.endswith("-HI") else "English"
        name = f"{vid} {title}"; root = _root_for(vid)
        out = root / "Ready to post" / lang / name; out.mkdir(parents=True, exist_ok=True)
        final = root / name / "4 Final"
        for suffix, label in ((".mp4", "video.mp4"), ("_thumbnail.jpg", "thumbnail.jpg"), ("_caption.txt", "caption.txt")):
            if (final / f"{stem}{suffix}").exists():
                shutil.copy2(final / f"{stem}{suffix}", out / f"{name} - {label}")
        s16 = stem.replace("_9x16_", "_16x9_")
        for suffix, label in ((".mp4", "video 16x9 (YouTube).mp4"), ("_thumbnail.jpg", "thumbnail 16x9 (YouTube).jpg"), ("_youtube_chapters.txt", "YouTube chapters.txt")):
            if (final / f"{s16}{suffix}").exists():
                shutil.copy2(final / f"{s16}{suffix}", out / f"{name} - {label}")


PUBLIC = DRIVE / "Public videos"


def _public_videos(rows):
    """Public videos/English|Hindi: only the final video files (vertical, plus 16:9 where made), named "<ID> <title>.mp4".
    This is the ONLY folder shared as "Anyone with the link: Viewer" (Ravi, 2026-09-29); the public website plays from it.
    Files are overwritten in place, never deleted and re-made, so their Drive links stay the same across publishes."""
    want = {}
    for vid, title, fmt, secs, status, voice, stem in rows:
        if status == "Rejected": continue
        final = _root_for(vid) / f"{vid} {title}" / "4 Final"; lang = "Hindi" if vid.endswith("-HI") else "English"
        for st, label in ((stem, ""), (stem.replace("_9x16_", "_16x9_"), " (16x9)")):
            if (final / f"{st}.mp4").exists(): want[PUBLIC / lang / f"{vid} {title}{label}.mp4"] = final / f"{st}.mp4"
    for dst, src in want.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() or dst.stat().st_size != src.stat().st_size or int(dst.stat().st_mtime) != int(src.stat().st_mtime):
            shutil.copy2(src, dst)
    for lang in ("English", "Hindi"):
        for f in (PUBLIC / lang).glob("*.mp4") if (PUBLIC / lang).exists() else []:
            if f not in want: f.unlink()   # a video that is no longer published
    (PUBLIC / "README.txt").write_text("Only the final Cheeko videos. This folder is public (anyone with the link can view); nothing else in \"cheeko ai videos\" is.\n"
                                       "The public video library plays from here: https://craftech360-projects.github.io/cheeko-video-library/\n"
                                       "Built by marketing/tools/publish_to_drive.py; don't add other files here.\n")


def _series_extras(rows):
    """Each series folder: README (parts, status, how to iterate), its plan, and the template code it is built with."""
    for name, sr in SERIES.items():
        root = DRIVE / name; root.mkdir(exist_ok=True)
        pd = root / "00 Plan and scripts"; pd.mkdir(exist_ok=True)
        shutil.copy2(MKT / sr["plan"], pd / sr["plan_name"])
        code = pd / "Series code"; code.mkdir(exist_ok=True)
        shutil.copytree(Path(__file__).parent / "feature", code / "feature template", dirs_exist_ok=True)
        for f in ("build_feature.py", "feature_lines.json", "feature_lines_hi.json"):
            shutil.copy2(Path(__file__).with_name(f), code / f)
        shutil.copy2(REPO / "thumbs-work/make_thumbs_feature.mjs", code / "make_thumbs_feature.mjs")
        mine = [r for r in rows if r[0].replace("-HI", "") in sr["ids"]]
        intro = {"Onboarding Cheeko": "The intro and onboarding series. Each part works alone as a Reel; at the end all parts are re-rendered together\nwith the same calm music and stitched into one film (V24, vertical and 16:9).",
                 "Cheeko App Guide": "A detailed walkthrough of the parent app, tab by tab, on an iPhone with the real app screens. Each part works alone as a Reel;\nat the end all parts are re-rendered together and stitched into one film (V25)."}.get(name, "")
        L = [f"# {name}", "", intro, "",
             "| Part | ID | Language | Name | Length | Status |", "|---|---|---|---|---|---|"]
        n = 0
        for vid, title, fmt, secs, status, voice, stem in sorted(mine, key=lambda r: (r[0].endswith("-HI"), r[2] == "Film", r[0])):
            base = vid.replace("-HI", "")
            if fmt == "Film": part = "Full film"
            elif "." in base: part = base.split(".")[1]
            else: n += 0 if vid.endswith("-HI") else 1; part = str(sr["ids"].index(base) + 1)
            L.append(f"| {part} | {vid} | {'Hindi' if vid.endswith('-HI') else 'English'} | {title} | {secs}s | {status} |")
        L += ["", "## What is where", "",
              "- `00 Plan and scripts/`: the plan with every line and shot, and the code these parts are built with.",
              "- `V2x <name>/`: 1 Script, 2 Voice (one clip per line), 3 Test (frame sheet), 4 Final, 5 Source.",
              "  `5 Source` has the composition, spec.js (the shot list), timings, music cues and `assets used (assets-img)/`:",
              "  every firmware screen, app screen, card and photo that part shows, so it can be re-rendered from here.",
              "- `Ready to post/`: only the video, thumbnail and caption per part (drafts until the final pass).", "",
              "## Iterating on a part", "",
              "The working copy is in the website repo: `cheeko-v2-website/brag-output-2026-09-29-<slug>/work/`.",
              "Edit `spec.js`, then run `marketing/tools/feature/setup.sh <dir>`, `node cues.mjs`, `python synth.py`,",
              "`node render.mjs ffmpeg <secs>` and `bash finish.sh ffmpeg <secs> <poster>`, then `publish_to_drive.py`.",
              "New voice lines: edit `feature_lines.json`, record on the dev box, run `build_feature.py`. Full steps: `00 Plan/HOW WE MAKE CHEEKO VIDEOS.md` in the main folder.", ""]
        (root / "README.md").write_text("\n".join(L))
        for old in (DRIVE / "00 Plan" / "V20-V24 Getting Started series - plan and scripts.md",
                    DRIVE / "00 Plan" / "V25 Cheeko App Walkthrough - plan and script.md"):
            if old.exists(): old.unlink()       # moved into the series folder


def _pipeline_code(plan):
    """00 Plan/Pipeline code: every script and config the videos are built with, for the next AI or person."""
    pc = plan / "Pipeline code"
    shutil.copy2(Path(__file__).with_name("HOW-WE-MAKE-VIDEOS.md"), plan / "HOW WE MAKE CHEEKO VIDEOS.md")
    (pc / "marketing-tools").mkdir(parents=True, exist_ok=True)
    for f in Path(__file__).parent.iterdir():
        if f.is_file() and f.suffix in (".py", ".json", ".md"): shutil.copy2(f, pc / "marketing-tools" / f.name)
    fw = Path(__file__).parent / "fwsim"
    if fw.exists(): shutil.copytree(fw, pc / "fwsim (firmware screen renderer)", dirs_exist_ok=True, symlinks=True, ignore=shutil.ignore_patterns("src", "build", "deps", "gen", "out", "sdcard"))   # tool only; render.sh rebuilds the rest
    tw = REPO / "thumbs-work"
    (pc / "thumbnails").mkdir(exist_ok=True)
    for f in ("thumb.html", "make_thumbs.mjs"):
        if (tw / f).exists(): shutil.copy2(tw / f, pc / "thumbnails" / f)
    sk = REPO / ".claude/skills"
    for name in ("cheeko-video", "brag-slim"):
        if (sk / name).exists(): shutil.copytree(sk / name, pc / f"skill {name}", dirs_exist_ok=True)


def main():
    only = set(sys.argv[1:])
    DRIVE.mkdir(exist_ok=True)
    rows = []
    for v in VIDEOS:
        if not only or v[0] in only:
            rows.append(build(v, _root_for(v[0])))
            print("built", v[0], v[1])
    if not only or "X01" in only:
        build(ARCHIVE, DRIVE / "X Archive")
        print("built archive")

    plan = DRIVE / "00 Plan"; plan.mkdir(exist_ok=True)
    shutil.copy2(MKT / "cheeko-video-ideas.md", plan / "Cheeko video ideas (all 28).md")
    shutil.copy2(Path(__file__).with_name("production-rules.md"), plan / "Production rules.md")
    if not only:
        lines = ["# Cheeko video tracker", "", "Every video has the same five stages: 1 Script, 2 Voice, 3 Test, 4 Final, 5 Source.", "",
                 "| ID | Name | Format | Length | Status | Voice | Final file |", "|---|---|---|---|---|---|---|"]
        for vid, title, fmt, secs, status, voice, stem in rows:
            where = _root_for(vid).name if _root_for(vid) != DRIVE else ""
            lines.append(f"| {vid} | {title}{' (in ' + where + ')' if where else ''} | {fmt} | {secs}s | {status} | {voice} | {stem}.mp4 |")
        lines += ["", "Archive: X01 Manifesto (rejected), too slow for Reels, kept for reference."]
        (plan / "Video tracker.md").write_text("\n".join(lines) + "\n")

    if not only:
        _ready_to_post(rows)
        _pipeline_code(plan)
    if not only: _public_videos(rows)
    _series_extras(rows)
    if not only:   # the team's master sheet with every video and its links (master_sheet.py)
        import master_sheet; master_sheet.build()

    assets = DRIVE / "01 Shared assets/Shipping cards"; assets.mkdir(parents=True, exist_ok=True)
    for f in sorted((MKT / "cards-shipping/originals").glob("*.png")):
        shutil.copy2(f, assets / f.name)
    shutil.copy2(MKT / "cards-shipping/README.md", assets / "README.md")
    shutil.copy2(REPO / "assets/img/device_live_screen_mask.png", DRIVE / "01 Shared assets/device screen mask.png")


if __name__ == "__main__":
    main()
