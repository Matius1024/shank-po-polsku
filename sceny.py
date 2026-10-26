"""Shank (wersja classic): polski lektor i polska audiodeskrypcja do wszystkich filmow.

Kazdy film: "d" = kwestie (lektor, tlumaczenie), "ad" = audiodeskrypcja (opis obrazu). Para: (sekunda, tekst).
Czasy kwestii z rozpisania glosu (tools/transcribe2.py na wersji classic, transcripts_classic/), opisy z klatek
co 2 sekundy (D:\\ShankPolski-audio\\classic\\sheets). Opisy stoja w przerwach miedzy kwestiami.
Uruchom: python -I sceny.py  -> zapisuje napisy/<film>.json
"""
import json
import os

S = {}

S["introscea"] = {"d": [], "ad": [
    (0.3, "Napis: gra zapisuje postęp sama, w punktach kontrolnych."),
    (4.0, "Oznaczenie wiekowe: od 17 lat. Krew, przemoc, wulgaryzmy i treści seksualne."),
    (8.5, "Na tle pustyni pojawia się czerwone logo EA."),
    (13.5, "Logo studia Klei Entertainment."),
]}
S["introscee"] = {"d": [], "ad": [
    (0.3, "Napis: dla najlepszych wrażeń zalecamy grę na padzie."),
    (4.0, "Na tle pustyni pojawia się czerwone logo EA."),
    (9.8, "Logo studia Klei Entertainment."),
]}
S["introtomain"] = {"d": [], "ad": [
    (0.2, "Migawki z gry: Shank wspina się po hakach, tnie olbrzyma, strzela z dwóch pistoletów."),
    (13.5, "Na czerwonym tle napis: Shank."),
]}

S["1a_02"] = {"d": [
    (25.46, "Co pijesz, kolego?"),
    (27.46, "Szukam kogoś."),
    (30.00, "He, he. Tutaj to zwykle ktoś szuka nas."),
    (39.08, "Nie mogę się doczekać, aż spróbuję twojej dziewczyny."),
    (46.70, "Znalazłem ją!"),
    (52.52, "Zabiłbym cię teraz, przyjacielu, ale chcę, żebyś usłyszał, jak krzyczy."),
    (57.02, "Nie! Nie!"),
    (62.80, "Lubisz walki?"),
    (66.78, "Nie tego zapaśnika."),
    (69.68, "Słyszałem, że nie żyjesz."),
    (71.60, "Źle słyszałeś."),
    (73.68, "Nie znoszę się mylić."),
    (78.92, "Mam tu przy barze twojego starego kumpla, Shanka."),
    (82.70, "Co mam z nim zrobić?"),
    (85.34, "Wykończ go."),
    (87.02, "Jasne."),
    (87.60, "Brać go!"),
], "ad": [
    (0.5, "Pustynia w pełnym słońcu. Drogą idzie umięśniony mężczyzna z czerwoną chustą na głowie i pasami na piersi. To Shank."),
    (9.5, "Zakurzone meksykańskie miasteczko. Nad dachami pomnik skrzydlatego anioła."),
    (14.5, "W ciemnym barze dwóch osiłków siłuje się na rękę. Pijak leży na podłodze."),
    (20.0, "Shank wchodzi do baru i podchodzi do wąsatego barmana."),
    (33.7, "Na ścianie wisi plakat walki zapaśników."),
    (36.2, "Wspomnienie. Łysy olbrzym, Rzeźnik."),
    (43.1, "Napis: Rzeźnik. Olbrzym okłada Shanka."),
    (48.6, "Shank, zakrwawiony, patrzy na Rzeźnika."),
    (60.4, "Rzeźnik odchodzi przez drzwi."),
    (64.2, "Shank zgniata plakat."),
    (75.8, "Barman dzwoni do kogoś."),
    (88.8, "Bandyci otaczają Shanka. Jeden rzuca się z maczetą, ale Shank wyciąga nóż i tnie ich jednego po drugim."),
    (97.0, "Dwóch gangsterów celuje do Shanka z obu stron. Shank wytrąca im pistolety, łapie je w locie i strzela do obu."),
    (106.0, "Strzelanina. Po chwili Shank stoi sam wśród trupów."),
    (112.0, "Z cienia wychodzi wielki osiłek z piłą łańcuchową."),
    (119.0, "Shank rzuca w niego nożami i zabija go w fontannie krwi."),
    (125.5, "Shank zabiera piłę łańcuchową i zarzuca ją na ramię."),
    (129.5, "Z ukrycia patrzą na niego kolejni bandyci."),
]}
S["1a_03"] = {"d": [
    (0.00, "Uciekł."),
    (6.08, "Shank wrócił."),
    (8.99, "Kto go zabije, temu będę wdzięczny i sowicie go wynagrodzę."),
], "ad": [
    (2.2, "Telefon odbiera siwy mężczyzna w szelkach."),
    (13.5, "Na zleceniu: osiłek z maczetą, rudowłosa z pistoletem i generał."),
]}
S["1a_04"] = {"d": [], "ad": [
    (1.5, "Na ring wchodzi zapaśnik w czerwono-czarnej masce."),
    (7.8, "Tłum szaleje, fanki machają transparentami: Rzeźnik."),
]}
S["1a_06"] = {"d": [(0.88, "Dość!"), (7.34, "Rzeźniku!")], "ad": [
    (2.0, "Zapaśnik w masce masakruje rywala na ringu."),
    (4.5, "Shank odpycha łysego staruszka."),
    (8.8, "Shank staje naprzeciw zamaskowanego olbrzyma w klatce."),
]}
S["1a_07"] = {"d": [
    (29.78, "Spróbuj w Dzielnicy Mięsnej. Możesz pojechać pociągiem do..."),
    (32.90, "Wiem, gdzie to jest."),
], "ad": [
    (0.3, "Shank dobija zamaskowanego zapaśnika i odcina mu głowę piłą łańcuchową."),
    (6.0, "Wspomnienie: tatuaż z wilkiem na ramieniu Rzeźnika."),
    (11.5, "Shank patrzy na odciętą głowę w masce."),
    (17.5, "Pod maską jest obca twarz. To nie Rzeźnik."),
    (21.0, "Shank jest wściekły."),
    (25.3, "Łysy organizator walk próbuje uciec. Shank go łapie."),
]}
S["1b_02"] = {"d": [], "ad": [
    (0.3, "Parowóz z wagonami pędzi przez pustynię, z komina bucha dym."),
]}
S["1b_03"] = {"d": [], "ad": [(0.2, "Shank biegnie po dachu wagonu.")]}
S["1b_04"] = {"d": [], "ad": [
    (0.5, "Pusta pustynia. Z oddali nadjeżdża samochód."),
    (3.8, "Za kierownicą szczerzy się bandzior w chuście. Goni pociąg."),
]}
S["1b_05"] = {"d": [], "ad": [
    (0.3, "Płonący wrak spada obok Shanka. Pociąg się wykoleja."),
    (7.5, "Shank zeskakuje na piasek i otrząsa się wśród wraku."),
    (12.0, "Wygrzebuje się spod przewróconego wagonu."),
    (15.5, "Rusza pieszo przez pustynię."),
]}
S["1c_01"] = {"d": [(4.70, "Ava!"), (6.10, "Ava!"), (10.28, "Ava!")], "ad": [
    (0.3, "Zachód słońca nad pustynią. Na horyzoncie mała sylwetka Shanka."),
    (7.6, "Wspomnienie. Shank wbiega do domu."),
    (11.8, "Zamaskowany olbrzym powala Shanka na ziemię."),
    (19.5, "Shank leży pobity, z krwią na twarzy."),
    (26.5, "Nad nim staje olbrzym w czerwono-czarnej masce."),
]}
S["1c_02"] = {"d": [
    (0.00, "Dalej żyjesz jak w bajce, co, Rzeźniku?"),
    (4.00, "Shank!"),
    (5.16, "Zabiłbym cię teraz, przyjacielu, ale chcę, żebyś usłyszał, jak krzyczy."),
    (16.78, "Zapłacisz za zabicie Avy."),
    (19.72, "Mówię ci, słodko się ją ujeżdżało, jak tak walczyła o życie."),
], "ad": [
    (9.8, "Wspomnienie: Rzeźnik zakłada maskę i wynosi kobietę z pokoju."),
    (25.1, "W rzeźni Rzeźnik w zakrwawionym fartuchu i czerwonych rękawicach rzuca się na Shanka."),
]}
S["1c_03"] = {"d": [(42.14, "Więc to ta mała dziwka?")], "ad": [
    (0.3, "Shank owija Rzeźnika łańcuchami z haków."),
    (5.5, "Tnie go piłą łańcuchową, tryska krew."),
    (9.5, "Zawiesza olbrzyma na łańcuchach."),
    (14.0, "Rzeźnik wisi na hakach, zakrwawiony. Shank patrzy mu w oczy."),
    (24.5, "Ciemność. Rzeźnik wisi bez życia."),
    (35.5, "Shank wychodzi w noc. Przy drodze neon: Club Stardust, z rysunkiem tancerki."),
    (44.3, "Kobieta z mieczem. Napis: Cassandra."),
    (46.6, "Shank rusza w stronę klubu."),
]}
S["2a_01"] = {"d": [(7.74, "Szukam Cassandry.")], "ad": [
    (0.3, "Neon: Club Stardust."),
    (2.0, "Shank podchodzi do łysego bramkarza i powala go jednym ciosem."),
    (10.3, "Shank wchodzi do klubu."),
]}
S["2a_02"] = {"d": [(7.30, "Plotki tym razem nie kłamały."), (10.40, "Żyjesz.")], "ad": [
    (0.3, "Kamera monitoringu śledzi Shanka."),
    (3.6, "Cassandra, ciemnowłosa kobieta z długimi kolczykami, patrzy w ekran."),
]}
S["2a_04"] = {"d": [
    (0.00, "Pozwól, że ci się przyjrzę."),
    (2.92, "Siedem lat, a ty dalej dobrze wyglądasz."),
    (8.04, "Tamta noc zrujnowała mi życie."),
    (11.44, "Więc to jest ta mała dziwka?"),
    (13.82, "Ava!"),
    (28.20, "Ava!"),
    (30.78, "Może to ty mnie pociąłeś, ale to Cesar wyrzucił mnie jak śmiecia."),
    (36.94, "Ale wiem, że jesteś tu tylko z jednego powodu, więc miejmy to z głowy."),
], "ad": [
    (14.6, "Wspomnienie: Cassandra celuje mieczem w przerażoną Avę."),
    (18.5, "Shank wpada do pokoju, kopniakiem odrzuca Cassandrę i tnie ją jej własnym mieczem po twarzy."),
    (25.0, "Cassandra zakrywa zakrwawioną twarz."),
    (42.5, "Cassandra unosi miecz."),
]}
S["2a_05"] = {"d": [], "ad": [
    (0.3, "Cassandra z mieczem rzuca się na Shanka."),
    (2.5, "Shank strzela. Kula trafia ją w czoło."),
    (7.5, "Cassandra leży martwa w kałuży krwi. Shank odchodzi."),
]}
S["2b_02_0"] = {"d": [
    (10.16, "Ładny tatuaż."),
    (13.26, "Shank?"),
    (14.16, "Myślałem, że nie żyjesz!"),
    (15.86, "Znamy się?"),
    (16.96, "Żartujesz?"),
    (18.16, "Robiliśmy razem robotę!"),
    (20.54, "Powiedz mi, gdzie znajdę Angela."),
    (22.76, "Wiesz, jesteś dość nachalny jak na kogoś na terenie Venomów."),
    (26.38, "Wyglądam, jakby mnie to obchodziło?"),
    (29.10, "Słuszna uwaga."),
], "ad": [
    (0.3, "Bar w czerwonym świetle. Shank patrzy na chudego mężczyznę z tatuażem."),
    (5.0, "Wspomnienie: wąż wytatuowany na plecach. Napis: Angelo."),
]}
S["2b_02_1"] = {"d": [
    (0.00, "Cesar coś mi kiedyś obiecał."),
    (5.28, "Obawiam się, że wątpisz w moją lojalność."),
    (7.70, "Wyciągnąłem cię z rynsztoka."),
    (10.36, "Dałem ci to, czego nie dałbym własnemu synowi."),
    (14.12, "Rozejrzyj się."),
    (15.58, "To wszystko było twoje, a ty na to sikasz."),
    (18.80, "Nie chciałem okazać braku szacunku."),
    (22.12, "Musisz ją zabić."),
    (24.90, "Zabić ją?"),
    (26.04, "Udowodnij, że chcesz należeć do tej rodziny."),
    (30.00, "Jedynej rodziny, która się liczy."),
    (33.18, "Nie zawiodę cię, Cesar."),
    (37.36, "Ty, mój przyjacielu, jesteś niezłym ziółkiem."),
    (40.42, "Angelo."),
    (41.20, "Jasne."),
    (41.84, "Powinien tu być."),
], "ad": [
    (2.4, "Wspomnienie: Cesar, siwy brodacz, w loży pełnej kobiet."),
    (43.2, "Idą do budynku z neonem Sweet Love."),
]}
S["2b_03"] = {"d": [(3.16, "Uważajcie na siebie, chłopcy, i pamiętajcie: bez gumki ani rusz.")], "ad": [
    (0.2, "Obskurny korytarz. Shank wyważa drzwi."),
    (8.0, "Chudzielec szczerzy się w drzwiach."),
]}
S["2b_04"] = {"d": [], "ad": [
    (0.3, "Shank rozrywa łańcuchy olbrzyma. Tryska krew."),
    (5.8, "Skacze na niego i wbija mu ostrze."),
    (9.8, "Dobija go piłą łańcuchową."),
]}
S["2c_01"] = {"d": [
    (0.00, "Wychodzi Wielki Denny, a Shank na to: co jest, kurwa?"),
    (3.78, "Mówię ci, bezcenne."),
    (6.94, "Tęskniłeś?"),
], "ad": [
    (8.0, "Shank chwyta chudzielca za gardło."),
    (10.5, "Chudzielec wyrywa się i ucieka w głąb ulicy."),
]}
S["2c_02"] = {"d": [], "ad": [(0.2, "Pod neonem czeka łysy osiłek.")]}
S["2c_03_0"] = {"d": [
    (1.82, "Mam na karku od cholery kłopotów."),
    (4.12, "Rusz tu dupę!"),
    (6.22, "Jestem tuż przed Karmą."),
], "ad": [(0.0, "Chudzielec dzwoni po pomoc.")]}
S["2c_03_1"] = {"d": [
    (0.00, "Pospiesz się!"),
    (1.40, "Ten dupek nie chce się ode mnie odczepić!"),
    (3.78, "Niech śmigłowiec czeka na mnie na dachu Złotej Rybki!"),
], "ad": []}
S["2c_03_2"] = {"d": [
    (0.00, "Zatrzymaliście się na pieprzony manicure?"),
    (2.92, "Gdzie jesteście?"),
    (4.84, "Jesteśmy w zaułku za Złotym Łańcuchem."),
    (7.68, "Wyślij Babyface'a, wyślij wsparcie, wyślij, kurwa, wszystkich!"),
], "ad": []}
S["2c_04"] = {"d": [(2.04, "Ej, ty, chodź tu.")], "ad": [
    (0.2, "Shank się rozgląda."),
    (4.3, "Z uliczki wychodzi banda: herszt w okularach i hawajskiej koszuli, osiłki z nożami."),
]}
S["2c_05"] = {"d": [
    (0.00, "Kurde, Shank."),
    (1.32, "Wiesz, ja się tylko z tobą trochę zabawiałem."),
    (3.70, "Wiedziałem, że dasz radę tym gościom."),
    (7.26, "Myślę, że powinniśmy połączyć siły, stary."),
    (9.28, "Skoro Falcone'a już nie ma, mógłbym być twoim nowym wspólnikiem."),
    (13.16, "Ach, proszę..."),
    (15.58, "Serio?"),
    (26.50, "Powiedz Angelowi, że jest następny."),
], "ad": [
    (5.9, "Shank mierzy do niego z pistoletu."),
    (16.3, "Shank chowa broń i jednym cięciem odrąbuje chudzielcowi rękę."),
    (21.5, "Tryska krew, ręka leży na ziemi."),
    (29.0, "Chudzielec ucieka, zostawiając smugę krwi."),
]}
S["3c_01"] = {"d": [
    (10.22, "O co chodzi, mój synu?"),
    (12.52, "Shank wrócił."),
    (14.60, "Gdzie on teraz jest?"),
    (18.64, "Idzie tutaj."),
    (22.56, "Nie mogę się doczekać."),
], "ad": [
    (0.3, "Smuga krwi na trawie."),
    (2.2, "Prowadzi do gotyckiego kościoła na wzgórzu."),
    (5.5, "W środku chudzielec bez ręki pada na kolana przed Angelem w sutannie."),
    (26.0, "Shank idzie po krwawym śladzie w stronę kościoła."),
]}
S["3c_02"] = {"d": [(7.36, "Z prochu powstałeś, przyjacielu, w proch się obrócisz.")], "ad": [
    (0.3, "Wspomnienie. Angelo patrzy w dół."),
    (2.2, "Cassandra, Angelo i Rzeźnik stoją nad leżącym Shankiem. Angelo zapala zapałkę."),
    (9.6, "Rzuca ją. Wszystko staje w płomieniach."),
    (13.5, "Trójka patrzy na pożar."),
]}
S["3c_03"] = {"d": [
    (2.96, "Zawiodłem w oczach Boga."),
    (6.22, "Wybacz mi, Ojcze, bo zgrzeszę."),
    (13.10, "Powinienem nazywać cię Łazarzem."),
    (16.22, "A ja na ciebie: trup."),
], "ad": [
    (0.3, "Shank klęczy w konfesjonale i składa ręce."),
    (10.2, "Shank wyskakuje z konfesjonału i powala Angela."),
    (18.0, "Shank celuje do niego z pistoletu. Obok modli się zakonnica."),
]}
S["3c_06"] = {"d": [(2.16, "Błogosławieni wytrwali, co, Shank?")], "ad": [
    (0.2, "Angelo mierzy z wyrzutni."),
    (5.6, "Widok przez celownik."),
]}
S["3c_07"] = {"d": [
    (0.00, "Angelo!"),
    (7.34, "Szukajcie, a znajdziecie."),
    (12.70, "Czego mógłbyś jeszcze szukać?"),
    (15.30, "Co mogłoby zaspokoić człowieka, który stracił tak wiele?"),
    (21.14, "Zemsta."),
], "ad": [
    (1.0, "Shank stoi pod wielkim dzwonem. Z góry celuje w niego Angelo."),
    (22.3, "Shank skacze na Angela i tnie piłą jego broń."),
    (26.2, "Angelo spada z wieży."),
]}
S["3c_08"] = {"d": [(15.44, "Chcę go żywego.")], "ad": [
    (0.3, "Angelo leży ranny przy swojej broni. Shank podchodzi."),
    (4.0, "Z góry sypie się gruz."),
    (9.5, "Spada na niego dzwon."),
    (13.2, "Shank leży przygnieciony."),
    (17.6, "Angelo i jego zbiry otaczają nieprzytomnego Shanka."),
]}
S["4a_01"] = {"d": [
    (0.94, "Nigdy nie przestajesz imponować, Shank."),
    (4.87, "Kiedy spadł ten dzwon, myślałem, że już po tobie, ale i z tego się wywinąłeś."),
    (32.99, "Jesteś moim największym rozczarowaniem."),
    (36.20, "A ty moim."),
    (39.94, "Wykończ go."),
    (41.40, "Trzeba było zostać martwym."),
], "ad": [
    (11.0, "Angelo pociąga za dźwignię."),
    (13.0, "Prąd przeszywa Shanka przypiętego do krzesła elektrycznego. Przed oczami ma Avę."),
    (24.0, "Shank ledwo przytomny. W drzwiach staje Cesar."),
    (44.0, "Ciemność. Zbiry podchodzą do krzesła, a Shank zrywa więzy."),
    (52.5, "Iskry. Shank zabija oprawców w czerwonym półmroku."),
]}
S["4a_02"] = {"d": [(8.64, "Sprawdźcie, co to było.")], "ad": [
    (0.2, "Wybuch nad ranczem."),
    (2.0, "Shank wyskakuje z płomieni z piłą łańcuchową."),
    (6.0, "Cesar ze swoimi ludźmi patrzy w stronę dymu."),
]}
S["4c_04"] = {"d": [(5.14, "Gdzie Angelo?"), (6.98, "Już nie musimy się nim przejmować."), (10.76, "Zaczynamy?")], "ad": [
    (0.3, "Gabinet Cesara. Siwy Cesar z kucykiem stoi przy oknie, plecami do drzwi."),
    (12.5, "Cesar odwraca się i dobywa zakrzywionej szabli."),
]}
S["4c_05"] = {"d": [
    (0.00, "Przez lata stałeś się lepszy."),
    (2.84, "Szkoda, że nie potrafiłeś być lojalny."),
    (5.68, "Lojalny?"),
    (6.86, "Nie wysłałeś mnie tam, żeby sprawdzić moją lojalność."),
    (10.94, "Musiałeś ją znaleźć."),
    (16.82, "Idźcie za nim, żeby znaleźć dziewczynę."),
    (18.92, "Potem zabijcie oboje."),
    (23.12, "Mówiłeś, że tylko go sprawdzisz!"),
    (25.36, "To własny umysł człowieka, a nie jego wróg, zwodzi go na złą drogę."),
    (30.00, "Przestaniesz z tym gównem?"),
    (31.64, "Nigdy cię nie rozumiem."),
    (33.48, "Shank dokonał wyboru, kiedy zastrzelił Rudy'ego, tak jak ty dokonasz wyboru teraz."),
    (53.24, "Zaprowadziłeś ich prosto do niej."),
], "ad": [
    (12.6, "Wspomnienie: Cesar w swoim klubie wydaje rozkaz."),
    (20.3, "Słuchają go Rzeźnik, Cassandra, Angelo i wąsaty osiłek."),
    (41.0, "Shank idzie przez pustynię do domu Avy."),
    (49.5, "Do Avy podchodzi mężczyzna. Teraźniejszość: Shank staje z nożem przed Cesarem."),
]}
S["4c_06"] = {"d": [
    (0.00, "Nie znasz całej historii."),
    (2.32, "Nie wiesz, dlaczego nie mogłem jej zabić."),
    (9.32, "Jest coś, co powinieneś wiedzieć."),
    (11.00, "Noszę twojego syna."),
    (14.64, "Syna?"),
    (18.96, "Nauczyłeś mnie, że nic nie jest ważniejsze od rodziny."),
    (22.30, "Ja byłem twoją rodziną."),
    (24.12, "Ona też."),
    (26.90, "Gdybym wiedział, że jest w ciąży, to by wiele zmieniło."),
], "ad": [
    (4.9, "Wspomnienie: Ava dotyka twarzy Shanka."),
    (15.8, "Do pokoju wpada Rzeźnik."),
    (31.0, "Shank zaciska zęby z wściekłości."),
]}
S["4c_07"] = {"d": [(39.74, "Zamknij się!")], "ad": [
    (0.3, "Na tarasie Shank ściera się z Cesarem."),
    (3.0, "Cesar tnie go szablą, tryska krew."),
    (6.5, "Shank atakuje piłą łańcuchową, ale pada ranny na posadzkę."),
    (12.0, "Cesar wyciąga dwa pistolety i śmieje się."),
    (20.0, "Shank wstaje. Cesar strzela, a Shank odbija kule i rusza na niego."),
    (31.5, "Błysk. Walczą wręcz."),
    (35.5, "Shank uderza Cesara głową i unosi nóż."),
    (42.0, "Ciemność, a potem nóż wbija się w szyję Cesara."),
    (49.5, "Cesar leży martwy na posadzce, z raną na czole."),
    (57.5, "Shank klęka przy nim, a potem wstaje."),
    (63.5, "Shank odchodzi samotnie w stronę zachodzącego słońca."),
    (72.0, "Napis: Shank. Koniec."),
]}
S["5a_01"] = {"d": [
    (0.00, "Jesteśmy wspólnikami od dziecka, więc wiesz, że jestem po twojej stronie."),
    (3.92, "I naprawdę mam gdzieś, gdzie moczysz kija, ale Cesar nie jest zadowolony."),
    (9.06, "Z powodu Avy?"),
    (10.94, "Ona jest przedszkolanką."),
    (12.68, "Jest nieszkodliwa."),
    (14.28, "No właśnie."),
    (15.04, "Ona nie jest taka jak my."),
    (20.16, "Następnym razem chcę też golenie."),
    (25.34, "Tak?"),
    (27.56, "Jasne."),
    (29.54, "Cassandra."),
    (37.14, "Co to za goście?"),
    (38.82, "Nie mam pojęcia."),
    (40.24, "Może się dowiemy?"),
    (45.62, "Chyba nie słyszeliście, chłopcy."),
    (51.00, "Przejmujemy interes."),
], "ad": [
    (16.5, "Na podłodze leży pobity fryzjer. Wspólnik zabiera mu pieniądze."),
    (22.6, "Wspólnikowi dzwoni telefon."),
    (30.5, "Przed barem stoi rząd motocykli."),
    (43.2, "Zza motocykli wychodzi banda motocyklistów w skórach."),
]}
S["5a_03"] = {"d": [
    (0.27, "Kurczę, nie wierzę, że ty kiedykolwiek..."),
    (4.92, "Ona cię chce, stary."),
    (8.68, "Poza tym mam Avę."),
    (10.90, "Twoja przedszkolanka tak potrafi?"),
    (26.60, "Tak, mała."),
    (28.68, "Denny ma dla ciebie prezent."),
    (30.96, "I to naprawdę duży. Widziałem go."),
    (35.66, "Tylko do patrzenia, przyjacielu."),
    (37.86, "Spadaj, amigo."),
    (40.48, "Dusty, trzeba dać tym chujkom nauczkę."),
], "ad": [
    (13.3, "Na scenie tańczy striptizerka. Przy stolikach siedzą motocykliści."),
    (21.8, "Tłusty motocyklista w różowych okularach ślini się przy scenie."),
    (33.0, "Motocyklista łapie tancerkę za nogę."),
]}
S["5a_04"] = {"d": [
    (0.00, "Ooo, Denny lubi, jak się stawiasz, suko."),
    (4.36, "Nikt ci nie pomoże."),
    (7.39, "Tamci chujkowie pewnie już nie żyją."),
    (11.05, "My, chujkowie, wciąż żyjemy, dupku."),
], "ad": [
    (3.2, "Denny dusi Cassandrę."),
]}
S["5a_05"] = {"d": [
    (0.96, "Czekaj."),
    (2.26, "Chcę Denny'ego żywego."),
    (6.83, "Na pewno?"),
    (8.72, "Chcę dać temu grubemu chujowi nauczkę."),
    (13.26, "Chodźmy obejrzeć walkę."),
], "ad": [
    (5.5, "Cassandra dobywa miecza."),
    (15.0, "Cassandra unosi miecz nad Dennym. Na niebie czerwony sierp księżyca."),
]}
S["5b_01"] = {"d": [
    (9.04, "Miał przegrać."),
    (12.72, "Musimy zapytać Cesara."),
    (14.68, "Pieprzyć Cesara."),
    (15.88, "Kiedy będziesz rządził kartelem, będziesz mógł robić, co chcesz."),
    (19.02, "Ale na razie pytamy twojego ojca."),
    (25.02, "Ludzie Cesara."),
    (26.34, "Brać go!"),
], "ad": [
    (0.3, "Podziemny ring. Zapaśnik rzuca rywalem o ziemię."),
    (4.2, "Shank i wspólnik patrzą z trybun."),
    (10.4, "Wspólnik sięga po pistolet."),
    (22.0, "Ochroniarze ich zauważają."),
    (28.0, "Zaczyna się bójka."),
]}
S["5b_02"] = {"d": [
    (1.46, "To czekaj na mnie w limuzynie."),
    (7.00, "Tak, mamy ścisłą zasadę: żadnych świadków, panie."),
    (11.80, "Cesar może mieć mój kontrakt, ale nie ma mojej kariery."),
    (16.60, "Czegoś nie zapomniałeś?"),
    (18.60, "Nie kładę się dla nikogo!"),
    (21.60, "Och, myślę, że się położysz. Prawda, Shank?"),
], "ad": [
    (0.0, "Zapaśnik z kobietami w szatni."),
]}
S["5b_04"] = {"d": [
    (0.00, "Czy nie zrobiłem wszystkiego, czego chce?"),
    (2.44, "Ściągałem długi, tłukłem dłużników na kwaśne jabłko."),
    (5.96, "Czemu mam przegrać z takim marnym palantem jak El Raton?"),
    (9.88, "Za dużo pytań, nie ta odpowiedź."),
], "ad": [
    (12.2, "Shank łapie zapaśnika od tyłu."),
]}
S["5b_05"] = {"d": [
    (4.20, "Uznajmy to za pierwszą ratę."),
    (8.54, "Znowu idziesz dziś wieczorem z tą swoją przedszkolanką?"),
    (11.36, "Tak."),
    (12.46, "Cesar ma rację."),
    (13.68, "Ava ma na ciebie zły wpływ."),
    (18.04, "Hej, Rudy."),
    (19.62, "Widziałeś to?"),
    (20.88, "Wybiłem mu ząb na czysto."),
    (23.10, "Bum!"),
    (23.58, "Nawet nie trzeba było znieczulenia."),
    (26.48, "Co jest, kurwa?"),
    (28.80, "Doskonale."),
    (31.16, "Jak sobie chcesz, Pasikoniku."),
    (32.56, "Któryś z was kiedyś chybi."),
    (34.50, "Wątpię."),
    (36.74, "Shank, muszę z tobą później porozmawiać."),
], "ad": [
    (0.3, "W powietrzu wiruje wybity ząb. Zapaśnik leży nieprzytomny na bruku."),
    (15.6, "Hacjenda Cesara. Ochroniarz otwiera drzwi."),
]}
S["5c_01"] = {"d": [
    (2.70, "A myślałem, że dziś będzie nudno."),
    (6.10, "Cesar kazał przyprowadzić księdza żywego i zrobić to po cichu."),
    (11.38, "Jak pieprzona kościelna mysz."),
], "ad": [
    (0.2, "Noc. Pod kościołem strażnik z karabinem."),
]}
S["5c_02"] = {"d": [], "ad": [
    (0.2, "Shank i wspólnik powalają strażnika."),
    (2.2, "Pod łukiem stoi łysy ksiądz, ojciec Gomez."),
]}
S["5c_03"] = {"d": [
    (13.49, "Chcemy tylko porozmawiać, ojcze."),
    (15.49, "Więzienie zmienia człowieka, kuzynie. Nie jestem już tym, kogo znałeś."),
    (30.34, "Odsiedziałeś swoje, Angelo."),
    (32.58, "Teraz moja kolej, żeby ci pomóc."),
    (37.96, "Ojcze Gomez, musimy porozmawiać."),
    (41.70, "Wolałbym stracić język."),
    (43.98, "Da się załatwić."),
    (46.28, "Może ojciec nie rozumie."),
    (48.14, "Jesteśmy tu, żeby ojcu pomóc."),
    (50.18, "Ludzie z mojej parafii nie potrzebują takiej pomocy."),
    (53.88, "Jesteście zarazą, którą Bóg zniszczy."),
    (57.44, "Szczerze, ojcze, nie uważa ojciec, że ten cały Bóg jest trochę przereklamowany?"),
    (63.44, "Uznam to za odpowiedź przeczącą."),
    (70.80, "Zabiłeś duchownego."),
    (72.96, "Chcesz być następny, ślicznotko?"),
    (74.54, "Czekaj."),
    (76.94, "Nikt nie wiedział, że ojciec Gomez już przyjechał do miasta."),
    (80.34, "To może się dobrze ułożyć."),
    (82.34, "Możesz mówić do mnie: ojcze Ramirez, mój synu."),
], "ad": [
    (0.2, "Strażnik ginie porażony prądem."),
    (6.0, "Wieża kościoła w świetle księżyca."),
    (9.5, "Ksiądz broni się krzyżem, ale Shank go powala."),
    (21.0, "Ranek przy hacjendzie Cesara."),
    (25.5, "W gabinecie czeka Cesar z kieliszkiem. Obok stoi młody Angelo w kamizelce."),
    (66.0, "Angelo wyciąga pistolet i zabija księdza."),
    (69.0, "Shank celuje do Angela."),
    (86.0, "Na plecach Angela tatuaż węża. Angelo uśmiecha się chytrze."),
]}
S["5d_01"] = {"d": [
    (7.64, "Tak."),
    (9.44, "Teraz?"),
    (11.70, "Ale jestem z Avą."),
    (14.42, "Dobra, będę."),
    (19.38, "Jeden przystanek i jedziemy dalej."),
    (31.64, "Zaraz wracam."),
    (36.30, "Myślałem, że zastępca burmistrza miał tu być dopiero jutro."),
    (39.64, "Cesar mówi, że robimy to teraz."),
    (47.96, "To nasz gość?"),
    (49.30, "Aha."),
    (49.86, "Cesar mówi, że jak sprzątniemy tego gnoja, przekupimy kapitana policji i będziemy mieć antyterrorystów na zawołanie."),
    (56.46, "Miło będzie dla odmiany nie walczyć z antyterrorystami."),
    (59.98, "Tobie może."),
    (62.24, "Rudy, pilnuj tylnego wejścia."),
    (66.30, "Co tu się dzieje?"),
    (67.70, "Zastępca burmistrza wygłasza przemówienie."),
    (69.48, "Ostro bierze się za kartele."),
    (71.94, "Musi pani przestawić samochód."),
    (73.58, "Kluczyki ma mój chłopak."),
    (75.60, "To lepiej go pani znajdzie, bo odholujemy."),
    (82.98, "Macie przepustki?"),
    (84.52, "Tak."),
    (85.70, "Proszę."),
], "ad": [
    (0.3, "Wieczór. Shank wysiada z kabrioletu, Ava zostaje."),
    (4.0, "Shank żegna się z Avą i odbiera telefon."),
    (22.0, "Za rogiem stoi dwóch policjantów z bronią."),
    (33.0, "Na parkingu czekają wspólnik i ochroniarz z przepaską."),
    (42.0, "Przed salą stoi kordon policji i limuzyna."),
    (64.0, "Policjant podchodzi do kabrioletu Avy."),
    (78.0, "Ava odjeżdża."),
    (80.0, "Wspólnik podchodzi do strażników z bronią."),
    (86.6, "Wspólnik wyciąga pistolet i strzela. Strażnicy padają."),
]}
S["5d_02"] = {"d": [], "ad": [
    (0.2, "Ava biegnie korytarzem."),
    (2.2, "Zagląda przez drzwi. Jest przerażona."),
]}
S["5d_08"] = {"d": [(0.00, "Tam jest!"), (9.07, "Nie masz szans.")], "ad": [
    (2.0, "Shank i wspólnik wpadają na korytarz. Przy drzwiach stoi wąsaty olbrzym w garniturze."),
    (6.0, "Olbrzym rozpina marynarkę i zaciska pięści."),
]}
S["5d_09"] = {"d": [
    (17.37, "Ava..."),
    (24.30, "Nie!"),
    (33.98, "Widziała, jak zastrzeliłem zastępcę burmistrza. Świadków. A potem mnie."),
    (57.42, "Shank!"),
    (58.56, "Co jest, kurwa?"),
    (59.98, "Rozpoznali go!"),
    (61.46, "To osobisty ochroniarz Cesara!"),
    (66.96, "Dość już wycierpiałeś."),
    (70.06, "Shank!"),
    (73.78, "Shank!"),
    (80.06, "Idźcie za nim, żeby znaleźć dziewczynę."),
    (83.02, "Potem zabijcie oboje."),
], "ad": [
    (0.2, "Wspólnik i olbrzym w garniturze walczą na noże. Shank tnie olbrzyma, tryska krew."),
    (11.5, "Shank patrzy przed siebie, przerażony."),
    (19.2, "W drzwiach stoi zakrwawiona Ava. Ochroniarz z przepaską na oku łapie ją i celuje w nią z pistoletu."),
    (26.5, "Wspólnik pada na podłogę, zostaje kałuża krwi."),
    (40.0, "Ava, ranna, patrzy na Shanka. Shank celuje do ochroniarza."),
    (44.5, "Shank skacze z dwoma pistoletami i strzela. Ochroniarz pada martwy."),
    (52.0, "Ava podbiega i rzuca się Shankowi w ramiona."),
    (75.5, "Pusta droga przez palmowy zagajnik. W oddali znika samochód."),
    (85.0, "Napis: Shank."),
]}
S["toro_intro_movie"] = {"d": [(4.68, "Tu się to kończy, głupcze.")], "ad": [
    (0.3, "Na tarasie hacjendy czeka umięśniony olbrzym z bandażem na głowie."),
    (7.9, "Olbrzym szczerzy zęby."),
]}
S["toro_intro_scene1"] = {"d": [], "ad": [(0.1, "Shank mruży oczy.")]}
S["toro_intro_scene1a"] = {"d": [], "ad": [(0.1, "Ostrze błyska nad pustynią.")]}
S["paxtorodead"] = {"d": [], "ad": [
    (0.2, "Olbrzym z kolczykiem w nosie słania się na tarasie."),
    (3.8, "Shank wpada na niego z piłą łańcuchową i strzela."),
    (6.0, "Olbrzym leży martwy w kałuży krwi. Shank odchodzi."),
]}
S["unlock_game"] = {"d": [], "ad": [
    (0.2, "Zwiastun pełnej wersji. Na pustyni stoi Shank, za nim słońce."),
    (4.0, "Napis: Shank."),
    (5.5, "Migawki z gry: Shank skacze po dachach i słupach, wspina się po lodowej ścianie, przemyka przez fabrykę."),
    (28.0, "Rozwala bandytów w barze."),
    (36.0, "Walczy na dachach z kolejnymi wrogami, a na moście z olbrzymem."),
    (58.0, "Siecze piłą łańcuchową w rzeźni."),
    (66.0, "Strzela, tnie i rzuca wrogami."),
    (90.0, "Shank dusi łańcuchem olbrzyma. Napis: Shank."),
]}
S["credits_1"] = {"d": [], "ad": [
    (0.2, "Napisy końcowe. Twórcy gry: Jeff Agala i Jamie Cheng."),
    (4.0, "Na czerwonym tle czarne sylwetki: Shank biegnie po dachach i walczy z kolejnymi wrogami."),
    (42.0, "Rysunki Shanka z jego bronią: piła łańcuchowa, pistolety, granatnik, pistolet maszynowy, ostrza."),
]}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "napisy", "classic")
    os.makedirs(out_dir, exist_ok=True)
    for fn in os.listdir(out_dir):
        os.remove(os.path.join(out_dir, fn))
    for movie, d in S.items():
        lines = [{"start": s, "kind": "d", "pl": t} for s, t in d["d"]]
        lines += [{"start": s, "kind": "ad", "pl": t} for s, t in d["ad"]]
        lines.sort(key=lambda l: l["start"])
        with open(os.path.join(out_dir, movie + ".json"), "w", encoding="utf-8") as f:
            json.dump({"movie": movie, "lines": lines}, f, ensure_ascii=False, indent=1)
    print(len(S), "filmow,", sum(len(v["d"]) for v in S.values()), "kwestii,",
          sum(len(v["ad"]) for v in S.values()), "opisow")


if __name__ == "__main__":
    main()
