"""Dvě nové místnosti. Seznam obdélníků tvoří nábytek a pevné překážky."""
import pygame

ZDI = [(48, 150, 1056, 48), (48, 150, 16, 450),
       (1088, 150, 16, 450), (48, 584, 1056, 16)]
MRIZ = (850, 198, 20, 386)
MAPY = {
    "archiv": {
        "nazev": "2 / 3 • ARCHIV", "barva": "#c8c8b7",
        # Střídavé mezery mezi regály vytvářejí průchozí cestu.
        "prekazky": [(280, 198, 54, 242), (450, 350, 54, 234),
                     (760, 198, 54, 242), (940, 225, 96, 48)],
        "predmety": {"recepce": ((576, 550), "Zpět na recepci"),
                     "kartoteka": ((990, 305), "Kartotéka sálu"),
                     "rozpis": ((990, 470), "Rozpis sálu"),
                     "pokyny": ((140, 500), "Pokyny k mříži"),
                     "cerveny": ((180, 250), "Červený spínač"),
                     "modry": ((600, 250), "Modrý spínač"),
                     "zeleny": ((650, 490), "Zelený spínač")},
    },
    "kancelar": {
        "nazev": "3 / 3 • SCHVALOVÁNÍ", "barva": "#c5d1c5",
        "prekazky": [(360, 395, 420, 35), (180, 275, 560, 35),
                     (880, 215, 152, 55), (120, 480, 140, 40)],
        "predmety": {"recepce": ((576, 550), "Zpět na recepci"),
                     "schvaleni": ((955, 307), "Pan Dvořák"),
                     "tabule": ((310, 520), "Postup kontrol"),
                     "spravce": ((770, 235), "Dostupnost správce"),
                     "rezervace": ((710, 510), "Rezervační terminál"),
                     "pokladna": ((870, 500), "Pokladna"),
                     "evidence": ((150, 360), "Evidence"),
                     "pecet": ((930, 370), "Pečeť"),
                     "podpis": ((460, 235), "Podpis")},
    },
}


def aktivni_mapa(stav, prekazky_recepce, predmety_recepce):
    mistnost = stav.get("mistnost", "recepce")
    if mistnost == "recepce":
        predmety = dict(predmety_recepce)
        predmety.update({"skola": ((600, 420), "Požadavky školy"),
                         "archiv": ((105, 430), "Dveře do archivu"),
                         "kancelar": ((1045, 430), "Schvalovací kancelář")})
        return prekazky_recepce, predmety
    mapa = MAPY[mistnost]
    prekazky = [pygame.Rect(r) for r in ZDI + mapa["prekazky"]]
    if mistnost == "archiv" and not stav.get("mriz"):
        prekazky.append(pygame.Rect(MRIZ))
    return prekazky, mapa["predmety"]


def kresli_mistnost(obraz, stav, napis):
    mistnost = stav.get("mistnost", "recepce")
    if mistnost == "recepce":
        for x, text, otevreno in [(78, "ARCHIV", stav["formular"] == 3),
                                  (1018, "KANCELÁŘ", stav.get("zaznam"))]:
            pygame.draw.rect(obraz, "#497f66" if otevreno else "#9c604d", (x, 390, 54, 75))
            napis(obraz, "E", x+20, 415, 28)
            napis(obraz, text, x-5, 470, 16, "#142529")
        pygame.draw.circle(obraz, "#36575e", (600, 420), 18)
        napis(obraz, "E", 594, 410, 22)
        napis(obraz, "ŠKOLA", 577, 444, 16, "#142529")
        return
    mapa = MAPY[mistnost]
    pygame.draw.rect(obraz, mapa["barva"], (48, 150, 1056, 450))
    for r in ZDI:
        pygame.draw.rect(obraz, "#3c6765", r)
    for x, y, w, h in mapa["prekazky"]:
        pygame.draw.rect(obraz, "#846e51", (x, y, w, h))
        pygame.draw.rect(obraz, "#b19770", (x+4, y+4, w-8, h-8))
        if mistnost == "archiv" and h > 60:
            for yy in range(y+12, y+h-10, 28):
                pygame.draw.line(obraz, "#485c58", (x+8, yy), (x+w-8, yy), 6)
    napis(obraz, mapa["nazev"], 390, 163, 26)
    pygame.draw.rect(obraz, "#497f66", (536, 536, 80, 42))
    napis(obraz, "ZPĚT", 550, 547, 22)
    if mistnost == "archiv":
        napis(obraz, "SÁL", 955, 238, 20, "#142529")
    else:
        pygame.draw.circle(obraz, "#ddae85", (955, 208), 12)
        napis(obraz, "DVOŘÁK", 902, 236, 20, "#142529")

    # Stanoviště jsou na podlaze, takže hráče nemohou uvěznit při aktivaci.
    barvy = {"cerveny": "#bd5144", "modry": "#467caf", "zeleny": "#398a5b"}
    nazvy = {"rozpis": "ROZPIS", "spravce": "SPRÁVCE", "rezervace": "REZERVACE", "pokyny": "POKYNY", "tabule": "POSTUP", "pokladna": "POKLADNA",
             "evidence": "EVIDENCE", "pecet": "PEČEŤ", "podpis": "PODPIS",
             "cerveny": "ČERVENÝ", "modry": "MODRÝ", "zeleny": "ZELENÝ"}
    for akce, ((x, y), _) in mapa["predmety"].items():
        if akce in nazvy:
            pygame.draw.circle(obraz, barvy.get(akce, "#36575e"), (x, y), 18)
            napis(obraz, "E", x-6, y-10, 22)
            napis(obraz, nazvy[akce], x-38, y+22, 16, "#142529")
    if mistnost == "archiv":
        if not stav.get("mriz"):
            pygame.draw.rect(obraz, "#34494c", MRIZ)
            for y in range(205, 580, 24):
                pygame.draw.line(obraz, "#b4c6c5", (850, y), (870, y), 3)
        napis(obraz, "SPÍNAČE " + str(stav.get("spinace", 0)) + "/4", 650, 163, 20)
    else:
        napis(obraz, "KONTROLA " + str(stav.get("stanoviste", 0)) + "/3", 760, 163, 20)
