"""Naprawia zapis Shanka po skokach do punktu kontrolnego (moda Shank Access).

Gra zapisuje ukończenie rozdziału ("complete_<trudność>_<poziom>_<rozdział>" = czas w ms)
tylko wtedy, gdy Shank sam dojdzie do jego końca. Skok do punktu kontrolnego to pomija,
a ekran wyboru poziomu blokuje wszystko od pierwszego nieukończonego rozdziału. Ten program
dopisuje czas każdemu rozdziałowi, który leży przed najdalszym ukończonym, a sam nie ma czasu.

Uruchamiać przy zamkniętej grze. Kopia zapisu trafia obok, z datą w nazwie.
"""
import glob
import os
import shutil
import struct
import sys
import time

# Story Mode z data/campaigns.lua, po kolei: (poziom, rozdział)
ROZDZIALY = [
    ("campaign_1a_wrestlingring", "Return Home"),
    ("campaign_1a_wrestlingring", "A Big Show"),
    ("campaign_1b_pretrain", "Other side of the Tracks"),
    ("campaign_1b_train", "Ride"),
    ("campaign_1b_train", "Gears and Grenades"),
    ("campaign_1c_meatpacking", "Meatpacking Plant"),
    ("campaign_1c_meatpacking", "The Butcher"),
    ("campaign_2a_brothel", "Red Lights"),
    ("campaign_2a_brothel", "A Good Fight"),
    ("campaign_2b_lovehotel", "On The Run"),
    ("campaign_2b_lovehotel", "Sweet Love"),
    ("campaign_2c_redlight", "Venom of the Vipers"),
    ("campaign_2c_redlight", "World of Warriors"),
    ("campaign_3c_church", "A Bad Confession"),
    ("campaign_3c_church", "Bombs and Bells"),
    ("campaign_3c_church", "Unjust Steward"),
    ("campaign_4a_winecellar", "The Underworld"),
    ("campaign_4a_winecellar", "Leap of Faith"),
    ("campaign_4c_thevilla", "Fertile Ground"),
    ("campaign_4c_thevilla", "The Final Fight"),
]
TRUDNOSCI = {2: "normalny", 3: "trudny"}
CZAS_ZASTEPCZY_MS = 15 * 60 * 1000
STEAM_USERDATA = r"C:\Program Files (x86)\Steam\userdata"


def sdbm(tekst):
    h = 0
    for c in tekst.lower().encode("latin-1"):
        h = (c + (h << 6) + (h << 16) - h) & 0xFFFFFFFF
    return h


def klucz(trudnosc, poziom, rozdzial):
    return sdbm("complete_%d_%s_%s" % (trudnosc, poziom, rozdzial))


def wczytaj(dane):
    if dane[:4] != b"V002":
        raise ValueError("nieznany format zapisu")
    n = struct.unpack_from("<I", dane, 4)[0]
    pary = {}
    o = 8
    for _ in range(n):
        k, v = struct.unpack_from("<II", dane, o)
        pary[k] = v
        o += 8
    return pary, dane[o:]


def zapisz(pary, reszta):
    wynik = b"V002" + struct.pack("<I", len(pary))
    for k in sorted(pary):
        wynik += struct.pack("<II", k, pary[k])
    return wynik + reszta


def napraw_plik(sciezka):
    with open(sciezka, "rb") as f:
        dane = f.read()
    pary, reszta = wczytaj(dane)
    dopisane = []
    for trudnosc, nazwa in TRUDNOSCI.items():
        klucze = [klucz(trudnosc, p, r) for p, r in ROZDZIALY]
        ukonczone = [i for i, k in enumerate(klucze) if pary.get(k, 0) > 0]
        if not ukonczone:
            continue
        for i in range(max(ukonczone)):
            if pary.get(klucze[i], 0) == 0:
                pary[klucze[i]] = CZAS_ZASTEPCZY_MS
                dopisane.append("%s (poziom trudności %s)" % (ROZDZIALY[i][1], nazwa))
    if not dopisane:
        print("%s: wszystko w porządku, nic do naprawy." % os.path.basename(sciezka))
        return
    kopia = sciezka + time.strftime(".kopia-%Y%m%d-%H%M%S")
    shutil.copy2(sciezka, kopia)
    with open(sciezka, "wb") as f:
        f.write(zapisz(pary, reszta))
    print("%s: dopisano ukończenie rozdziałów: %s." % (os.path.basename(sciezka), ", ".join(dopisane)))
    print("Kopia poprzedniego zapisu: %s" % kopia)


def main():
    if os.popen('tasklist /FI "IMAGENAME eq Shank.exe" /NH').read().lower().count("shank.exe"):
        print("Shank jest uruchomiony. Zamknij grę i uruchom naprawę jeszcze raz.")
        return 1
    pliki = []
    for wzor in ("*.sav", "savedata.dat"):
        pliki += glob.glob(os.path.join(STEAM_USERDATA, "*", "6120", "remote", wzor))
    if not pliki:
        print("Nie znaleziono zapisu Shanka w folderze Steam.")
        return 1
    for p in pliki:
        try:
            napraw_plik(p)
        except (OSError, ValueError, struct.error) as e:
            print("%s: nie udało się (%s)." % (p, e))
    return 0


if __name__ == "__main__":
    sys.exit(main())
