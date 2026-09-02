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