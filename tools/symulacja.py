"""Sprawdza gotowe nagrania i symuluje odtwarzanie jak shank_polski.py.

Zglasza: brakujace nagrania, opisy (ad) nachodzace na nastepna kwestie, opisy pomijane w grze (spoznione > 1 s)
i ile spoznia sie lektor. Uzycie: python symulacja.py <plik z dlugosciami filmow> [wersja]
"""
import glob
import json
import os
import sys
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def length(path):
    with wave.open(path) as f:
        return f.getnframes() / f.getframerate()


def main():
    durations = {l.split()[0]: float(l.split()[1]) for l in open(sys.argv[1])}
    version = sys.argv[2] if len(sys.argv) > 2 else "classic"
    missing = overlaps = dropped = skipped = total = 0
    worst = []
    for path in sorted(glob.glob(os.path.join(ROOT, "napisy", version, "*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        movie, lines = d["movie"], d["lines"]
        t = 0.0
        for i, line in enumerate(lines):
            if line.get("skip"):
                skipped += 1
                continue
            total += 1
            wav = os.path.join(ROOT, "lektor", version, f"{movie}_{i:03d}.wav")
            if not os.path.exists(wav):
                missing += 1
                print(f"BRAK nagrania: {movie} #{i}")
                continue
            n = length(wav)
            late = t - line["start"]
            if line["kind"] == "ad":
                if late > 1:
                    dropped += 1
                    print(f"opis spozniony: {movie} #{i} ({late:.1f}s)")
                end = max(t, line["start"]) + n
                nxt = next((l["start"] for l in lines[i + 1:] if l["kind"] == "d"), durations.get(movie, 1e9))
                if end > nxt + 0.05:
                    overlaps += 1
                    print(f"NAKLADANIE: {movie} #{i} opis konczy sie {end:.1f}s, kwestia od {nxt:.1f}s")
            elif late > 0.5:
                worst.append((late, movie, i))
            t = max(t, line["start"]) + n
    print(f"\nnagran do zagrania: {total}, brakujacych: {missing}, opisow pominietych przy dopasowaniu: {skipped}")
    print(f"opisy nachodzace na kwestie: {overlaps}, opisy spoznione ponad 1 s: {dropped}")
    worst.sort(reverse=True)
    print(f"kwestie lektora spoznione ponad 0,5 s: {len(worst)}; najwieksze:",
          ", ".join(f"{m} #{i} {l:.1f}s" for l, m, i in worst[:5]))


if __name__ == "__main__":
    main()
