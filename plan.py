import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from pathlib import Path

url = 'https://plan.zse.bydgoszcz.pl/plany/o29.html'
response = requests.get(url, timeout=30)
response.raise_for_status()
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')
plan = soup.find('table', class_= 'tabela')

nauczyciele = {
    "Ch": "M Chabowski",
    "dA": "A Sumicka",
    "Md": "D Musierowicz",
    "Sm": "Z Smutek",
    "Js": "S Janeczek",
    "Bm": "M Bzdawka",
    "An": "P Augustyn",
    "Br": "M Baranowska",
    "Bt": "D Bartkowska",
    "Bd": "K Bednarek",
    "Bk": "K Beszczyński",
    "Bo": "R Borowczyk",
    "Cm": "M Chełmińska",
    "Ck": "M Cierzniakowska",
    "Ci": "T Ciżmowski",
    "CA": "A Czarnecka",
    "Cj": "J Czerniak",
    "Cz": "M Czeszewska",
    "Cd": "D Czyżewski",
    "Dm": "A Dembczyńska",
    "Do": "Ł Dolski",
    "Di": "I Dziemitko",
    "Gw": "A Gałdecka-Wysk",
    "Gł": "K Gałek-Stachura",
    "MG": "M Geruzel",
    "Gi": "D Gierczak-Pliszka",
    "Gz": "D Gozdur-Kolendo",
    "Gb": "K Grabska",
    "Gj": "A Grajek",
    "Gc": "A Gralak",
    "Hr": "W Hermanowski",
    "Jz": "Z Jakubiak",
    "Ja": "T Janka",
    "Kn": "M Kantorska",
    "Kg": "G Kantowicz",
    "Kj": "J Karolkiewicz",
    "KD": "P Kiedrowski",
    "Ko": "K Kołodziejski",
    "Kc": "W Korput",
    "Kt": "R Korytek",
    "Re": "K Kosecka",
    "Ad": "A Kowalczewski",
    "Śc": "I Kowalska",
    "Kr": "R Krzemiński",
    "Go": "G Kubiak",
    "Wd": "M Kucharska",
    "Ku": "H Kulczewska",
    "Kp": "P Kulpa",
    "Jk": "J Kuźba",
    "PL": "P Leda",
    "AL": "A Leszczyńska",
    "Le": "L Lewandowska",
    "Ła": "E Łabuńska",
    "AM": "A Mordaka-Markiewicz",
    "No": "A Nowak",
    "RO": "R Owczarzak",
    "Pw": "R Pacewicz",
    "Pa": "M Pawłowska",
    "Pe": "G Piekarz",
    "Pń": "E Pieńkosz-Kumor",
    "Pi": "A Piłat",
    "Po": "T Poćwiardowski",
    "Ra": "R Rajkowska",
    "Rs": "M Reszkowska",
    "Ry": "M Rybacka",
    "Se": "W Sempowicz",
    "Vf": "S Sędalska",
    "Sd": "S Sidor",
    "Sg": "J Siegert",
    "Sp": "J Siepniewska-Stańczyk",
    "Sc": "A Sieracki",
    "So": "A Skotnicka-Maciak",
    "Sn": "K Smoleń",
    "St": "P Stachura",
    "Pm": "M Staśkiewicz",
    "Sh": "A Szlachciak",
    "RŚ": "R Śmidoda",
    "Ta": "K Tabor",
    "To": "M Tomczak",
    "Tj": "J Torzecka",
    "Tr": "J Truszkowski",
    "TZ": "A Trzciński",
    "TL": "J Tylicki",
    "Wm": "M Wilczyńska",
    "Wl": "S Wilczyński",
    "dW": "R Wojciechowaki",
    "Wo": "M Wojtecka-Ratajczak",
    "Wu": "D Wojtuń",
    "Wj": "K Wójcik-Wasilewska",
    "Wr": "D Wróblewska",
    "Ws": "A Wrzesień",
    "Ze": "M Zelek",
    "Ie": "I.Vacat",
    "Ia": "I.Vacat",
    "Ib": "I.Vacat",
    "BV": "t.Vacat tech"
}
licznik=0
wiersze = plan.find_all('tr')[1:]
dane=[]
dni = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']
for wiersz in wiersze:
    # godzina = wiersz.find('td', class_='g').get_text()
    numer = wiersz.find('td', class_='nr').get_text()
    lekcje = wiersz.find_all('td', class_='l')
    for dzien in range(5):
        dzieńTygodnia = dni[dzien]
        br = lekcje[dzien].find("br")
        if br:
            lekcje[dzien] = br.find_next_sibling()
        span = lekcje[dzien].find("span", class_="p")
        lekcja = span.get_text(strip=True) if span else "brak"
        if lekcja[-3:]=='1/2':
            lekcja='brak'
        nauczyciel=lekcje[dzien].find('a', class_='n')
        if nauczyciel:
            nauczyciel=nauczyciel.get_text()
            if nauczyciel not in nauczyciele.keys():
                nauczyciel='-'
            else:
                nauczyciel=nauczyciele[nauczyciel]
        sala=lekcje[dzien].find('a', class_='s')
        if sala:
            sala=sala.get_text()
        if lekcja=='brak' or nauczyciel==None or lekcja[:7]=='religia':
            lekcja='brak'
            nauczyciel='brak'
            sala='brak'
        if lekcja[:2] == 'wf':
            lekcja='wf'
        if lekcja=='brak' and nauczyciel=='brak' and sala=='brak':
            licznik+=1
        dane.append([numer, dzieńTygodnia, lekcja, nauczyciel, sala])
        if licznik==5:
            for i in range(5):
                dane.pop(-1)

    licznik=0
folder = Path(__file__).parent
nazwa = folder / 'data' / 'plan' / f"Plan-{date.today()}.json"
nazwa.parent.mkdir(parents=True, exist_ok=True)
with open(nazwa, 'w', encoding='utf-8') as plik:
    plik.write(json.dumps(dane, ensure_ascii=False, indent=4))