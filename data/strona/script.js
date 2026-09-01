function zaznaczLekcje() {
    const teraz = new Date();
    const dzien = teraz.getDay();
    const aktualnaGodzina = teraz.getHours() * 60 + teraz.getMinutes();

    document.querySelectorAll(".lekcja").forEach(lekcja => {
        const lekcjaDzien = Number(lekcja.dataset.day);

        const [startH, startM] = lekcja.dataset.start.split(":").map(Number);
        const [endH, endM] = lekcja.dataset.end.split(":").map(Number);

        const start = startH * 60 + startM;
        const end = endH * 60 + endM;

        lekcja.classList.remove("dzisiaj");
        lekcja.classList.remove("aktualna");

        if (lekcjaDzien === dzien) {
            lekcja.classList.add("dzisiaj");

            if (aktualnaGodzina >= start && aktualnaGodzina < end) {
                lekcja.classList.add("aktualna");
            }
        }
    });
}

zaznaczLekcje();

setInterval(zaznaczLekcje, 60000);