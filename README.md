# Shank po polsku

Polski lektor i audiodeskrypcja do scenek filmowych z gry **Shank** (2010, Klei Entertainment).
Projekt fanowski dla niewidomych i słabowidzących graczy, ale może z niego korzystać każdy.

## Pobieranie

Instalator jest w zakładce [Releases](../../releases/latest): plik `ShankPoPolsku-<wersja>-instalator.exe`.
Instalacja nie wymaga uprawnień administratora. Instalator jest po polsku i działa z czytnikami ekranu.
Można w nim wybrać lektora i audiodeskrypcję, tylko lektora albo tylko audiodeskrypcję.

## Co to robi

- Gdy w grze leci scenka, polski lektor (głos męski) czyta kwestie na tle ściszonego oryginału.
- W przerwach między kwestiami drugi głos (kobiecy) czyta audiodeskrypcję, czyli opis tego, co widać na ekranie.
- Gotowe dla wszystkich 63 filmów z gry.

Program działa samodzielnie, obok gry. Nie zmienia plików gry i nie potrzebuje żadnego moda.
Można go używać razem z modem dostępności [Shank Access](https://github.com/KarlBelanger/shank_access) albo bez niego.
Scenki rozpoznaje po pliku filmu, który otwiera gra.

## Wersje gry

- **Gałąź „classic” na Steam** (zalecana): wszystkie scenki mają lektora i audiodeskrypcję.
  Jak ją włączyć: Steam, prawy przycisk na grze Shank, Właściwości, Wersje beta, wybierz „classic”.
- **Zwykła wersja**: 38 scenek ma lektora i audiodeskrypcję, a pozostałe 21 tylko lektora.
- **Kopia spoza Steam** (np. GOG): wpisz folder gry w ustawieniach (`folder_gry` w `shank_polski.ini`).

## Ustawienia

Menu Start, folder „Shank po polsku”, skrót „Ustawienia”. Można tam wyłączyć audiodeskrypcję,
czytać tłumaczenie czytnikiem ekranu zamiast nagrań i zmienić głośność gry pod lektorem.

## Dla twórców

- `sceny.py`: tłumaczenie kwestii i audiodeskrypcja dla każdego filmu, z czasami, zapisywane do `napisy/classic/*.json`.
- `tools/make_lektor.py`: nagrania głosami syntezatora Microsoft (edge-tts: Marek, Zofia). `tools/dopasuj.py`
  dopasowuje opisy do przerw między kwestiami, a `tools/symulacja.py` sprawdza, czy nic się nie nakłada.
- `tools/shank_polski.py`: sam program. `tools/zbuduj_instalator.py`: buduje instalator (PyInstaller i Inno Setup).

Nagrania nie są w repozytorium, tylko w instalatorze.
