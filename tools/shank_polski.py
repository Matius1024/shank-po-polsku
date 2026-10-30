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
import msvcrt
import os
import queue
import subprocess
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
        "dialogue": s.get("lektor", "1").strip() == "1",
        "enabled": s.get("wlaczony", "1").strip() == "1",
    }


def save_setting(name, value):
    """Zapisuje jedno ustawienie w shank_polski.ini, reszty pliku nie rusza."""
    path = os.path.join(ROOT, "shank_polski.ini")
    try:
        with open(path, encoding="utf-8-sig") as f:
            lines = f.read().splitlines()
        found = False
        for i, line in enumerate(lines):
            if line.startswith(name + "="):
                lines[i] = f"{name}={value}"
                found = True
        if not found:
            lines.append(f"{name}={value}")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except OSError as e:
        log(f"ustawienia: blad zapisu {e}")


def installed_parts(mode):
    """(czy sa nagrania lektora, czy sa nagrania opisow). Tryb napisy czyta czytnik ekranu, wiec ma wszystko."""
    if mode != "lektor":
        return True, True
    found = {"d": False, "ad": False}
    folder = os.path.join(ROOT, "napisy", "classic")
    for name in os.listdir(folder) if os.path.isdir(folder) else ():
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            lines = json.load(f)["lines"]
        for i, line in enumerate(lines):
            if os.path.exists(os.path.join(ROOT, "lektor", "classic", f"{name[:-5]}_{i:03d}.wav")):
                found[line.get("kind", "d")] = True
    return found["d"], found["ad"]


def load_classic():
    """(rozmiary plikow filmow wersji classic, filmy wspolne obu wersji)"""
    try:
        with open(os.path.join(ROOT, "rozmiary_classic.json"), encoding="utf-8") as f:
            d = json.load(f)
        return d["rozmiary"], set(d["wspolne"])
    except (OSError, ValueError, KeyError):
        return {}, set()


class Speaker:
    """Czytnik ekranu we wlasnym watku: mowi do niego kilka watkow, a obiekty COM dzialaja tylko w tym, ktory je utworzyl."""

    def __init__(self):
        self.queue = queue.Queue()
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        try:
            import comtypes
            comtypes.CoInitialize()
            from accessible_output2.outputs.auto import Auto
            out = Auto()
        except Exception as e:
            log(f"czytnik ekranu: blad {e}")
            out = None
        while True:
            text, interrupt = self.queue.get()
            if out is None:
                continue
            try:
                out.speak(text, interrupt=interrupt)
            except Exception as e:
                log(f"mowa: blad {e}")

    def say(self, text, interrupt=False):
        self.queue.put((text, interrupt))


class Player:
    """Odtwarza kwestie jednego filmu w osobnym watku; stop() przerywa."""

    def __init__(self, speaker, mode, duck, ad, dialogue, enabled):
        self.speaker, self.mode, self.duck = speaker, mode, duck
        self.ad, self.dialogue, self.enabled = ad, dialogue, enabled
        self.cancel = threading.Event()
        self.thread = None
        self.sounding = None  # rodzaj kwestii ("d", "ad"), ktorej nagranie teraz gra

    def wants(self, kind):
        return self.enabled and {"d": self.dialogue, "ad": self.ad}.get(kind, True)

    def settings_changed(self):
        """Po klawiszu: nagranie tego, co wlasnie wylaczono, urywa sie; reszta dziala od nastepnej kwestii."""
        if self.sounding and not self.wants(self.sounding):
            winsound.PlaySound(None, winsound.SND_PURGE)
            set_game_volume(1.0)

    def play(self, movie, version, started):
        self.stop()
        path = os.path.join(ROOT, "napisy", version, movie + ".json")
        if not os.path.exists(path):
            log(f"film {movie} ({version}): brak napisow")
            return
        with open(path, encoding="utf-8") as f:
            lines = json.load(f)["lines"]
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
            if cancel.wait(max(delay, 0)):
                return
            if delay < -2 and time.monotonic() - started < 1:  # program wystartowal w srodku filmu
                continue
            kind = line.get("kind", "d")
            if not self.wants(kind):  # sprawdzane w chwili kwestii: klawisze A i S dzialaja w trakcie filmu
                continue
            # Spoznione kwestie i opisy czytamy zawsze w calosci (gracz: opis nie moze znikac).
            wav = os.path.join(ROOT, "lektor", version, f"{movie}_{i:03d}.wav")
            if self.mode == "lektor" and os.path.exists(wav):
                set_game_volume(self.duck)  # jak lektor w telewizji: oryginal ciszej pod polskim glosem
                self.sounding = kind
                winsound.PlaySound(wav, winsound.SND_FILENAME | winsound.SND_NODEFAULT)
                self.sounding = None
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


KEY_MODE, KEY_POWER = ord("A"), ord("S")
# Z tymi klawiszami to nie nasz skrot (np. NVDA+A, NVDA+S): Shift, Ctrl, Alt, Caps Lock, Insert, Windows.
KEY_MODIFIERS = (0x10, 0x11, 0x12, 0x14, 0x2D, 0x5B, 0x5C)
PARTS = [(True, True, "Lektor i audiodeskrypcja."), (True, False, "Tylko lektor."),
         (False, True, "Tylko audiodeskrypcja.")]


def next_mode(player, speaker, has_dialogue, has_ad):
    """Klawisz A: nastepny tryb sposrod tych, ktorych nagrania sa zainstalowane."""
    if not player.enabled:
        speaker.say("Program jest wyłączony. Włącza go klawisz S.", interrupt=True)
        return
    modes = [m for m in PARTS if (has_dialogue or not m[0]) and (has_ad or not m[1])]
    if len(modes) < 2:
        speaker.say("Zainstalowano tylko " + ("lektora." if has_dialogue else "audiodeskrypcję."), interrupt=True)
        return
    now = next((i for i, m in enumerate(modes) if m[:2] == (player.dialogue, player.ad)), -1)
    player.dialogue, player.ad, text = modes[(now + 1) % len(modes)]
    save_setting("lektor", int(player.dialogue))
    save_setting("audiodeskrypcja", int(player.ad))
    log(f"klawisz A: lektor {int(player.dialogue)}, audiodeskrypcja {int(player.ad)}")
    player.settings_changed()
    speaker.say(text, interrupt=True)


def toggle_program(player, speaker):
    """Klawisz S: wlacza i wylacza cale czytanie; wlaczenie wraca do ostatniego trybu."""
    player.enabled = not player.enabled
    save_setting("wlaczony", int(player.enabled))
    log(f"klawisz S: wlaczony {int(player.enabled)}")
    player.settings_changed()
    name = "Polski lektor" if player.dialogue else "Polska audiodeskrypcja"
    state = ("włączony" if player.enabled else "wyłączony") if player.dialogue else \
        ("włączona" if player.enabled else "wyłączona")
    speaker.say(f"{name} {state}.", interrupt=True)


def key_process(pid):
    """Osobny proces (--klawisze <pid>): pisze "A" lub "S" po nacisnieciu klawisza, gdy gra jest aktywnym oknem.
    Osobny, bo sprawdzanie plikow gry wstrzymuje caly program na ponad 100 ms i krotkie nacisniecia by gubil.
    Tylko odczyt stanu: gra i inne programy dostaja te litery normalnie. (Skroty Windows do gry nie docieraja.)"""
    user32, kernel32 = ctypes.windll.user32, ctypes.windll.kernel32
    kernel32.GetStdHandle.restype = ctypes.c_void_p
    out = msvcrt.open_osfhandle(kernel32.GetStdHandle(-11), 0)
    was_down = set()
    while psutil.pid_exists(pid):
        time.sleep(0.02)
        owner = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), ctypes.byref(owner))
        if owner.value != pid:
            was_down.clear()
            continue
        down = {k for k in (KEY_MODE, KEY_POWER) if user32.GetAsyncKeyState(k) & 0x8000}
        if not any(user32.GetAsyncKeyState(k) & 0x8000 for k in KEY_MODIFIERS):
            for key in down - was_down:
                os.write(out, chr(key).encode() + b"\n")
        was_down = down


def start_keys(pid, player, speaker):
    """Uruchamia proces klawiszy i wykonuje to, co zglasza. Zwraca proces albo None."""
    args = [sys.executable] if getattr(sys, "frozen", False) else [sys.executable, os.path.abspath(__file__)]
    try:
        proc = subprocess.Popen(args + ["--klawisze", str(pid)], stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
    except OSError as e:
        log(f"klawisze: blad {e!r}")
        return None

    def read():
        has_dialogue, has_ad = installed_parts(player.mode)
        for line in proc.stdout:
            try:
                if line.strip() == b"A":
                    next_mode(player, speaker, has_dialogue, has_ad)
                elif line.strip() == b"S":
                    toggle_program(player, speaker)
            except Exception as e:
                log(f"klawisze: blad {e!r}")

    threading.Thread(target=read, daemon=True).start()
    return proc


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
    exes = [os.path.join(cfg["game"], "Shank.exe"), os.path.join(cfg["game"], "bin", "Shank.exe")] if cfg["game"] else []
    exe = next((e for e in exes if os.path.exists(e)), "")
    if exe:
        subprocess.Popen([exe], cwd=os.path.dirname(exe))
    elif steam_exe():
        os.startfile("steam://rungameid/6120")
    else:
        log("nie wiem, jak uruchomic gre: wpisz folder_gry w shank_polski.ini")


def main():
    if "--klawisze" in sys.argv:
        key_process(int(sys.argv[sys.argv.index("--klawisze") + 1]))
        return
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
        log(f"gra uruchomiona, tryb {cfg['mode']}, lektor {int(cfg['dialogue'])}, audiodeskrypcja {int(cfg['ad'])}, "
            f"wlaczony {int(cfg['enabled'])}")
        if not cfg["enabled"]:
            speaker.say("Polski lektor wyłączony. Włącza go klawisz S.")
        elif cfg["dialogue"]:
            speaker.say("Polski " + ("lektor" if cfg["mode"] == "lektor" else "tekst") +
                        (" i audiodeskrypcja" if cfg["ad"] else "") + " włączone.")
        elif cfg["ad"]:
            speaker.say("Polska audiodeskrypcja włączona.")
        player = Player(speaker, cfg["mode"], cfg["duck"], cfg["ad"], cfg["dialogue"], cfg["enabled"])
        keys = start_keys(game.pid, player, speaker)
        watch(game, player, classic)
        if keys:
            keys.terminate()
        log("gra zamknieta")
        player.stop()


def open_movies(game):
    """Pliki filmow (.usm), ktore gra ma teraz otwarte; None, gdy gra sie zamknela."""
    try:
        return {f.path for f in game.open_files() if f.path.lower().endswith(".usm")}
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None if not game.is_running() else set()


def after_movie(movie, version):
    """Kwestie grane w samej grze po filmie (napisy/<wersja>/po_<film>.json); te same dzwieki w obu wersjach."""
    for v in (version, "classic"):
        if os.path.exists(os.path.join(ROOT, "napisy", v, f"po_{movie}.json")):
            return v
    return None


def watch(game, player, classic):
    """Sledzi otwieranie i zamykanie plikow filmow, dopoki gra dziala."""
    playing = set(open_movies(game) or ())  # film juz trwajacy przy starcie programu pomijamy
    versions = {}
    current = None  # film, ktory teraz czyta lektor
    while True:
        before = time.monotonic()
        now = open_movies(game)
        if now is None:
            return
        for path in playing - now:
            movie, version = versions.pop(path, (None, None))
            # Gra zamyka poprzedni film chwile po otwarciu nastepnego (3c_02 -> spowiedz 3c_03):
            # zamkniecie starego filmu nie moze ucinac lektora nowego.
            if path != current:
                continue
            player.stop()
            current = None
            v = after_movie(movie, version) if movie else None
            if v and not now - playing:  # od konca filmu gra mowi dalej sama (np. spacer z Mello w 2b)
                player.play(f"po_{movie}", v, before - POLL / 2)
        for path in now - playing:
            movie = os.path.splitext(os.path.basename(path))[0].lower()
            try:
                size = os.path.getsize(path)
            except OSError:
                size = -1
            sizes, shared = classic
            version = "classic" if sizes.get(movie) == size or movie in shared else "zwykla"
            versions[path] = (movie, version)
            current = path
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
