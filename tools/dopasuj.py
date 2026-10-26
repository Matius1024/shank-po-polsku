"""Dopasowuje nagrania do czasu filmu. Zrodla: lektor/<wersja>_surowe, wynik: lektor/<wersja>.

Lektor (kind "d") zawsze w zwyklym tempie: moze sie spozniac i nachodzic na glos postaci, tak jak w telewizji.
Audiodeskrypcja (kind "ad") musi sie zmiescic w ciszy: zaczyna sie, gdy lektor skonczy, i konczy przed
nastepna kwestia. Za dluga jest przyspieszana (najwyzej MAX razy); jesli i tak sie nie miesci, dostaje
"skip": true w napisy/<wersja>/<film>.json (program jej nie czyta) i trafia na liste do skrocenia.

Uzycie: python dopasuj.py <plik z dlugosciami filmow> [wersja]
"""
import glob
import json
import os
import subprocess
import sys
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX = 1.35
MARGIN = 0.2  # cisza miedzy koncem opisu a nastepna kwestia


def length(path):
    with wave.open(path) as f:
        return f.getnframes() / f.getframerate()


TRIM = ("silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
        "silenceremove=start_periods=1:start_threshold=-45dB,areverse")


def trimmed(src, cache):
    """Nagranie bez ciszy na poczatku i koncu (syntezator dodaje pauzy); zapisane obok, w <wersja>_ciete."""
    out = os.path.join(cache, os.path.basename(src))
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-af", TRIM, out], check=True)
    return out


def copy(src, dst, tempo):
    if tempo > 1.01:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src,
                        "-filter:a", f"atempo={tempo:.3f}", dst], check=True)
    else:
        with open(src, "rb") as a, open(dst, "wb") as b:
            b.write(a.read())


def main():
    durations = {l.split()[0]: float(l.split()[1]) for l in open(sys.argv[1])}
    version = sys.argv[2] if len(sys.argv) > 2 else "classic"
    src, dst = os.path.join(ROOT, "lektor", version + "_surowe"), os.path.join(ROOT, "lektor", version)
    cache = os.path.join(ROOT, "lektor", version + "_ciete")
    os.makedirs(dst, exist_ok=True)
    os.makedirs(cache, exist_ok=True)
    for path in sorted(glob.glob(os.path.join(ROOT, "napisy", version, "*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        movie, lines = d["movie"], d["lines"]
        t = 0.0
        for i, line in enumerate(lines):
            name = f"{movie}_{i:03d}.wav"
            raw = trimmed(os.path.join(src, name), cache)
            n = length(raw)
            begin = max(t, line["start"])
            line.pop("skip", None)
            if line["kind"] == "d":
                copy(raw, os.path.join(dst, name), 1.0)
                t = begin + n
                continue
            limit = next((l["start"] for l in lines[i + 1:] if l["kind"] == "d"), durations.get(movie, 1e9))
            room = limit - MARGIN - begin
            if n / MAX > room:
                line["skip"] = True
                print(f"{movie} #{i} opis sie nie miesci ({n:.1f}s, miejsca {max(room, 0):.1f}s od {begin:.1f}s): {line['pl']}")
                continue
            tempo = max(1.0, n / room)
            copy(raw, os.path.join(dst, name), tempo)
            t = begin + n / tempo
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
