"""Shank po polsku: polski lektor i audiodeskrypcja do scenek z gry Shank.

Program dziala obok gry i nie potrzebuje zadnego moda. Co chwile sprawdza, ktore pliki ma otwarte Shank.exe:
gra otwiera plik filmu (data\\movies\\<film>.usm) na poczatku scenki i zamyka go na koncu.
Na poczatku kazdej kwestii odtwarza nagranie lektora (albo mowi tlumaczenie przez czytnik ekranu),
w przerwach miedzy kwestiami drugi glos czyta audiodeskrypcje (opis tego, co widac).
Wersja filmu: plik o rozmiarze z rozmiary_classic.json to wersja z galezi "classic" na Steam (napisy/classic,
lektor/classic), tak samo filmy z listy "wspolne" (ten sam dzwiek w obu wersjach); inne to zwykla wersja gry
(napisy/zwykla, lektor/zwykla: sam lektor, bez audiodeskrypcji).

Uzycie: pythonw shank_polski.py [--w-tle]   (ustawienia w shank_polski.ini; po spakowaniu: Shank po polsku.exe)
"""
import configparser
import ctypes
import json
import os
import sys
import threading
import time
import winsound

import psutil

if getattr(sys, "frozen", False):  # spakowany program (PyInstaller): dane obok pliku exe
    ROOT = os.path.dirname(sys.executable)
else:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "shank_polski.log")
POLL = 0.1  # co ile sekund sprawdzamy pliki gry


def log(msg):
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%H:%M:%S ") + msg + "\n")
    except OSError:
        pass


def load_config():
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join(ROOT, "shank_polski.ini"), encoding="utf-8-sig")
    s = cfg["ustawienia"] if cfg.has_section("ustawienia") else {}
    return {
        "game": s.get("folder_gry", "").strip(),
        "mode": s.get("tryb", "lektor").strip().lower(),
        "start_game": s.get("uruchom_gre", "1").strip() == "1",
        "duck": int(s.get("glosnosc_gry_pod_lektorem", "35")) / 100,
        "ad": s.get("audiodeskrypcja", "1").strip() == "1",
    }


def load_classic():
    """(rozmiary plikow filmow wersji classic, filmy wspolne obu wersji)"""
    try:
        with open(os.path.join(ROOT, "rozmiary_classic.json"), encoding="utf-8") as f:
            d = json.load(f)
        return d["rozmiary"], set(d["wspolne"])
    except (OSError, ValueError, KeyError):
        return {}, set()


class Speaker:
    def __init__(self):
        try:
            from accessible_output2.outputs.auto import Auto
            self.out = Auto()
        except Exception as e:
            log(f"czytnik ekranu: blad {e}")
            self.out = None

    def say(self, text, interrupt=False):
        if self.out is None:
            return
        try:
            self.out.speak(text, interrupt=interrupt)
        except Exception as e:
            log(f"mowa: blad {e}")


class Player:
    """Odtwarza kwestie jednego filmu w osobnym watku; stop() przerywa."""

    def __init__(self, speaker, mode, duck, ad):
        self.speaker, self.mode, self.duck, self.ad = speaker, mode, duck, ad
        self.cancel = threading.Event()
        self.thread = None

    def play(self, movie, version, started):
        self.stop()
        path = os.path.join(ROOT, "napisy", version, movie + ".json")
        if not os.path.exists(path):
            log(f"film {movie} ({version}): brak napisow")
            return
        with open(path, encoding="utf-8") as f:
            lines = json.load(f)["lines"]
        if not self.ad:
            lines = [l if l.get("kind", "d") == "d" else dict(l, pl="") for l in lines]
        self.cancel = threading.Event()
        self.thread = threading.Thread(target=self._run, args=(movie, version, lines, started, self.cancel),
                                       daemon=True)
        self.thread.start()

    def _run(self, movie, version, lines, started, cancel):
        log(f"film {movie} ({version}): {len(lines)} kwestii, tryb {self.mode}")
        for i, line in enumerate(lines):
            text = line.get("pl", "").strip()
            if not text or line.get("skip"):  # opis, ktory nie miesci sie miedzy kwestiami (tools/dopasuj.py)
                continue
            delay = started + line["start"] - time.monotonic()
            if delay > 0 and cancel.wait(delay):
                return
            if delay < -2 and time.monotonic() - started < 1:  # program wystartowal w srodku filmu
                continue
            # Spoznione kwestie i opisy czytamy zawsze w calosci (gracz: opis nie moze znikac).
            wav = os.path.join(ROOT, "lektor", version, f"{movie}_{i:03d}.wav")
            if self.mode == "lektor" and os.path.exists(wav):
                set_game_volume(self.duck)  # jak lektor w telewizji: oryginal ciszej pod polskim glosem
                winsound.PlaySound(wav, winsound.SND_FILENAME | winsound.SND_NODEFAULT)
                set_game_volume(1.0)
            else:
                self.speaker.say(text)

    def stop(self):
        self.cancel.set()
        winsound.PlaySound(None, winsound.SND_PURGE)
        set_game_volume(1.0)


def set_game_volume(level):
    """Glosnosc dzwieku gry Shank.exe w mikserze Windows (0.0 - 1.0)."""
    try:
        from pycaw.pycaw import AudioUtilities
        import comtypes
        comtypes.CoInitialize()
        for s in AudioUtilities.GetAllSessions():
            if s.Process and s.Process.name().lower() == "shank.exe":
                s.SimpleAudioVolume.SetMasterVolume(level, None)
    except Exception as e:
        log(f"glosnosc gry: blad {e}")


def find_game():
    for p in psutil.process_iter(["name"]):
        if (p.info["name"] or "").lower() == "shank.exe":
            return p
    return None


def steam_exe():
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as k:
            exe = winreg.QueryValueEx(k, "SteamExe")[0]
        return exe if os.path.exists(exe) else None
    except OSError:
        return None


def start_game(cfg):
    """Gra ze Steam przez Steam; inna kopia (np. GOG) z folder_gry w ustawieniach."""
    exe = os.path.join(cfg["game"], "Shank.exe") if cfg["game"] else ""
    if exe and os.path.exists(exe):
        os.startfile(exe)
    elif steam_exe():
        os.startfile("steam://rungameid/6120")
    else:
        log("nie wiem, jak uruchomic gre: wpisz folder_gry w shank_polski.ini")


def main():
    cfg = load_config()
    speaker = Speaker()
    # Jedna kopia programu naraz: druga (np. z pliku na Pulpicie) tylko uruchamia gre.
    ctypes.windll.kernel32.CreateMutexW(None, False, "ShankPoPolsku")
    first = ctypes.windll.kernel32.GetLastError() != 183  # ERROR_ALREADY_EXISTS
    if cfg["start_game"] and "--w-tle" not in sys.argv and find_game() is None:
        start_game(cfg)
    if not first:
        return
    log("start, czekam na gre")
    classic = load_classic()
    while True:
        game = find_game()
        if game is None:
            time.sleep(3)
            continue
        cfg = load_config()  # zmiany w shank_polski.ini dzialaja od nastepnego uruchomienia gry
        if cfg["mode"] in ("wylaczone", "wyłączone"):
            while game.is_running():
                time.sleep(3)
            continue
        log(f"gra uruchomiona, tryb {cfg['mode']}, audiodeskrypcja {int(cfg['ad'])}")
        speaker.say("Polski " + ("lektor" if cfg["mode"] == "lektor" else "tekst") +
                    (" i audiodeskrypcja" if cfg["ad"] else "") + " włączone.")
        player = Player(speaker, cfg["mode"], cfg["duck"], cfg["ad"])
        watch(game, player, classic)
        log("gra zamknieta")
        player.stop()


def open_movies(game):
    """Pliki filmow (.usm), ktore gra ma teraz otwarte; None, gdy gra sie zamknela."""
    try:
        return {f.path for f in game.open_files() if f.path.lower().endswith(".usm")}
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None if not game.is_running() else set()


def watch(game, player, classic):
    """Sledzi otwieranie i zamykanie plikow filmow, dopoki gra dziala."""
    playing = set(open_movies(game) or ())  # film juz trwajacy przy starcie programu pomijamy
    while True:
        before = time.monotonic()
        now = open_movies(game)
        if now is None:
            return
        if playing - now:
            player.stop()
        for path in now - playing:
            movie = os.path.splitext(os.path.basename(path))[0].lower()
            try:
                size = os.path.getsize(path)
            except OSError:
                size = -1
            sizes, shared = classic
            version = "classic" if sizes.get(movie) == size or movie in shared else "zwykla"
            # Plik otwarto gdzies miedzy poprzednim a tym sprawdzeniem: srodek tego okna.
            player.play(movie, version, before - POLL / 2)
        playing = now
        time.sleep(POLL)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"blad: {e!r}")
        raise
