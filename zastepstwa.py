import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from datetime import date, datetime, timedelta
import sys

dzisiaj = date.today()
teraz = datetime.now()

if dzisiaj.weekday() == 5:
    sys.exit(0)

if dzisiaj.weekday() == 6 and teraz.hour < 14:
    sys.exit(0)

if dzisiaj.weekday() == 6:
    data_docelowa = dzisiaj + timedelta(days=1)
else:
    data_docelowa = dzisiaj

rok_szkolny = data_docelowa.year if data_docelowa.month >= 8 else data_docelowa.year - 1
pierwszy_dzien = date(rok_szkolny, 8, 31)
tydzien = (data_docelowa - pierwszy_dzien).days // 7 + 1

nazwaFolderu = 'tydzien_' + str(tydzien)

folder = Path(__file__).parent

url = 'https://zastepstwa.zse.bydgoszcz.pl/'

strona = requests.get(url, timeout=30)
strona.raise_for_status()
strona.encoding = 'ISO-8859-2'

zupa = BeautifulSoup(strona.text, 'html.parser')

nauczyciele = zupa.find_all('td', class_='st1')
tr = zupa.find_all('tr')

nobr = zupa.find('nobr')

dni = [
    'poniedziałek',
    'wtorek',
    'środa',
    'czwartek',
    'piątek'
]

dzien_tygodnia = None

if nobr:
    pierwsza_linia = nobr.get_text("\n", strip=True).split("\n")[0]

    for dzien in dni:
        if dzien in pierwsza_linia.lower():
            dzien_tygodnia = str(dni.index(dzien))
            break

if dzien_tygodnia is None:
    raise Exception("Nie udało się znaleźć dnia tygodnia na stronie zastępstw")

if int(dzien_tygodnia) != data_docelowa.weekday():
    raise Exception(
        f"Strona zastępstw dotyczy innego dnia: {dzien_tygodnia}, "
        f"oczekiwano: {data_docelowa.weekday()}"
    )

nazwa = folder / 'data' / nazwaFolderu / f"zastepstwa-{data_docelowa}.json"
nazwa.parent.mkdir(parents=True, exist_ok=True)

if len(tr) > 4:
    nauczycieleLista = []

    for i in nauczyciele:
        nauczycieleLista.append(i.get_text(strip=True))

    for i in range(len(nauczycieleLista)):
        czesci = nauczycieleLista[i].split(' ')

        if len(czesci) >= 2:
            nauczycieleLista[i] = czesci[0][0] + ' ' + czesci[1]

    zastepstwa = []
    licznik = 0
    nauczyciel = None

    tr = zupa.find_all('tr')[1:]
    tymczasowe = []

    for i in tr:
        naglowki = i.find_all('td', class_='st1')
        info = i.find_all(
            'td',
            string=lambda text: text and 'opis' in text
        )

        if naglowki:
            if licznik >= len(nauczycieleLista):
                continue

            nauczyciel = nauczycieleLista[licznik]
            licznik += 1

        if nauczyciel:
            tymczasowe.append(nauczyciel)

            if not naglowki and not info:
                for td in i.find_all('td'):
                    tekst = td.get_text(strip=True)
                    tekst = tekst.replace('\xa0', '').strip()

                    if not tekst:
                        tekst = 'brak'

                    tymczasowe.append(tekst)

        if len(tymczasowe) >= 2:
            tymczasowe[2:3] = tymczasowe[2].split(' - ')
            zastepstwa.append(tymczasowe)

        tymczasowe = []

    with open(nazwa, 'w', encoding='utf-8') as plik:
        json.dump(
            zastepstwa,
            plik,
            ensure_ascii=False,
            indent=4
        )
else:
    with open(nazwa, 'w', encoding='utf-8') as plik:
        json.dump('', plik, ensure_ascii=False)