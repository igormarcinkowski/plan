import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from datetime import date

folder = Path(__file__).parent
nazwa = folder / 'data' / 'zastepstwa' / f"Zastepstwa-{date.today()}.json"
nazwa2 = folder / 'data' / 'zastepstwa' / "pomoc.txt"
nazwa.parent.mkdir(parents=True, exist_ok=True)

# url = 'https://zastepstwa.zse.bydgoszcz.pl/'
url = 'https://web.archive.org/web/20240913055040/https://zastepstwa.zse.bydgoszcz.pl/'

strona = requests.get(url, timeout=30)
strona.raise_for_status()
strona.encoding = 'ISO-8859-2'
zupa = BeautifulSoup(strona.text, 'html.parser')
tabela = zupa.find_all('table')
nauczyciele = zupa.find_all('td', class_='st1')
nauczycieleLista=[]
tr = zupa.find_all('tr')

nobr = zupa.find('nobr')
dni = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek']
dzien_tygodnia = None
if nobr:
    pierwsza_linia = nobr.get_text("\n", strip=True).split("\n")[0]
    for dzien in dni:
        if dzien in pierwsza_linia.lower():
            dzien_tygodnia = str(dni.index(dzien))
            break
if dzien_tygodnia is None:
    raise Exception("Nie udało się znaleźć dnia tygodnia na stronie zastępstw")

if len(tr)>4:
    licznik=0
    for i in nauczyciele:
        nauczycieleLista.append(i.get_text(strip=True))
        licznik+=1
    for i in range(len(nauczycieleLista)):
        pomoc=''
        pomoc=str(nauczycieleLista[i].split(' ')[0][0]) + ' ' + str(nauczycieleLista[i].split(' ')[1])
        nauczycieleLista[i]=pomoc

    godziny=[]
    for i in nauczyciele:
        godziny.append([i.get_text(strip=True)])
    # for i in godziny:
    #     print(i)

    wiersze = zupa.find_all('tr')

    informacje = zupa.find('td', class_='st0')

    zastepstwa=[]
    licznik=0
    nauczyciel=None

    tr = zupa.find_all('tr')[1:]
    tymczasowe=[]
    for i in tr:
        przerwa = i.find_all('td', class_='st15')
        naglowki = i.find_all('td', class_='st1')
        info = i.find_all('td', string=lambda text: 'opis' in text)
        if naglowki:
            nauczyciel = nauczycieleLista[licznik]
            licznik+=1
        if nauczyciel:
            tymczasowe.append(nauczyciel)
            if not naglowki and not przerwa and not info:
                for td in i.find_all('td'):
                    tekst = td.get_text(strip=True).replace('\xa0', '').strip()
                    if not tekst:
                        tekst = 'brak'
                    tymczasowe.append(tekst)
        if not len(tymczasowe)<2:
            tymczasowe[2:3] = tymczasowe[2].split(' - ')
            zastepstwa.append(tymczasowe)
        tymczasowe=[]

    with open(nazwa, 'w', encoding='utf-8') as plik, open(nazwa2, 'w') as dzienTygodnia:
        plik.write(json.dumps(zastepstwa, ensure_ascii=False, indent=4))
        dzienTygodnia.write(dzien_tygodnia)
else:
    zastepstwa=''
    with open(nazwa, 'w', encoding='utf-8') as plik, open(nazwa2, 'w') as dzienTygodnia:
            plik.write(json.dumps(zastepstwa, ensure_ascii=False, indent=4))
            dzienTygodnia.write(dzien_tygodnia)