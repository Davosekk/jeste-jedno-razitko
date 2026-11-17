"""Ještě jedno razítko — jednoduchá 2D adventura v Pythonu a Pygame."""
import math
import pygame
from pribeh import novy_stav, proved, UKOLY, INVENTAR

# 1. NASTAVENÍ: souřadnice jsou v pixelech, rychlost v pixelech za sekundu.
SIRKA, VYSKA = 1152, 720
RYCHLOST = 190
START = (576, 532)
POZADI = "#142529"
SVETLA = "#f1ead5"
ZELENA = "#335d58"
ZLATA = "#e8b274"

PREKAZKY = [
    pygame.Rect(48, 150, 1056, 48), pygame.Rect(48, 150, 16, 450),
    pygame.Rect(1088, 150, 16, 450), pygame.Rect(48, 584, 1056, 16),
    pygame.Rect(136, 280, 136, 60), pygame.Rect(460, 246, 232, 54),
    pygame.Rect(870, 280, 136, 60), pygame.Rect(294, 486, 160, 40),
    pygame.Rect(698, 486, 160, 40), pygame.Rect(84, 206, 40, 42),
    pygame.Rect(1028, 206, 40, 42),
]
PREDMETY = {
    "formulare": ((204, 370), "Formuláře"),
    "urednice": ((576, 330), "Úřednice"),
    "stolek": ((938, 370), "Psací stolek"),
    "nastenka": ((372, 240), "Nástěnka"),
}


# 2. POHYB A KOLIZE: hráč má u nohou malý kolizní obdélník.
def telo(pozice):
    return pygame.Rect(round(pozice.x) - 12, round(pozice.y) - 12, 24, 24)


def posun_hrace(pozice, smer, cas):
    if smer.length() == 0:
        return pozice.copy()
    # Normalizace zabrání rychlejšímu pohybu šikmo.
    posun = smer.normalize() * RYCHLOST * min(cas, 0.05)
    vysledek = pozice.copy()
    # Malé kroky zabrání přeskočení překážky při pomalejším snímku.
    kroku = max(1, math.ceil(posun.length() / 4))
    for _ in range(kroku):
        kandidat = vysledek + pygame.Vector2(posun.x / kroku, 0)
        if not any(telo(kandidat).colliderect(p) for p in PREKAZKY):
            vysledek = kandidat
        kandidat = vysledek + pygame.Vector2(0, posun.y / kroku)
        if not any(telo(kandidat).colliderect(p) for p in PREKAZKY):
            vysledek = kandidat
    return vysledek


def nejblizsi_predmet(pozice):
    nejblizsi = None
    vzdalenost = 70
    for nazev, (bod, popisek) in PREDMETY.items():
        vzd = pozice.distance_to(bod)
        # Úsečka od hráče k předmětu nesmí protínat překážku.
        pres_zed = any(p.clipline(tuple(pozice), bod) for p in PREKAZKY)
        if vzd < vzdalenost and not pres_zed:
            nejblizsi = nazev
            vzdalenost = vzd
    return nejblizsi


# 3. KRESLENÍ: jednoduché tvary, žádné obrázky nebo další editor.
def napis(obraz, text, x, y, velikost=22, barva=SVETLA):
    font = pygame.font.Font(None, velikost)
    obraz.blit(font.render(text, True, barva), (x, y))


def obdelnik(obraz, barva, x, y, sirka, vyska):
    pygame.draw.rect(obraz, barva, (x, y, sirka, vyska))


def stul(obraz, x, y, sirka, popisek):
    obdelnik(obraz, "#b59364", x, y, sirka, 39)
    obdelnik(obraz, "#866849", x, y + 39, sirka, 21)
    napis(obraz, popisek, x + 9, y + 42, 19)


def kresli_kancelar(obraz, stav):
    obdelnik(obraz, "#d6d4bd", 48, 150, 1056, 450)
    for x in range(64, 1088, 48):
        for y in range(198, 584, 48):
            barva = "#dcdbc6" if (x // 48 + y // 48) % 2 else "#d4d3bc"
            obdelnik(obraz, barva, x, y, min(47, 1088-x), min(47, 584-y))
    for zed in PREKAZKY[:4]:
        pygame.draw.rect(obraz, "#3c6765", zed)
    obdelnik(obraz, "#588784", 64, 150, 1024, 38)
    for x in (154, 862):
        obdelnik(obraz, "#bddbd1", x, 160, 144, 31)
        obdelnik(obraz, SVETLA, x + 68, 160, 5, 31)
    obdelnik(obraz, SVETLA, 452, 157, 248, 32)
    napis(obraz, "ODDĚLENÍ POVOLENÍ", 475, 164, 24, POZADI)
    obdelnik(obraz, "#886949", 332, 160, 81, 33)
    for x in (341, 362, 383):
        obdelnik(obraz, SVETLA, x, 166, 15, 20)
    pygame.draw.circle(obraz, SVETLA, (758, 173), 17)
    pygame.draw.lines(obraz, POZADI, False, [(758, 160), (758, 173), (768, 175)], 2)
    obdelnik(obraz, "#31545d", 560, 216, 32, 32)
    pygame.draw.circle(obraz, "#ddae85", (576, 208), 12)
    obdelnik(obraz, "#655449", 564, 196, 24, 9)
    obdelnik(obraz, POZADI, 567, 208, 18, 3)
    stul(obraz, 460, 246, 232, "PŘÍJEM ŽÁDOSTÍ")
    obdelnik(obraz, "#314b50", 484, 234, 46, 29)
    obdelnik(obraz, "#8cb8aa", 488, 238, 38, 20)
    obdelnik(obraz, SVETLA, 612, 253, 30, 21)
    stul(obraz, 136, 280, 136, "FORMULÁŘE")
    if stav["formular"] == 0:
        obdelnik(obraz, SVETLA, 166, 288, 36, 27)
        napis(obraz, "A-38", 169, 296, 15, POZADI)
    stul(obraz, 870, 280, 136, "PSACÍ STOLEK")
    obdelnik(obraz, SVETLA, 893, 287, 37, 27)
    pygame.draw.line(obraz, "#284a65", (945, 289), (955, 308), 4)
    for x in (294, 698):
        for i in range(3):
            obdelnik(obraz, "#4e7771", x + i*54, 486, 50, 40)
            obdelnik(obraz, "#72958a", x + i*54 + 3, 490, 44, 24)
    for x in (104, 1048):
        obdelnik(obraz, "#a77855", x-13, 223, 26, 23)
        pygame.draw.circle(obraz, "#64895b", (x, 220), 20)
    obdelnik(obraz, "#a3ae98", 520, 542, 112, 37)
    napis(obraz, "VSTUP", 547, 552, 22, POZADI)


def kresli_hrace(obraz, pozice):
    x, y = round(pozice.x), round(pozice.y)
    pygame.draw.ellipse(obraz, "#959b87", (x-17, y-2, 34, 12))
    for offset in (-9, 2):
        obdelnik(obraz, "#263944", x+offset, y-5, 7, 10)
    obdelnik(obraz, "#d5854e", x-13, y-27, 26, 24)
    obdelnik(obraz, "#efad70", x-8, y-27, 16, 18)
    for offset in (-16, 11):
        obdelnik(obraz, "#f1c9a0", x+offset, y-24, 5, 17)
    obdelnik(obraz, "#edc399", x-10, y-46, 20, 21)
    obdelnik(obraz, "#49372f", x-11, y-49, 22, 9)
    for offset in (-6, 3):
        obdelnik(obraz, POZADI, x+offset, y-37, 3, 3)


def zalom_text(text, font, sirka):
    radky = []
    for odstavec in text.split("\n"):
        radek = ""
        for slovo in odstavec.split():
            novy = (radek + " " + slovo).strip()
            if radek and font.size(novy)[0] > sirka:
                radky.append(radek)
                radek = slovo
            else:
                radek = novy
        radky.append(radek)
    return radky


def rozlozeni_dialogu(rozhovor):
    radky = zalom_text(rozhovor["text"], pygame.font.Font(None, 25), 620)
    vyska = 108 + len(radky)*29 + len(rozhovor["moznosti"])*50
    panel = pygame.Rect(236, (VYSKA-vyska)//2, 680, vyska)
    tlacitka = []
    for i in range(len(rozhovor["moznosti"])):
        tlacitka.append(pygame.Rect(266, panel.y+82+len(radky)*29+i*50, 620, 42))
    return panel, radky, tlacitka


def kresli_dialog(obraz, rozhovor, vybrano):
    stin = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
    stin.fill((5, 15, 19, 200))
    obraz.blit(stin, (0, 0))
    panel, radky, tlacitka = rozlozeni_dialogu(rozhovor)
    pygame.draw.rect(obraz, SVETLA, panel, border_radius=6)
    napis(obraz, rozhovor["nadpis"], 266, panel.y+25, 32, ZELENA)
    for i, radek in enumerate(radky):
        napis(obraz, radek, 266, panel.y+70+i*29, 25, POZADI)
    for i, tlacitko in enumerate(tlacitka):
        pygame.draw.rect(obraz, ZELENA, tlacitko, border_radius=4)
        if i == vybrano:
            pygame.draw.rect(obraz, ZLATA, tlacitko, 2, border_radius=4)
        napis(obraz, rozhovor["moznosti"][i][0], 280, tlacitko.y+11, 24)


# 4. HLAVNÍ SMYČKA: události -> pohyb -> kreslení -> zobrazení.
def main():
    pygame.display.init()
    pygame.font.init()
    okno = pygame.display.set_mode((SIRKA, VYSKA), pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Ještě jedno razítko — Python 0.1")
    hodiny = pygame.time.Clock()
    stav = novy_stav()
    pozice = pygame.Vector2(START)
    rozhovor = proved("uvod", stav)
    vybrano = 0
    bezi = True

    while bezi:
        cas = hodiny.tick(60) / 1000  # Milisekundy převedeme na sekundy.
        for udalost in pygame.event.get():
            akce = None
            if udalost.type == pygame.QUIT:
                bezi = False
            elif udalost.type == pygame.WINDOWFOCUSLOST:
                if rozhovor is None:
                    rozhovor = proved("pauza", stav)
                    vybrano = 0
            elif rozhovor is not None:
                if udalost.type == pygame.KEYDOWN:
                    if udalost.key == pygame.K_ESCAPE:
                        akce = "zavrit"
                    elif udalost.key in (pygame.K_UP, pygame.K_DOWN):
                        krok = 1 if udalost.key == pygame.K_DOWN else -1
                        vybrano = (vybrano+krok) % len(rozhovor["moznosti"])
                    elif udalost.key in (pygame.K_RETURN, pygame.K_SPACE):
                        akce = rozhovor["moznosti"][vybrano][1]
                elif udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:
                    for i, tlacitko in enumerate(rozlozeni_dialogu(rozhovor)[2]):
                        if tlacitko.collidepoint(udalost.pos):
                            akce = rozhovor["moznosti"][i][1]
                            break
            elif udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_e:
                    akce = nejblizsi_predmet(pozice)
                elif udalost.key == pygame.K_ESCAPE:
                    akce = "pauza"
                elif udalost.key == pygame.K_r:
                    akce = "novy_zacatek"

            if akce == "konec":
                bezi = False
            elif akce == "restart":
                stav = novy_stav()
                pozice = pygame.Vector2(START)
                rozhovor = None
                vybrano = 0
            elif akce is not None:
                rozhovor = proved(akce, stav)
                vybrano = 0

        if rozhovor is None and pygame.key.get_focused():
            klavesy = pygame.key.get_pressed()
            dx = int(klavesy[pygame.K_d] or klavesy[pygame.K_RIGHT]) - int(klavesy[pygame.K_a] or klavesy[pygame.K_LEFT])
            dy = int(klavesy[pygame.K_s] or klavesy[pygame.K_DOWN]) - int(klavesy[pygame.K_w] or klavesy[pygame.K_UP])
            pozice = posun_hrace(pozice, pygame.Vector2(dx, dy), cas)

        okno.fill(POZADI)
        kresli_kancelar(okno, stav)
        kresli_hrace(okno, pozice)
        napis(okno, "JEŠTĚ JEDNO RAZÍTKO", 48, 24, 39)
        napis(okno, "PYTHON • PROTOTYP 0.1", 850, 37, 22, ZLATA)
        napis(okno, "AKTUÁLNÍ ÚKOL", 48, 100, 19, "#94b7ac")
        napis(okno, UKOLY[stav["formular"]], 212, 98, 24)
        napis(okno, "U SEBE", 48, 622, 18, "#94b7ac")
        napis(okno, INVENTAR[stav["formular"]], 48, 646, 25, ZLATA)
        predmet = nejblizsi_predmet(pozice)
        if predmet is not None and rozhovor is None:
            pygame.draw.circle(okno, "#ba883f", PREDMETY[predmet][0], 21, 3)
            napoveda = "E • " + PREDMETY[predmet][1]
        else:
            napoveda = "Přijdi blíž k předmětu nebo úřednici."
        napis(okno, napoveda, 390, 636, 25)
        napis(okno, "WASD / ŠIPKY  pohyb      E  interakce      ESC  pauza      R  nový začátek", 290, 690, 19, "#94b7ac")
        if rozhovor is not None:
            kresli_dialog(okno, rozhovor, vybrano)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
