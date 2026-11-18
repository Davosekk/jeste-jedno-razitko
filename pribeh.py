"""Příběh a pravidla hry. Tento soubor nepotřebuje Pygame."""


def novy_stav():
    # 0 = nemám formulář, 1 = prázdný, 2 = podepsaný, 3 = odevzdaný
    return {"formular": 0}


def dialog(nadpis, text, moznosti):
    # Každá možnost obsahuje popisek tlačítka a název další akce.
    return {"nadpis": nadpis, "text": text, "moznosti": moznosti}


def proved(akce, stav):
    """Zpracuje rozhodnutí hráče a vrátí další dialog. None znamená zavřít."""
    formular = stav["formular"]
    if akce == "zavrit":
        return None
    if akce == "uvod":
        return dialog("Ještě jedno razítko", "Vaše třída chystá školní turnaj. Potřebuješ povolení z úřadu.\n\nNajdi správný formulář, vyplň ho a předej úřednici. Potom prozkoumej archiv a schvalovací kancelář.", [("Vstoupit na úřad", "zavrit")])
    if akce == "pauza":
        return dialog("Pauza", "Úřední kolečko může chvíli počkat.", [("Pokračovat", "zavrit"), ("Začít znovu", "restart"), ("Ukončit hru", "konec")])
    if akce == "novy_zacatek":
        return dialog("Začít znovu?", "Obnoví se hráč i všechny dokumenty.", [("Zpět do hry", "zavrit"), ("Ano, začít znovu", "restart")])
    if akce == "urednice":
        if formular == 3:
            return dialog("Paní Novotná", "Žádost je přijatá. Odemkla jsem vám archiv vlevo. Najděte záznam o sálu a odneste ho do kanceláře vpravo.", [("Zpět", "zavrit"), ("Zkusit znovu", "restart")])
        return dialog("Paní Novotná • příjem žádostí", "Dobrý den. Co potřebujete vyřídit?", [("Co potřebuji na školní turnaj?", "napoveda"), ("Chci odevzdat žádost", "odevzdat"), ("Na shledanou", "zavrit")])
    if akce == "napoveda":
        return dialog("Nejdřív správný formulář", "Na turnaj potřebujete A-38. Vlevo si jej vezměte, vpravo vyplňte a podepište. Potom ho přineste sem.", [("Děkuji", "zavrit")])
    if akce == "nastenka":
        return dialog("Pokyny pro žadatele", "POŘÁDÁNÍ AKCÍ — FORMULÁŘ A-38\n\n1. Vyzvedni formulář vlevo.\n2. Vyplň jej a podepiš u stolku vpravo.\n3. Předej jej na přepážce příjmu.\n\nNeúplné žádosti se vracejí k doplnění.", [("Přečteno", "zavrit")])
    if akce == "formulare":
        if formular != 0:
            return dialog("Formuláře", "A-38 už máš nebo je odevzdaný. Další kus nepotřebuješ.", [("Zpět", "zavrit")])
        return dialog("Zásobník formulářů", "Ve stojanu jsou dvě žádosti. Která patří ke školnímu turnaji?", [("A-38 • pořádání akcí", "sebrat"), ("B-17 • parkovací oprávnění", "spatny"), ("Nechat být", "zavrit")])
    if akce == "spatny":
        return dialog("Jiná žádost", "B-17 je parkovací oprávnění. Na turnaj se nehodí, vrátíš ho do stojanu.", [("Vybrat znovu", "formulare"), ("Zpět", "zavrit")])
    if akce == "sebrat":
        if formular != 0:
            return proved("formulare", stav)
        stav["formular"] = 1
        return dialog("Získáno: A-38", "Máš prázdný formulář. Vyplň ho u psacího stolku vpravo.", [("Pokračovat", "zavrit")])
    if akce == "stolek":
        if formular == 0:
            text = "Pero tu je, ale nemáš co vyplnit. Nejdřív si vlevo vezmi formulář."
        elif formular == 1:
            return dialog("Psací stolek", "Doplníš název akce, organizátora a podpis.", [("Vyplnit a podepsat A-38", "vyplnit"), ("Zatím ne", "zavrit")])
        else:
            text = "Formulář už je vyplněný. Další podpis není potřeba."
        return dialog("Psací stolek", text, [("Zpět", "zavrit")])
    if akce == "vyplnit":
        if formular != 1:
            return proved("stolek", stav)
        stav["formular"] = 2
        return dialog("Vyplněno a podepsáno", "Akce: školní turnaj.\nOrganizátor: vaše třída.\nPodpis: doplněn.\n\nOdnes žádost úřednici.", [("Pokračovat", "zavrit")])
    if akce == "odevzdat":
        if formular == 0:
            return dialog("Něco chybí", "Žádost nemáte. Formulář A-38 je vlevo ve stojanu.", [("Dojdu pro něj", "zavrit")])
        if formular == 1:
            return dialog("Vráceno k doplnění", "Chybí údaje a podpis. Vyplňte je u stolku vpravo. Formulář ti zůstává.", [("Doplním údaje", "zavrit")])
        if formular == 2:
            stav["formular"] = 3
        return dialog("První úkol hotový!", "Žádost byla přijatá. Našel jsi správný formulář, vyplnil ho a odevzdal.\n\nÚřednice odemyká archiv vlevo. Najdi tam záznam o sálu; s ním tě pustí do kanceláře vpravo.", [("Ještě se projít", "zavrit"), ("Hrát od začátku", "restart")])
    if akce == "archiv":
        if formular < 3:
            return dialog("Zamčený archiv", "Nejdřív odevzdej vyplněnou žádost. Úřednice potom odemkne archiv.", [("Zpět", "zavrit")])
        stav["mistnost"] = "archiv"
        return dialog("2 / 3 • Archiv", "Projdi mezi regály. Ve vzdálené kartotéce najdi záznam o sálu pro školní turnaj.", [("Prozkoumat archiv", "zavrit")])
    if akce == "recepce":
        stav["mistnost"] = "recepce"
        return None
    if akce == "kartoteka":
        return dialog("Kartotéka", "Hledáš doklad pro školní turnaj. Který záznam potřebuješ?", [("Sál • sportovní a školní akce", "zaznam"), ("Parkoviště • rezervace stání", "spatny_zaznam"), ("Zpět", "zavrit")])
    if akce == "spatny_zaznam":
        return dialog("Nesprávný šanon", "Tohle je evidence parkovišť. Zkus šanon se sálem.", [("Vybrat znovu", "kartoteka")])
    if akce == "zaznam":
        if formular < 3 or stav.get("mistnost") != "archiv":
            return dialog("Nejdřív do archivu", "Záznam musíš vyzvednout v archivu po přijetí žádosti.", [("Zpět", "zavrit")])
        stav["zaznam"] = True
        return dialog("Získáno: záznam o sálu", "Sál je vhodný pro školní turnaj. Vrať se spodními dveřmi a zamiř do kanceláře vpravo.", [("Pokračovat", "zavrit")])
    if akce == "kancelar":
        if not stav.get("zaznam"):
            return dialog("Průchod uzavřen", "Ke schválení potřebuješ záznam o sálu z archivu vlevo.", [("Zpět", "zavrit")])
        stav["mistnost"] = "kancelar"
        return dialog("3 / 3 • Schvalovací kancelář", "Obejdi přepážky a dojdi k panu Dvořákovi. Máš všechny potřebné podklady.", [("Vstoupit", "zavrit")])
    if akce == "schvaleni":
        if formular != 3 or not stav.get("zaznam") or stav.get("mistnost") != "kancelar":
            return dialog("Chybí podklady", "Nejdřív podej žádost a vyzvedni záznam v archivu.", [("Zpět", "zavrit")])
        stav["schvaleno"] = True
        return dialog("Dnešní úsek splněný!", "Pan Dvořák zkontroloval záznam a přidal razítko. Prošel jsi všechny tři části úřadu. Konečné rozhodnutí a dvě zakončení doplníme v dalších dnech.", [("Prohlédnout úřad", "zavrit"), ("Začít znovu", "restart")])
    raise ValueError("Neznámá akce: " + akce)


UKOLY = [
    "Zjisti, jak vyřídit povolení. Začni u úřednice.",
    "Vyplň A-38 u psacího stolku vpravo.",
    "Odevzdej podepsanou žádost úřednici.",
    "Úvodní úkol splněn. Další část přijde příště.",
]
INVENTAR = ["Prázdné kapsy", "A-38 • nevyplněný", "A-38 • podepsaný", "Žádost odevzdána"]


def aktualni_ukol(stav):
    if stav.get("schvaleno"):
        return "Tři části úřadu splněny. Záznam má kontrolní razítko."
    if stav["formular"] < 3:
        return UKOLY[stav["formular"]]
    if not stav.get("zaznam"):
        return "V archivu vlevo najdi záznam o sálu."
    return "Zanes záznam do schvalovací kanceláře vpravo."
