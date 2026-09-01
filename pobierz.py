from pathlib import Path
from datetime import date
import json

folder = Path(__file__).parent

nazwaPlan = 'Plan-' + str(date.today()) + '.json'
nazwaZastepstwa = 'Zastepstwa-' + str(date.today()) + '.json'

sciezkaPlan = folder / 'data' / 'plan' / nazwaPlan
sciezkaZastepstwa = folder / 'data' / 'zastepstwa' / nazwaZastepstwa
dzienTygodnia = folder / 'data' / 'zastepstwa' / 'pomoc.txt'

with open(sciezkaPlan, 'r', encoding='utf-8') as plan, \
     open(sciezkaZastepstwa, 'r', encoding='utf-8') as zastepstwa, \
     open(dzienTygodnia, 'r', encoding='utf-8') as PlikdzienTygodnia:

    danePlan = json.load(plan)
    daneZastepstwa = json.load(zastepstwa)

    for wiersz in PlikdzienTygodnia:
        dzienTygodnia = int(wiersz)

    zmiany = []

    for i in range(len(daneZastepstwa)):
        if daneZastepstwa[i][2] in ['5 H', '5 H(2)']:
            zmiany.append(daneZastepstwa[i])

    dniTygodnia = [
        'Poniedziałek',
        'Wtorek',
        'Środa',
        'Czwartek',
        'Piątek'
    ]

    dzienTygodniaNazwa = dniTygodnia[dzienTygodnia]

    for i in danePlan:
        for j in zmiany:
            if i[1] == dzienTygodniaNazwa and i[0] == j[1]:
                if j[5] != 'brak':
                    i[2] = j[5]
                i[3] = j[4]
                i[4] = j[3]

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

with open(nazwa, 'w', encoding='utf-8') as plik:
    html = """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Plan 4H</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
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

        html += (
            f'<td class="lekcja" '
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

            if licznik2 <= int(danePlan[-1][0]):
                html += (
                    '<tr>'
                    f'<td>{licznik2}</td>'
                    f'<td>{godziny[licznik2][0]} - {godziny[licznik2][1]}</td>'
                )

            licznik = 0

    html += """</tr>
        </tbody>
    </table>
    <script src="./script.js"></script>
</body>
</html>
"""

    plik.write(html)