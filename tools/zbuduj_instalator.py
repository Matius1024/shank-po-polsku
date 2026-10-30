"""Buduje instalator Windows programu Shank po polsku (dist\\ShankPoPolsku-<wersja>-instalator.exe).

1. PyInstaller pakuje tools\\shank_polski.py do "Shank po polsku.exe" (bez Pythona u gracza).
2. Folder pakietu: program, napisy (classic, zwykla), nagrania lektora zmniejszone do 24 kHz mono
   (syntezator i tak mowi w 24 kHz), rozmiary_classic.json, domyslne ustawienia, CZYTAJ_MNIE.txt.
3. Inno Setup (ISCC) robi z pakietu jeden plik instalatora.

Uzycie: D:\\ShankPolski-audio\\buildenv\\Scripts\\python.exe tools\\zbuduj_instalator.py [wersja]
"""
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WORK = r"D:\ShankPolski-audio\budowa"
PAKIET = r"D:\ShankPolski-audio\pakiet"
PAKIET_LEKTOR = r"D:\ShankPolski-audio\pakiet_lektor"
PAKIET_AD = r"D:\ShankPolski-audio\pakiet_ad"
ISCC = os.path.join(os.environ["LOCALAPPDATA"], r"Programs\Inno Setup 6\ISCC.exe")
NAME = "Shank po polsku"
VERSIONS = ["classic", "zwykla"]


def run(cmd):
    subprocess.run(cmd, check=True)


def build_exe():
    run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onedir", "--noconsole",
         "--name", NAME, "--collect-all", "accessible_output2", "--hidden-import", "pycaw.pycaw",
         "--distpath", os.path.join(WORK, "dist"), "--workpath", os.path.join(WORK, "build"),
         "--specpath", WORK, os.path.join(HERE, "shank_polski.py")])
    return os.path.join(WORK, "dist", NAME)


def shrink(src, dst):
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", dst])


def is_description(version, wav):
    """Czy nagranie <film>_<nr>.wav to audiodeskrypcja (pole kind kwestii nr w napisach filmu)."""
    movie, nr = wav[:-4].rsplit("_", 1)
    with open(os.path.join(ROOT, "napisy", version, movie + ".json"), encoding="utf-8") as f:
        return json.load(f)["lines"][int(nr)].get("kind", "d") == "ad"


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else "1.0"
    exe_dir = build_exe()
    if os.path.exists(PAKIET):
        shutil.rmtree(PAKIET)
    shutil.copytree(exe_dir, PAKIET)
    # Nagrania osobno, bo instalator kopiuje tylko to, co wybral gracz (lektor, audiodeskrypcja).
    for folder in (PAKIET_LEKTOR, PAKIET_AD):
        if os.path.exists(folder):
            shutil.rmtree(folder)
    jobs = []
    for v in VERSIONS:
        shutil.copytree(os.path.join(ROOT, "napisy", v), os.path.join(PAKIET, "napisy", v))
        src = os.path.join(ROOT, "lektor", v)
        for folder in (PAKIET_LEKTOR, PAKIET_AD):
            os.makedirs(os.path.join(folder, "lektor", v))
        for f in os.listdir(src):
            if f.endswith(".wav"):
                folder = PAKIET_AD if is_description(v, f) else PAKIET_LEKTOR
                jobs.append((os.path.join(src, f), os.path.join(folder, "lektor", v, f)))
    with ThreadPoolExecutor(os.cpu_count()) as pool:
        list(pool.map(lambda j: shrink(*j), jobs))
    print(f"{len(jobs)} nagran")
    shutil.copy(os.path.join(ROOT, "rozmiary_classic.json"), PAKIET)
    for f in ("shank_polski.ini", "CZYTAJ_MNIE.txt"):
        shutil.copy(os.path.join(ROOT, "instalator", f), PAKIET)
    # Inno Setup czyta polskie litery w skrypcie tylko z plikow UTF-8 z BOM.
    iss = os.path.join(ROOT, "instalator", "shank_po_polsku.iss")
    with open(iss, encoding="utf-8-sig") as f:
        text = f.read()
    with open(iss, "w", encoding="utf-8-sig") as f:
        f.write(text)
    run([ISCC, f"/DPAKIET={PAKIET}", f"/DPAKIET_LEKTOR={PAKIET_LEKTOR}", f"/DPAKIET_AD={PAKIET_AD}",
         f"/DWersja={version}", iss])


if __name__ == "__main__":
    main()
