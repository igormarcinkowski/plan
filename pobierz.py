from pathlib import Path
from datetime import date, datetime
import json

folder = Path(__file__).parent

dzisiaj = date.today()
rok = dzisiaj.year
pierwszy_dzien = date(rok, 8, 31)
tydzien = (dzisiaj - pierwszy_dzien).days // 7 + 1

dyzurny1 = tydzien
if dyzurny1 > 17:
    dyzurny1 = -17
dyzurny2 = 35 - dyzurny1

nazwaFolderu = 'tydzien_' + str(tydzien)
folderNazwa = folder / 'data' / nazwaFolderu

sciezkaPlan = folderNazwa / 'plan.json'

with open(sciezkaPlan, 'r', encoding='utf-8') as plan:
    danePlan = json.load(plan)

dniTygodnia = [
    'Poniedziałek',
    'Wtorek',
    'Środa',
    'Czwartek',
    'Piątek'
]

zmiany = set()

for plik in folderNazwa.glob("zastepstwa-*.json"):
    dzienn = (
        plik.name
        .removeprefix("zastepstwa-")
        .removesuffix(".json")
    )

    dzienTygodnia = datetime.strptime(
        dzienn,
        "%Y-%m-%d"
    ).weekday()

    if dzienTygodnia >= 5:
        continue

    dzienTygodniaNazwa = dniTygodnia[dzienTygodnia]

    with open(plik, 'r', encoding='utf-8') as zastepstwa:
        daneZastepstwa = json.load(zastepstwa)

    for j in daneZastepstwa:
        if j[2] in ['5 H', '5 H(2)']:
            for i in danePlan:
                if (
                    i[1] == dzienTygodniaNazwa
                    and i[0] == j[1]
                ):
                    zmiany.add(
                        (
                            dzienTygodniaNazwa,
                            j[1]
                        )
                    )

                    if j[5] != 'brak':
                        i[2] = j[5]

                    i[3] = j[4]
                    i[4] = j[3]

sciezkaAktualizacji = folder / "data" / "ostatnia_aktualizacja.txt"

ostatniaAktualizacja = datetime.now()

with open(sciezkaAktualizacji, 'w', encoding='utf-8') as plik:
    plik.write(
        ostatniaAktualizacja.strftime("%Y-%m-%d %H:%M")
    )

nazwa = folder / "data" / "strona" / "index.html"
nazwa.parent.mkdir(parents=True, exist_ok=True)

godziny = {
    0: ("07:05", "07:50"),
    1: ("08:00", "08:45"),
    2: ("08:55", "09:40"),
    3: ("09:50", "10:35"),
    4: ("10:45", "11:30"),
    5: ("11:40", "12:25"),
    6: ("12:45", "13:30"),
    7: ("13:40", "14:25"),
    8: ("14:45", "15:30"),
    9: ("15:40", "16:25"),
    10: ("16:35", "17:20"),
    11: ("17:30", "18:15")
}

max_lekcja = max(int(i[0]) for i in danePlan)

ostatniaAktualizacjaTekst = ostatniaAktualizacja.strftime(
    "%d.%m.%Y, %H:%M"
)

dni_wolne = [
    "14 października — Dzień Nauczyciela",
    "31 października - 2 listopada — Wszystkich Świętych",
    "11 listopada — Narodowe Święto Niepodległości",
    "24 grudnia - 6 stycznia — przerwa świąteczna",
    "8 stycznia – dni dyrektorskie",
    "15 lutego - 28 lutego — ferie zimowe",
    "25 marca - 30 marca — wiosenna przerwa świąteczna",
    "14 kwietnia – wystawienie ocen końcowych",
    "30 kwietnia – zakończenie roku szkolnego",
    "4 maja - 7 maja – matury",
    "17 maja – matura informatyka"
]

lista_dni_wolnych = ""

for dzien_wolny in dni_wolne:
    lista_dni_wolnych += f"                <li>{dzien_wolny}</li>\n"

with open(nazwa, 'w', encoding='UTF-8') as plik:
    html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plan 5H</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="naglowek">
        <div class="aktualizacja">
            Zaaktualizowano plan: {ostatniaAktualizacjaTekst}
            Numery dyżurnych: {dyzurny1, dyzurny2}
        </div>
    </div>

    <table>
        <tbody>
            <tr>
                <th>Lekcja</th>
                <th>Godziny</th>
                <th>Poniedziałek</th>
                <th>Wtorek</th>
                <th>Środa</th>
                <th>Czwartek</th>
                <th>Piątek</th>
            </tr>
"""

    licznik = 0
    licznik2 = 0

    html += (
        f'<tr>'
        f'<td>{licznik2}</td>'
        f'<td>{godziny[licznik2][0]} - {godziny[licznik2][1]}</td>'
    )

    for i in range(len(danePlan)):
        for j in range(3):
            if danePlan[i][j + 2] == 'brak' or danePlan[i][j + 2] is None:
                danePlan[i][j + 2] = '&nbsp;'

        numer_lekcji = int(danePlan[i][0])
        dzien = danePlan[i][1]

        start, end = godziny[numer_lekcji]

        klasa = "lekcja"

        if (dzien, danePlan[i][0]) in zmiany:
            klasa += " zmiana"

        if danePlan[i][2] == '&nbsp;':
            html += '<td class="pusta">&nbsp;</td>'
        else:
            html += (
                f'<td class="{klasa}" '
                f'data-day="{dniTygodnia.index(dzien) + 1}" '
                f'data-start="{start}" '
                f'data-end="{end}">'
                f'{danePlan[i][2]}<br>'
                f'{danePlan[i][3]}<br>'
                f'{danePlan[i][4]}'
                f'</td>'
            )

        licznik += 1

        if licznik > 4:
            licznik2 += 1
            html += '</tr>'

            if licznik2 <= max_lekcja:
                html += (
                    '<tr>'
                    f'<td>{licznik2}</td>'
                    f'<td>{godziny[licznik2][0]} - {godziny[licznik2][1]}</td>'
                )

            licznik = 0

    html += f"""</tr>
        </tbody>
    </table>

    <div class="legenda">
        <span class="legenda-item">
            <span class="kolor dzisiaj-kolor"></span>
            Dzisiejszy dzień
        </span>

        <span class="legenda-item">
            <span class="kolor nastepna-kolor"></span>
            Następna lekcja
        </span>

        <span class="legenda-item">
            <span class="kolor aktualna-kolor"></span>
            Aktualna lekcja
        </span>
    </div>

    <div class="odliczanie">
        <div class="timer">
            <div id="gora">
                <span>Odliczanie do najbliższej lekcji:</span>
                <span id="lekcja"></span><br>
            </div>

            <div id="gora">
                <span>Odliczanie do najbliższego weekendu:</span>
                <span id="wolny"></span><br>
            </div>

            <div id="srodek">
                <span>Odliczanie do najbliższego wolnego:</span>
                <span id="wolneDni"></span><br>
            </div>

            <div id="dol">
                <span>Odliczanie do początku matur:</span>
                <span id="matury"></span>
            </div>
        </div>

        <div class="dniWolne">
            <h2>Dni wolne</h2>
            <ul>
{lista_dni_wolnych}            </ul>
        </div>
    </div>

    <script src="./script.js"></script>
</body>
</html>
"""

    plik.write(html)