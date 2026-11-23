"""Rezervační hádanka: tři zdroje informací a 27 možných návrhů."""

PODKLADY = {
    "skola": ("recepce", "Požadavky školy",
        "Turnaj: 48 účastníků. V pátek je celá škola na exkurzi.\n\nProgram: 3 zápasy po 25 minutách, dvě přestávky po 10 minutách a 25 minut přípravy. Rezervuj přesně délku celého programu."),
    "rozpis": ("archiv", "Rozpis sálu",
        "ÚTERÝ: kapacita 40 osob, bez rezervací.\nČTVRTEK: kapacita 60 osob, obsazeno 14:00–15:00 a 17:00–18:00.\nPÁTEK: kapacita 60 osob, bez rezervací.\n\nNová akce smí začít přesně po konci jiné a skončit přesně před začátkem další."),
    "spravce": ("kancelar", "Dostupnost správce",
        "ÚTERÝ a ČTVRTEK: 14:00–18:00.\nPÁTEK: 14:00–17:00.\n\nSprávce musí být přítomný po celou rezervaci včetně přípravy. Zvol den, začátek a délku na rezervačním terminálu dole v kanceláři."),
}
DNY = {"den_ut": "Úterý", "den_ct": "Čtvrtek", "den_pa": "Pátek"}
CASY = {"cas_14": 14, "cas_15": 15, "cas_16": 16}
DELKY = {"delka_90": 90, "delka_120": 120, "delka_150": 150}
AKCE_REZERVACE = set(PODKLADY) | set(DNY) | set(CASY) | set(DELKY) | {
    "rezervace", "vyber_den", "vyber_cas", "vyber_delku", "odeslat_termin", "poznamky"
}


def dialog(nadpis, text, moznosti):
    return {"nadpis": nadpis, "text": text, "moznosti": moznosti}


def over_termin(den, zacatek, delka):
    """Vrátí důvod zamítnutí. Prázdný text znamená platnou rezervaci."""
    if den not in DNY.values() or zacatek not in CASY.values() or delka not in DELKY.values():
        return "Doplň všechny tři části návrhu: den, začátek a délku."
    if delka != 3 * 25 + 2 * 10 + 25:
        return "Délka neodpovídá celému programu školy. Započítej i přípravu a přestávky."
    if den == "Pátek":
        return "Termín odporuje programu školy. Znovu projdi školní požadavky."
    if den == "Úterý":
        return "Kapacita sálu nestačí pro všechny účastníky."
    konec = zacatek + delka / 60
    zavira = 17 if den == "Pátek" else 18
    if zacatek < 14 or konec > zavira:
        return "Správce není přítomný po celou dobu."
    obsazeno = [(14, 15), (17, 18)] if den == "Čtvrtek" else []
    for od, do in obsazeno:
        if zacatek < do and konec > od:
            return "Rezervace se překrývá s jinou akcí. Porovnej oba konce časového úseku."
    return ""


def proved_rezervaci(akce, stav):
    zpet = [("Zpět", "zavrit")]
    if not stav.get("schvaleno"):
        return dialog("Rezervace zatím uzavřená", "Nejdřív dokonči poplatek, kontrolní stanoviště a získej Dvořákovo razítko.", zpet)
    mistnost = stav.get("mistnost", "recepce")
    if akce in PODKLADY:
        kde, nadpis, text = PODKLADY[akce]
        if mistnost != kde:
            return dialog("Mimo dosah", "K této informační tabuli musíš dojít.", zpet)
        stav["info_" + akce] = True
        return dialog(nadpis, text + "\n\nÚdaje máš zapsané v poznámkách terminálu.", zpet)
    if mistnost != "kancelar":
        return dialog("Mimo dosah", "Rezervační terminál je ve schvalovací kanceláři.", zpet)
    if akce == "poznamky":
        # Prohlíží se jen nalezené podklady; k novým je nutné dojít.
        moznosti = [(PODKLADY[k][1], "poznamka_" + k) for k in PODKLADY if stav.get("info_" + k)]
        return dialog("Moje poznámky", "Vyber nalezený podklad. Můžeš se k němu kdykoliv vrátit.", moznosti + [("Zpět k návrhu", "rezervace")])
    if akce.startswith("poznamka_"):
        klic = akce.removeprefix("poznamka_")
        if stav.get("info_" + klic):
            _, nadpis, text = PODKLADY[klic]
            return dialog(nadpis, text, [("Zpět do poznámek", "poznamky")])
        return dialog("Podklad chybí", "Nejdřív najdi původní tabuli.", zpet)
    if stav.get("termin"):
        return dialog("Termín už je rezervovaný", "Čtvrtek 15:00–17:00. Rezervace je připojená k žádosti. Vrať se spodními dveřmi na recepci k paní Novotné pro poslední kontrolu a povolení.", zpet)
    if akce == "rezervace":
        chybi = [PODKLADY[k][1] for k in PODKLADY if not stav.get("info_" + k)]
        if chybi:
            return dialog("Chybějí podklady", "Najdi tři tabule: ŠKOLA na recepci, ROZPIS za mříží v archivu a SPRÁVCE v kanceláři.\n\nJeště chybí: " + ", ".join(chybi), [("Moje poznámky", "poznamky"), ("Zpět", "zavrit")])
        return dialog("Rezervace • návrh", "Den: " + str(stav.get("navrh_den", "—")) + "\nZačátek: " + str(stav.get("navrh_cas", "—")) + " h\nDélka: " + str(stav.get("navrh_delka", "—")) + " minut\n\nSlaď program, kapacitu, obsazenost a přítomnost správce.", [("Vybrat / změnit návrh", "vyber_den"), ("Odeslat návrh", "odeslat_termin"), ("Moje poznámky", "poznamky"), ("Zpět", "zavrit")])
    if not all(stav.get("info_" + k) for k in PODKLADY):
        return proved_rezervaci("rezervace", stav)
    if akce in DNY:
        stav["navrh_den"] = DNY[akce]
        akce = "vyber_cas"
    if akce in CASY:
        stav["navrh_cas"] = CASY[akce]
        akce = "vyber_delku"
    if akce in DELKY:
        stav["navrh_delka"] = DELKY[akce]
        return proved_rezervaci("rezervace", stav)
    if akce == "vyber_den":
        return dialog("1 / 3 • Den turnaje", "Který den vyhovuje všem podkladům?", [(v, k) for k, v in DNY.items()] + [("Zpět", "rezervace")])
    if akce == "vyber_cas":
        return dialog("2 / 3 • Začátek", "Začátek rezervace zahrnuje také přípravu.", [(str(v) + ":00", k) for k, v in CASY.items()] + [("Zpět", "vyber_den")])
    if akce == "vyber_delku":
        return dialog("3 / 3 • Délka", "Spočítej celý program v minutách.", [(str(v) + " minut", k) for k, v in DELKY.items()] + [("Zpět", "vyber_cas")])
    if akce == "odeslat_termin":
        chyba = over_termin(stav.get("navrh_den"), stav.get("navrh_cas"), stav.get("navrh_delka"))
        if chyba:
            return dialog("Návrh vrácen k opravě", chyba + "\n\nDosavadní dokumenty i hotové hádanky ti zůstávají.", [("Opravit návrh", "vyber_den"), ("Moje poznámky", "poznamky"), ("Zpět", "zavrit")])
        stav["termin"] = True
        return proved_rezervaci("rezervace", stav)
    raise ValueError("Neznámá rezervační akce: " + akce)


AKCE_REZERVACE.update("poznamka_" + k for k in PODKLADY)
