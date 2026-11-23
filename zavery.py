"""Poslední kontrola žádosti a dva konce. Bez Pygame, jen podmínky a text."""

AKCE_ZAVERU = {"zaver", "opravit_ucel", "ponechat_ucel", "potvrdit_zaver"}


def dialog(nadpis, text, moznosti):
    return {"nadpis": nadpis, "text": text, "moznosti": moznosti}


def konec_pribehu(stav):
    if stav["zaver"] == "povoleno":
        nadpis = "KONEC • Turnaj povolen!"
        text = ("Opravil jsi účel na školní turnaj. Paní Novotná přidává poslední razítko."
                "\n\nVe čtvrtek od 15 do 17 hodin se sál zaplní spolužáky. Turnaj může začít."
                "\n\nPovolení získáno. A tentokrát už žádné další razítko!")
    else:
        nadpis = "KONEC • Razítko nestačilo"
        text = ("Potvrdil jsi soukromou oslavu. Tento účel nesouhlasí se školním poukazem ani žádostí o turnaj."
                "\n\nÚřad povolení zamítl. Samotná rezervace sálu nestačí a turnaj se neuskuteční."
                "\n\nPříště při poslední kontrole oprav účel akce.")
    return dialog(nadpis, text, [("Hrát znovu", "restart"), ("Ukončit hru", "konec")])


def proved_zaver(akce, stav):
    if (stav.get("mistnost", "recepce") != "recepce" or stav["formular"] != 3
            or not all(stav.get(k) for k in ("zaznam", "uctenka", "kontrola", "schvaleno", "termin"))):
        return dialog("Ještě není vše hotové", "Dokonči vyřizování i rezervaci a vrať se k paní Novotné na recepci.", [("Zpět", "zavrit")])
    if akce == "zaver":
        stav.pop("volba_zaveru", None)
        return dialog("Poslední kontrola • A-38", "Paní Novotná: Při přepisu se do žádosti dostal účel SOUKROMÁ OSLAVA. Vy ale pořádáte ŠKOLNÍ TURNAJ."
                      "\n\nPovolím jen akci odpovídající podkladům. Před posledním razítkem údaje zkontrolujte.",
                      [("Opravit na školní turnaj", "opravit_ucel"), ("Ponechat soukromou oslavu", "ponechat_ucel"), ("Ještě neodevzdávat", "zavrit")])
    if akce in ("opravit_ucel", "ponechat_ucel"):
        stav["volba_zaveru"] = "povoleno" if akce == "opravit_ucel" else "zamitnuto"
        text = ("Účel: ŠKOLNÍ TURNAJ. Údaje odpovídají podkladům." if akce == "opravit_ucel" else
                "Účel: SOUKROMÁ OSLAVA. Neodpovídá školnímu poukazu ani původní žádosti. Pokud ji takto odevzdáš, povolení bude zamítnuté.")
        return dialog("Odevzdat konečnou žádost?", text + "\n\nTato volba uzavře příběh.",
                      [("Odevzdat žádost", "potvrdit_zaver"), ("Změnit rozhodnutí", "zaver"), ("Zatím zpět", "zavrit")])
    if stav.get("volba_zaveru") not in ("povoleno", "zamitnuto"):
        return proved_zaver("zaver", stav)
    stav["zaver"] = stav.pop("volba_zaveru")
    return konec_pribehu(stav)
