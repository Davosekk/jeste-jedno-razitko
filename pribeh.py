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
    # Obtížnější úkoly mají vlastní malou funkci, aby původní příběh zůstal čitelný.
    if akce in HADANKY:
        return tezsi_ukoly(akce, stav)
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
        return dialog("2 / 3 • Archiv", "Projdi mezi regály. U mříže přečti pokyny. Spínače musíš obejít ve správném pořadí; pak se dostaneš ke kartotéce.", [("Prozkoumat archiv", "zavrit")])
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
        if not stav.get("mriz"):
            return dialog("Za mříží", "Nejdřív otevři mříž pomocí barevných spínačů.", [("Zpět", "zavrit")])
        stav["zaznam"] = True
        return dialog("Získáno: záznam o sálu", "Sál je vhodný pro školní turnaj. Vrať se spodními dveřmi a zamiř do kanceláře vpravo.", [("Pokračovat", "zavrit")])
    if akce == "kancelar":
        if not stav.get("zaznam"):
            return dialog("Průchod uzavřen", "Ke schválení potřebuješ záznam o sálu z archivu vlevo.", [("Zpět", "zavrit")])
        stav["mistnost"] = "kancelar"
        return dialog("3 / 3 • Schvalovací kancelář", "Obejdi přepážky a dojdi k panu Dvořákovi. U pokladny zjisti poplatek a na tabuli pořadí kontrolních stanovišť.", [("Vstoupit", "zavrit")])
    if akce == "schvaleni":
        if formular != 3 or not stav.get("zaznam") or stav.get("mistnost") != "kancelar":
            return dialog("Chybí podklady", "Nejdřív podej žádost a vyzvedni záznam v archivu.", [("Zpět", "zavrit")])
        if not stav.get("uctenka") or not stav.get("kontrola"):
            return dialog("Ještě kontrola a poplatek", "U pokladny vypočítej poplatek za turnaj. Potom projdi kontrolní stanoviště podle tabule. Až pak mohu přidat razítko.", [("Zpět", "zavrit")])
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
        if not stav.get("mriz"):
            return "Archiv: přečti pokyny a otevři mříž spínači."
        return "V archivu za otevřenou mříží vyzvedni záznam."
    if not stav.get("uctenka"):
        return "Kancelář vpravo: vyřeš poplatek u pokladny."
    if not stav.get("kontrola"):
        return "Přečti tabuli a projdi kontrolní stanoviště."
    return "Vše připraveno. Zanes podklady panu Dvořákovi."


# Dvě pořadové hádanky. Chyba vynuluje jen rozpracované pořadí.
SPINACE = ["cerveny", "modry", "zeleny", "cerveny"]
STANOVISTE = ["evidence", "pecet", "podpis"]
HADANKY = SPINACE + STANOVISTE + ["pokyny", "tabule", "pokladna", "platba", "spatna_platba"]


def tezsi_ukoly(akce, stav):
    mistnost = stav.get("mistnost", "recepce")
    archiv = akce in SPINACE or akce == "pokyny"
    if mistnost != ("archiv" if archiv else "kancelar") or stav["formular"] != 3:
        return dialog("Mimo dosah", "K tomuto stanovišti musíš nejdřív dojít.", [("Zpět", "zavrit")])
    if akce == "pokyny":
        return dialog("Nouzové otevření archivu", "Čtyři stisky, tři spínače. První i poslední stisk je červený. Zelený patří bezprostředně před poslední. Modrý je mezi prvním a zeleným.\n\nPři chybě se pořadí vynuluje. Otevřená mříž už zůstane otevřená.", [("Přečteno", "zavrit")])
    if akce == "tabule":
        return dialog("Postup kontrol", "Nejdřív zaplať u pokladny. Pak obejdi všechna tři stanoviště.\n\nPodpis smí přijít až po pečeti. Pečeť vyžaduje evidenci. Každé stanoviště navštiv jednou. Chyba resetuje pouze kontrolu, účtenka zůstává.", [("Přečteno", "zavrit")])
    if akce in ["pokladna", "platba", "spatna_platba"]:
        if not stav.get("zaznam"):
            return dialog("Chybí záznam", "Poplatek lze vyřídit až se záznamem o sálu.", [("Zpět", "zavrit")])
        if stav.get("uctenka"):
            return dialog("Uhrazeno", "Účtenku už máš. Znovu neplatíš.", [("Zpět", "zavrit")])
        if akce == "platba":
            stav["uctenka"] = True
            return dialog("Získáno: účtenka", "Správně: 120 + 3 × 40 − 20 = 220 Kč. Úřad přijímá školní poukaz. Pokračuj na kontrolní stanoviště podle tabule.", [("Pokračovat", "zavrit")])
        if akce == "spatna_platba":
            return dialog("Částka nesouhlasí", "Přičti poplatek za všechny tři týmy a školní slevu odečti jen jednou. Žádné peníze se neztratily.", [("Přepočítat", "pokladna"), ("Zpět", "zavrit")])
        return dialog("Pokladna • školní poukaz", "Základ: 120 Kč. Za každý tým: 40 Kč. Účastní se 3 týmy. Jednorázová školní sleva: 20 Kč.\n\nJaká částka má být na účtence?", [("200 Kč", "spatna_platba"), ("220 Kč", "platba"), ("240 Kč", "spatna_platba"), ("Zpět", "zavrit")])
    if not archiv and not stav.get("uctenka"):
        return dialog("Nejdřív pokladna", "Kontrolní stanoviště vyžaduje účtenku.", [("Zpět", "zavrit")])
    poradi = SPINACE if archiv else STANOVISTE
    klic = "spinace" if archiv else "stanoviste"
    hotovo = "mriz" if archiv else "kontrola"
    if stav.get(hotovo):
        return dialog("Už splněno", "Tato část je dokončená. Můžeš pokračovat dál.", [("Zpět", "zavrit")])
    krok = stav.get(klic, 0)
    if akce != poradi[krok]:
        stav[klic] = 0
        return dialog("Chybné pořadí", "Tahle část začíná znovu od prvního kroku. Přečti si pokyny; dokumenty ti zůstávají.", [("Zkusím znovu", "zavrit")])
    stav[klic] = krok + 1
    if stav[klic] == len(poradi):
        stav[hotovo] = True
        text = "Mříž je otevřená. Vyzvedni záznam v kartotéce." if archiv else "Kontrola dokončená. Dojdi s podklady k panu Dvořákovi."
        return dialog("Hádanka vyřešena", text, [("Pokračovat", "zavrit")])
    return dialog("Správný krok", "Postup: " + str(stav[klic]) + "/" + str(len(poradi)) + ". Dojdi k dalšímu stanovišti.", [("Pokračovat", "zavrit")])
