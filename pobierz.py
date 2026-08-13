from pathlib import Path
from datetime import date
import json
folder = Path(__file__).parent
nazwaPlan = 'Plan-'+str(date.today())+'.json'
nazwaZastepstwa = 'Zastepstwa-'+str(date.today())+'.json'
sciezkaPlan = folder / 'data' / 'plan' / nazwaPlan
sciezkaZastepstwa = folder / 'data' / 'zastepstwa' / nazwaZastepstwa    
dzienTygodnia = folder / 'data' / 'zastepstwa' / 'pomoc.txt'

with open(sciezkaPlan, 'r', encoding='utf-8') as plan, open(sciezkaZastepstwa, 'r', encoding='utf-8') as zastepstwa, open(dzienTygodnia, 'r') as PlikdzienTygodnia:
    danePlan = json.load(plan)
    daneZastepstwa = json.load(zastepstwa)
    for wiersz in PlikdzienTygodnia:
        dzienTygodnia=int(wiersz)
    zmiany=[]
    for i in range(len(daneZastepstwa)):
        if daneZastepstwa[i][2] in ['4 H', '4 H(2)']:
            zmiany.append(daneZastepstwa[i])
    dniTygodnia = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']
    dzienTygodniaNazwa = dniTygodnia[dzienTygodnia]
    for i in danePlan:
        for j in zmiany:
            if i[1] == dzienTygodniaNazwa and i[0] == j[1]:
                i[2] = j[5]
                i[3] = j[4]
                i[4] = j[3]
folder = Path(__file__).parent
nazwa = folder / "data" / "strona" / "index.html"
nazwa.parent.mkdir(parents=True, exist_ok=True)
with open(nazwa, 'w', encoding='utf-8') as plik:
    html="""<!DOCTYPE html>
<html lang="en">
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
                
                <th>Poniedziałek</th>
                <th>Wtorek</th>
                <th>Środa</th>
                <th>Czwartek</th>
                <th>Piątek</th>
            </tr>"""
    licznik=0
    licznik2=0
    html+="<td>"+str(licznik2)+"</td>"
    for i in range(len(danePlan)):
        for j in range(3):
            if danePlan[i][j+2] == 'brak' or danePlan[i][j+2] == None:
                danePlan[i][j+2] = '&nbsp;'
        html+="<td>"+str(danePlan[i][2])+"<br>"+str(danePlan[i][3])+"<br>"+str(danePlan[i][4])+"<br>"+"</td>"
        licznik+=1
        if licznik>4:
            licznik2+=1
            html+="</tr><tr>"
            if licznik2-1<int(danePlan[-1][0]):
                html+="<td>"+str(licznik2)+"</td>"
            licznik=0
    html+= """</tr>
</tbody>
</table>
</body>
</html>"""
    plik.write(html)