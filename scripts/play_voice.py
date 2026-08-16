#!/usr/bin/env python3
"""Play Azuma (吾妻) bundled voice-line MP3s.

The skill's assets/ folder may contain voice clips named after their in-game
trigger, e.g. 好感度失望.mp3. This script lists, verifies, and plays them.

Usage:
    python scripts/play_voice.py                  # list all bundled voices
    python scripts/play_voice.py 好感度陌生        # play one voice (exact or fuzzy name)
    python scripts/play_voice.py --check          # verify MP3 files without playing
    python scripts/play_voice.py --all            # play every bundled voice in order
"""

import argparse
import ctypes
import pathlib
import shutil
import subprocess
import sys
import tempfile

ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets"
ALIAS = "azuma_voice"

# Known voice clips bundled in this skill and their in-game text (from references/lines.md).
KNOWN_LINES = {
    "好感度失望.mp3": "指挥官，我很担心你的近况……不要再这样下去了，好吗？",
    "好感度陌生.mp3": "我对这里还不是太熟悉……能耽误指挥官一点时间，稍微陪我在港区里走走吗？",
}


def list_voices(assets_dir=ASSETS_DIR):
    return sorted(assets_dir.glob("*.mp3"))


def is_mp3(path):
    try:
        head = path.read_bytes()[:3]
    except OSError:
        return False
    return head == b"ID3" or head[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")


def print_voice(path):
    line = KNOWN_LINES.get(path.name, "")
    suffix = f"  —— {line}" if line else ""
    print(f"{path.name}{suffix}")


def check_voices(voices):
    bad = [v for v in voices if not is_mp3(v)]
    for v in voices:
        status = "OK" if v not in bad else "BAD"
        print(f"[{status}] {v.name}")
    return 0 if not bad else 1


def play_windows(path):
    mci = ctypes.windll.winmm.mciSendStringW

    def send(cmd):
        code = mci(cmd, None, 0, 0)
        if code != 0:
            raise RuntimeError(f"MCI error {code} for: {cmd}")

    # MCI on some Windows builds fails on non-ASCII paths, so play from a
    # temporary copy with an ASCII name and clean it up afterwards. Let MCI
    # auto-detect the device from the .mp3 extension (no explicit type).
    temp_path = pathlib.Path(tempfile.gettempdir()) / "azuma_voice_tmp.mp3"
    shutil.copyfile(path, temp_path)
    try:
        send(f'open "{temp_path}" alias {ALIAS}')
        try:
            send(f"play {ALIAS} wait")
        finally:
            send(f"close {ALIAS}")
    finally:
        temp_path.unlink(missing_ok=True)


def play_voice(path):
    if not path.exists():
        print(f"[ERROR] Voice file not found: {path}", file=sys.stderr)
        return 1
    if not is_mp3(path):
        print(f"[ERROR] Not a valid MP3 file: {path}", file=sys.stderr)
        return 1
    print(f"[PLAY] {path.name}")
    line = KNOWN_LINES.get(path.name)
    if line:
        print(f"        {line}")

    if sys.platform.startswith("win"):
        play_windows(path)
    elif sys.platform == "darwin":
        subprocess.run(["afplay", str(path)], check=True)
    else:
        for player in ("paplay", "aplay", "ffplay"):
            try:
                subprocess.run([player, str(path)], check=True)
                return 0
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue
        print("[ERROR] No audio player found. Install paplay/aplay/ffplay.", file=sys.stderr)
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description="Play Azuma voice lines bundled in this skill.")
    parser.add_argument("query", nargs="?", help="Voice file name (exact or part of the name).")
    parser.add_argument("--all", action="store_true", help="Play every bundled voice in order.")
    parser.add_argument("--check", action="store_true", help="Verify MP3 files without playing.")
    parser.add_argument("--assets", default=str(ASSETS_DIR), help="Override the assets directory.")
    args = parser.parse_args()

    assets_dir = pathlib.Path(args.assets)
    voices = list_voices(assets_dir)
    if not voices:
        print(f"[ERROR] No MP3 files found under {assets_dir}", file=sys.stderr)
        return 1

    if args.check:
        return check_voices(voices)

    if args.all:
        for voice in voices:
            print_voice(voice)
            play_voice(voice)
        return 0

    if args.query:
        exact = assets_dir / args.query
        candidates = [v for v in voices if v.name == args.query or args.query in v.name]
        if exact.exists():
            candidates = [exact]
        if not candidates:
            print(f"[ERROR] No voice matches '{args.query}'. Available voices:", file=sys.stderr)
            for voice in voices:
                print_voice(voice)
            return 1
        if len(candidates) > 1:
            print("[WARN] Multiple matches, choose one:")
            for voice in candidates:
                print_voice(voice)
            return 1
        return play_voice(candidates[0])

    print(f"Bundled voices ({len(voices)}):")
    for voice in voices:
        print_voice(voice)
    return 0


if __name__ == "__main__":
    sys.exit(main())
