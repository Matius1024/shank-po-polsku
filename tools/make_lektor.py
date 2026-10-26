"""Nagrywa polskie glosy: jeden plik WAV na kwestie (lektor/<wersja>/<film>_<nr>.wav), glosami neuronowymi Microsoft Edge.

Kwestie postaci (kind "d") czyta lektor, opisy obrazu (kind "ad") drugi glos: audiodeskrypcja.
Uzycie: python make_lektor.py [wersja]   (domyslnie classic; wersja = podfolder w napisy/)
"""
import asyncio
import glob
import json
import os
import subprocess
import sys

import edge_tts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = sys.argv[1] if len(sys.argv) > 1 else "classic"
VOICES = {"d": ("pl-PL-MarekNeural", "+15%"), "ad": ("pl-PL-ZofiaNeural", "+20%")}


async def main():
    out_dir = os.path.join(ROOT, "lektor", VERSION)
    os.makedirs(out_dir, exist_ok=True)
    for path in sorted(glob.glob(os.path.join(ROOT, "napisy", VERSION, "*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        for i, line in enumerate(d["lines"]):
            text = line.get("pl", "").strip()
            wav = os.path.join(out_dir, f"{d['movie']}_{i:03d}.wav")
            if not text or os.path.exists(wav):
                continue
            voice, rate = VOICES[line.get("kind", "d")]
            mp3 = wav[:-4] + ".mp3"
            await edge_tts.Communicate(text, voice, rate=rate).save(mp3)
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", mp3,
                            "-ar", "44100", "-ac", "2", wav], check=True)
            os.remove(mp3)
            print(os.path.basename(wav), text, flush=True)


asyncio.run(main())
