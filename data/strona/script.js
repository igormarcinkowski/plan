function zaznaczLekcje() {
    const teraz = new Date();
    const dzien = teraz.getDay();
    const aktualnaGodzina = teraz.getHours() * 60 + teraz.getMinutes();

    const lekcje = Array.from(
        document.querySelectorAll(".lekcja")
    );

    lekcje.forEach(lekcja => {
        lekcja.classList.remove("dzisiaj");
        lekcja.classList.remove("aktualna");
        lekcja.classList.remove("nastepna");
    });

    const lekcjeDzisiaj = lekcje.filter(lekcja => {
        return Number(lekcja.dataset.day) === dzien;
    });

    let aktualnaLekcja = null;
    let nastepnaLekcja = null;
    let najblizszyStart = Infinity;

    lekcjeDzisiaj.forEach(lekcja => {
        const [startH, startM] = lekcja.dataset.start
            .split(":")
            .map(Number);

        const [endH, endM] = lekcja.dataset.end
            .split(":")
            .map(Number);

        const start = startH * 60 + startM;
        const end = endH * 60 + endM;

        lekcja.classList.add("dzisiaj");

        if (
            aktualnaGodzina >= start &&
            aktualnaGodzina < end
        ) {
            aktualnaLekcja = lekcja;
        }

        if (
            start > aktualnaGodzina &&
            start < najblizszyStart
        ) {
            nastepnaLekcja = lekcja;
            najblizszyStart = start;
        }
    });

    if (aktualnaLekcja) {
        aktualnaLekcja.classList.add("aktualna");

        if (nastepnaLekcja) {
            nastepnaLekcja.classList.add("nastepna");
        }

        return;
    }

    if (nastepnaLekcja) {
        nastepnaLekcja.classList.add("nastepna");
        return;
    }

    let nastepnyDzien;

    if (dzien >= 1 && dzien <= 4) {
        nastepnyDzien = dzien + 1;
    } else {
        nastepnyDzien = 1;
    }

    let najwczesniejszaLekcja = null;
    let najwczesniejszyStart = Infinity;

    lekcje.forEach(lekcja => {
        const lekcjaDzien = Number(lekcja.dataset.day);

        if (lekcjaDzien !== nastepnyDzien) {
            return;
        }

        const [startH, startM] = lekcja.dataset.start
            .split(":")
            .map(Number);

        const start = startH * 60 + startM;

        if (start < najwczesniejszyStart) {
            najwczesniejszyStart = start;
            najwczesniejszaLekcja = lekcja;
        }
    });

    if (najwczesniejszaLekcja) {
        najwczesniejszaLekcja.classList.add("nastepna");
    }
}

zaznaczLekcje();

setInterval(zaznaczLekcje, 60000);

function formatujCzas(ms) {
    if (ms <= 0) {
        return "00d 00h 00m 00s";
    }

    const sekundy = Math.floor(ms / 1000);

    const dni = Math.floor(sekundy / 86400);
    const godziny = Math.floor((sekundy % 86400) / 3600);
    const minuty = Math.floor((sekundy % 3600) / 60);
    const sek = sekundy % 60;

    return `${dni}d ${String(godziny).padStart(2, "0")}h ` +
           `${String(minuty).padStart(2, "0")}m ` +
           `${String(sek).padStart(2, "0")}s`;
}

function odliczanieDoWeekendu() {
    const teraz = new Date();
    const weekend = new Date(teraz);

    const dniDoSoboty = (6 - teraz.getDay() + 7) % 7;

    weekend.setDate(teraz.getDate() + dniDoSoboty);
    weekend.setHours(0, 0, 0, 0);

    if (teraz.getDay() === 0 || teraz.getDay() === 6) {
        weekend.setDate(weekend.getDate() + 7);
    }

    const pozostalo = weekend - teraz;

    document.getElementById("wolny").textContent =
        formatujCzas(pozostalo);
}

const dniWolne = [
    {
        nazwa: "Dzień Nauczyciela",
        start: new Date(2026, 9, 14, 0, 0, 0),
        koniec: new Date(2026, 9, 15, 0, 0, 0)
    },
    {
        nazwa: "Wszystkich Świętych",
        start: new Date(2026, 9, 31, 0, 0, 0),
        koniec: new Date(2026, 10, 3, 0, 0, 0)
    },
    {
        nazwa: "Narodowe Święto Niepodległości",
        start: new Date(2026, 10, 11, 0, 0, 0),
        koniec: new Date(2026, 10, 12, 0, 0, 0)
    },
    {
        nazwa: "Przerwa świąteczna",
        start: new Date(2026, 11, 24, 0, 0, 0),
        koniec: new Date(2027, 0, 7, 0, 0, 0)
    },
    {
        nazwa: "Dzień dyrektorski",
        start: new Date(2027, 0, 8, 0, 0, 0),
        koniec: new Date(2027, 0, 9, 0, 0, 0)
    },
    {
        nazwa: "Ferie zimowe",
        start: new Date(2027, 1, 15, 0, 0, 0),
        koniec: new Date(2027, 2, 1, 0, 0, 0)
    },
    {
        nazwa: "Wiosenna przerwa świąteczna",
        start: new Date(2027, 2, 25, 0, 0, 0),
        koniec: new Date(2027, 2, 31, 0, 0, 0)
    }
];

function odliczanieDoWolnego() {
    const teraz = new Date();
    let najblizsze = null;

    for (const wolne of dniWolne) {
        if (teraz >= wolne.start && teraz < wolne.koniec) {
            document.getElementById("wolneDni").textContent =
                "WOLNE! " + wolne.nazwa;
            return;
        }

        if (wolne.start > teraz) {
            if (
                najblizsze === null ||
                wolne.start < najblizsze.start
            ) {
                najblizsze = wolne;
            }
        }
    }

    if (najblizsze !== null) {
        const pozostalo = najblizsze.start - teraz;

        document.getElementById("wolneDni").innerHTML =
            "<i><u>"+najblizsze.nazwa +"</u></i>"+ ": " + formatujCzas(pozostalo);
    } else {
        document.getElementById("wolneDni").innerHTML =
            "Brak kolejnych dni wolnych";
    }
}

function odliczanieDoMatur() {
    const teraz = new Date();
    const matury = new Date(2027, 4, 4, 9, 0, 0);
    const pozostalo = matury - teraz;

    const element = document.getElementById("matury");

    if (pozostalo <= 0) {
        element.textContent = "MATURY TRWAJĄ";
        return;
    }

    element.textContent = formatujCzas(pozostalo);
}

function aktualizujTimery() {
    odliczanieDoWeekendu();
    odliczanieDoWolnego();
    odliczanieDoMatur();
}

aktualizujTimery();

setInterval(aktualizujTimery, 1000);

function aktualizujOdliczanieDoLekcji() {
    const element = document.getElementById("lekcja");

    if (!element) {
        return;
    }

    const lekcje = Array.from(
        document.querySelectorAll(".lekcja[data-day][data-start][data-end]")
    );

    if (lekcje.length === 0) {
        element.textContent = "Brak lekcji";
        return;
    }

    const teraz = new Date();
    const dzienTygodnia = teraz.getDay();

    let najblizsza = null;
    let najblizszaData = null;

    for (const lekcja of lekcje) {
        const dzien = Number(lekcja.dataset.day);
        const [godzinaStart, minutaStart] = lekcja.dataset.start.split(":").map(Number);
        const [godzinaKoniec, minutaKoniec] = lekcja.dataset.end.split(":").map(Number);

        let roznicaDni = dzien - dzienTygodnia;

        if (dzienTygodnia === 0) {
            roznicaDni = dzien;
        } else if (dzienTygodnia === 6) {
            roznicaDni = dzien + 1;
        } else if (roznicaDni < 0) {
            roznicaDni += 7;
        }

        const dataStart = new Date(teraz);
        dataStart.setHours(0, 0, 0, 0);
        dataStart.setDate(dataStart.getDate() + roznicaDni);
        dataStart.setHours(godzinaStart, minutaStart, 0, 0);

        const dataKoniec = new Date(dataStart);
        dataKoniec.setHours(godzinaKoniec, minutaKoniec, 0, 0);

        if (dataStart <= teraz && teraz < dataKoniec) {
            element.textContent = "trwa lekcja";
            return;
        }

        if (dataStart > teraz) {
            if (najblizszaData === null || dataStart < najblizszaData) {
                najblizsza = lekcja;
                najblizszaData = dataStart;
            }
        }
    }

    if (najblizsza === null) {
        element.textContent = "Brak kolejnych lekcji";
        return;
    }

    const roznica = najblizszaData - teraz;

    const dni = Math.floor(roznica / 86400000);
    const godziny = Math.floor((roznica % 86400000) / 3600000);
    const minuty = Math.floor((roznica % 3600000) / 60000);
    const sekundy = Math.floor((roznica % 60000) / 1000);

    let tekst = "";

    if (dni > 0) {
        tekst += `${dni}d `;
    }

    tekst += `${String(godziny).padStart(2, "0")}:`;
    tekst += `${String(minuty).padStart(2, "0")}:`;
    tekst += `${String(sekundy).padStart(2, "0")}`;

    element.textContent = tekst;
}

aktualizujOdliczanieDoLekcji();
setInterval(aktualizujOdliczanieDoLekcji, 1000);