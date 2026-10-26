"""Polskie tlumaczenie kwestii ze scenek Shanka.

Kazda kwestia: (sekunda od poczatku filmu, tekst polski). Czasy z rozpisania glosu (tools/transcribe2.py,
transcripts2/), kilka uzupelnionych z pierwszego rozpisania (transcripts/). W komentarzu oryginal.
Uruchom: python -I tlumaczenie.py  -> zapisuje napisy/<film>.json
"""
import json
import os

PL = {
    "1a_02": [
        (27.10, "Ava."),
        (42.02, "Fan walk?"),  # You a fight fan?
        (45.90, "Nie tego zapaśnika."),
        (48.76, "Słyszałem, że nie żyjesz."),
        (50.76, "Źle słyszałeś."),
        (52.78, "Nie znoszę się mylić."),
        (57.80, "Brać go!"),
    ],
    "1a_03": [
        (0.00, "Uciekł."),
        (6.08, "Shank wrócił."),
        (8.99, "Ktokolwiek go zabije, zyska moją wdzięczność i sowitą nagrodę."),
    ],
    "1a_06": [(0.00, "Dość!"), (7.32, "Rzeźniku!")],
    "1a_07": [(29.78, "Spróbuj w Dzielnicy Mięsnej. Możesz pojechać pociągiem do..."), (32.90, "Wiem, gdzie to jest.")],
    "1c_01": [(4.68, "Ava! Ava!")],
    "1c_02": [
        (0.00, "Dalej żyjesz jak w bajce, co, Rzeźniku?"),
        (4.00, "Shank!"),
        (5.04, "Zapłacisz za zabicie Avy."),
    ],
    "2a_01": [(7.74, "Szukam Cassandry.")],
    "2a_02": [(7.30, "Plotki tym razem nie kłamały."), (10.40, "Żyjesz.")],
    "2a_04": [
        (0.00, "Pozwól, że ci się przyjrzę."),
        (2.92, "Siedem lat, a ty dalej dobrze wyglądasz."),
        (8.02, "Tamta noc zrujnowała mi życie."),
        (11.44, "Więc to jest ta mała dziwka?"),
        (13.84, "Ava!"),
        (28.20, "Ava!"),
        (30.78, "Może to ty mnie pociąłeś, ale to Cesar wyrzucił mnie jak śmiecia."),
        (36.94, "Ale wiem, że jesteś tu tylko z jednego powodu, więc miejmy to z głowy."),
    ],
    "2b_02_0": [
        (10.16, "Ładny tatuaż."),
        (13.26, "Shank?"),
        (14.16, "Myślałem, że nie żyjesz!"),
        (15.86, "Znamy się?"),
        (16.96, "Żartujesz?"),
        (18.16, "Robiliśmy razem robotę!"),
        (20.58, "Powiedz mi, gdzie znajdę Angela."),
        (22.76, "Wiesz, jesteś dość nachalny jak na kogoś na terenie Venomów."),
        (26.36, "Wyglądam, jakby mnie to obchodziło?"),
        (29.14, "Słuszna uwaga."),
    ],
    "2b_02_1": [
        (0.00, "Cesar coś mi kiedyś obiecał."),
        (5.54, "Obawiam się, że wątpisz w moją lojalność."),
        (7.98, "Wyciągnąłem cię z rynsztoka."),
        (10.62, "Dałem ci to, czego nie dałbym własnemu synowi."),
        (14.38, "Rozejrzyj się."),
        (15.88, "To wszystko było twoje, a ty na to sikasz."),
        (18.80, "Nie chciałem okazać braku szacunku."),
        (22.42, "Musisz ją zabić."),
        (25.14, "Zabić ją?"),
        (26.48, "Udowodnij, że chcesz należeć do tej rodziny."),
        (30.00, "Jedynej rodziny, która się liczy."),
        (33.46, "Nie zawiodę cię, Cesar."),
        (37.62, "Ty, mój przyjacielu, jesteś niezłym ziółkiem."),
        (40.70, "Angelo."),
        (41.44, "Jasne."),
        (42.10, "Powinieneś tu być."),
    ],
    "2b_03": [(3.16, "Uważajcie na siebie, chłopcy, i pamiętajcie: bez gumki ani rusz.")],
    "2c_01": [
        (0.00, "Wychodzi Wielki Denny, a Shank na to: co jest, kurwa?"),
        (3.78, "Mówię ci, bezcenne."),
        (6.94, "Tęskniłeś?"),
    ],
    "2c_03_0": [
        (1.80, "Mam na karku od cholery kłopotów."),
        (4.12, "Rusz tu dupę!"),
        (6.22, "Jestem tuż przed Karmą."),
    ],
    "2c_03_1": [
        (0.00, "Pospiesz się!"),
        (1.40, "Ten dupek nie chce się ode mnie odczepić!"),
        (3.78, "Niech śmigłowiec czeka na mnie na dachu Złotej Rybki!"),
    ],
    "2c_03_2": [
        (0.00, "Zatrzymaliście się na pieprzony manicure?"),
        (2.94, "Gdzie jesteście?"),
        (4.84, "Jesteśmy w zaułku za Złotym Łańcuchem."),
        (7.68, "Wyślij Babyface'a, wyślij wsparcie, wyślij, kurwa, wszystkich!"),
    ],
    "2c_04": [(2.04, "Ej, ty, chodź tu.")],
    "2c_05": [
        (0.00, "Kurde, Shank."),
        (1.34, "Wiesz, ja się tylko z tobą trochę zabawiałem."),
        (3.70, "Wiedziałem, że dasz radę tym gościom."),
        (7.26, "Myślę, że powinniśmy połączyć siły, stary."),
        (9.28, "Skoro Falcone'a już nie ma, mógłbym być twoim nowym wspólnikiem."),
        (13.16, "Ach, proszę..."),
        (15.58, "Serio?"),
        (26.50, "Powiedz Angelowi, że jest następny."),
    ],
    "3c_01": [
        (1.36, "O co chodzi, mój synu?"),
        (12.47, "Shank wrócił."),
        (14.55, "Gdzie on teraz jest?"),
        (18.51, "Idzie tutaj."),
        (22.54, "Nie mogę się doczekać."),
    ],
    "3c_02": [(7.36, "Z prochu powstałeś, przyjacielu, w proch się obrócisz.")],
    "3c_03": [
        (2.96, "Zawiodłem w oczach Boga."),
        (6.22, "Wybacz mi, Ojcze, bo zgrzeszę."),  # Forgive me, Father, for I will sin.
        (12.94, "Powinienem nazywać cię Łazarzem."),
        (16.20, "A ja ciebie: wyruchanym."),
    ],
    "3c_06": [(2.16, "Błogosławieni wytrwali, co, Shank?")],
    "3c_07": [
        (0.00, "Angelo!"),
        (7.34, "Szukajcie, a znajdziecie."),
        (12.70, "Czego mógłbyś jeszcze szukać?"),
        (15.30, "Co mogłoby zaspokoić człowieka, który stracił tak wiele?"),
        (21.12, "Zemsta."),
    ],
    "3c_08": [(15.66, "Chcę go żywego.")],
    "4a_01": [
        (0.92, "Nigdy nie przestajesz imponować, Shank."),
        (4.87, "Kiedy spadł ten dzwon, myślałem, że już po tobie, ale i z tego się wywinąłeś."),
        (33.34, "Jesteś moim największym rozczarowaniem. Dobij go. Trzeba było zostać martwym."),
    ],
    "4a_02": [(8.64, "Sprawdźcie, co to było.")],
    "4c_04": [(5.14, "Gdzie Angelo?"), (6.98, "Już nie musimy się nim przejmować."), (10.76, "Zaczynamy?")],
    "4c_05": [
        (0.00, "Przez lata stałeś się lepszy."),
        (2.86, "Szkoda, że nie potrafiłeś być lojalny."),
        (5.70, "Lojalny?"),
        (6.88, "Nie wysłałeś mnie tam, żeby sprawdzić moją lojalność."),
        (10.96, "Musiałeś ją znaleźć."),
        (16.84, "Idźcie za nim, żeby znaleźć dziewczynę."),
        (18.94, "Potem zabijcie oboje."),
        (23.12, "Mówiłeś, że tylko go sprawdzisz!"),
        (25.36, "To własny umysł człowieka, a nie jego wróg, zwodzi go na złą drogę."),
        (30.00, "Przestaniesz z tym gównem?"),
        (31.66, "Nigdy cię nie rozumiem."),
        (33.48, "Shank dokonał wyboru, kiedy zastrzelił Rudy'ego, tak jak ty dokonasz wyboru teraz."),
        (53.26, "Zaprowadziłeś ich prosto do niej."),
    ],
    "4c_06": [
        (0.00, "Nauczyłeś mnie, że nic nie jest ważniejsze od rodziny."),
        (2.98, "Ja byłem twoją rodziną."),
        (4.78, "Ona też."),
    ],
    "5a_01": [
        (0.70, "Jesteśmy wspólnikami od dziecka, więc wiesz, że jestem po twojej stronie."),
        (4.18, "Ale Cesar nie jest zadowolony."),
        (6.50, "Z powodu Avy?"),
        (8.42, "Ona jest przedszkolanką."),
        (10.22, "Jest nieszkodliwa."),
        (11.76, "No właśnie."),
        (12.50, "Ona nie jest taka jak my."),
        (17.56, "Następnym razem chcę też golenie."),
        (22.82, "Tak?"),
        (25.04, "Jasne."),
        (27.14, "Cassandra."),
        (34.70, "Co to za goście?"),
        (36.20, "Nie mam pojęcia."),
        (37.82, "Chyba nie słyszeliście, chłopcy."),
        (39.82, "Przejmujemy interes."),
    ],
    "5a_04": [(1.52, "Dusty, trzeba dać tym chujkom nauczkę."), (5.70, "Biorę go, Denny.")],
    "5a_05": [
        (1.54, "Czekaj."),
        (2.32, "Chcę Denny'ego żywego."),
        (6.85, "Na pewno?"),
        (8.80, "Chcę dać temu grubemu chujowi nauczkę."),
        (13.34, "Chodźmy obejrzeć walkę."),
    ],
    "5b_01": [
        (9.04, "Miał przegrać."),
        (12.72, "Musimy zapytać Cesara."),
        (14.68, "Pieprzyć Cesara."),
        (15.90, "Kiedy będziesz rządził kartelem, będziesz mógł robić, co chcesz."),
        (19.02, "Ale na razie pytamy twojego ojca."),
        (25.02, "Ludzie Cesara."),
        (26.36, "Brać go!"),
    ],
    "5b_02": [
        (1.78, "Cesar może mieć mój kontrakt, ale nie ma mojej kariery."),
        (6.28, "Czegoś nie zapomniałeś?"),
        (7.94, "Nie kładę się dla nikogo."),
    ],
    "5b_04": [
        (0.00, "Czy nie zrobiłem wszystkiego, czego chce?"),
        (2.44, "Ściągałem długi, tłukłem dłużników na kwaśne jabłko."),
        (5.98, "Czemu mam przegrać z takim marnym palantem jak El Raton?"),
        (9.88, "Za dużo pytań, a nie ta odpowiedź."),
    ],
    "5b_05": [
        (4.20, "Uznajmy to za pierwszą ratę."),
        (8.54, "Znowu wychodzisz dziś wieczorem z tą przedszkolanką?"),
        (11.36, "No."),
        (12.46, "Cesar ma rację."),
        (13.68, "Ava ma na ciebie zły wpływ."),
        (18.04, "Hej, Rudy."),
        (19.62, "Widziałeś to?"),
        (20.88, "Wybiłem mu ząb na czysto."),
        (23.10, "Bam!"),
        (23.58, "Nawet znieczulenie nie było potrzebne."),
        (26.46, "Co jest, kurwa?"),
        (28.76, "Doskonale."),
        (31.16, "Jak tam chcesz, Koniku Polny."),
        (32.56, "Któryś z was kiedyś spudłuje."),
        (34.50, "Wątpię."),
        (36.74, "Shank, muszę z tobą później pogadać."),
    ],
    "5c_01": [
        (2.70, "A myślałem, że dzisiejszy wieczór będzie nudny."),
        (6.10, "Cesar powiedział, że przyprowadzamy księdza żywego i robimy to po cichu."),
        (11.36, "Jak pieprzona kościelna mysz."),
    ],
    "5c_03": [
        (18.38, "Nie jestem już tym samym człowiekiem, którego znałeś."),
        (20.78, "Odsiedziałeś swoje, Angelo."),
        (22.98, "Teraz moja kolej, żeby ci pomóc."),
        (30.00, "Nikt jeszcze nie wiedział, że ojciec Gomez przyjechał do miasta."),
        (33.60, "To może się nieźle ułożyć."),
        (35.56, "Możesz mnie nazywać ojcem Ramirezem, mój synu."),
    ],
    "5d_01": [
        (1.14, "Jeden przystanek i ruszamy dalej."),
        (18.64, "To nasz gość?"),
        (20.00, "No."),
        (20.60, "Cesar mówi, że jak sprzątniemy tego gnoja, przekupimy kapitana policji i będziemy mieć oddziały SWAT, kiedy zechcemy."),
        (27.10, "Rudy, pilnuj tylnego wejścia."),
        (30.82, "Co tu się dzieje?"),
        (32.16, "Zastępca burmistrza wygłasza przemówienie."),
        (33.98, "Ostro bierze się za kartele."),
        (36.44, "Musi pani przestawić samochód."),
        (38.10, "Kluczyki ma mój chłopak."),
        (40.12, "Lepiej niech go pani znajdzie, bo odholujemy auto."),
        (47.46, "Macie przepustki?"),
        (48.96, "Tak."),
        (50.14, "Proszę."),
    ],
    "5d_08": [(0.00, "Tam jest!"), (9.07, "Nie masz szans.")],
    "5d_09": [
        (34.22, "Widziała, jak zastrzeliłem zastępcę burmistrza. Świadkowie. A potem ja."),
        (54.98, "Shank, co jest, kurwa?"),
        (57.82, "Rozpoznali go."),
        (59.40, "To osobisty ochroniarz Cesara."),
        (63.76, "Dość już wycierpiałeś."),
        (67.10, "Shank?"),
        (77.84, "Idźcie za nim, żeby znaleźć dziewczynę. Potem zabijcie oboje."),
    ],
    "toro_intro_movie": [(4.74, "Tu się to kończy, głupcze.")],
}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "napisy")
    os.makedirs(out_dir, exist_ok=True)
    for fn in os.listdir(out_dir):
        os.remove(os.path.join(out_dir, fn))
    for movie, lines in PL.items():
        with open(os.path.join(out_dir, movie + ".json"), "w", encoding="utf-8") as f:
            json.dump({"movie": movie, "lines": [{"start": s, "pl": t} for s, t in lines]},
                      f, ensure_ascii=False, indent=1)
    print(len(PL), "filmow,", sum(len(v) for v in PL.values()), "kwestii")


if __name__ == "__main__":
    main()
