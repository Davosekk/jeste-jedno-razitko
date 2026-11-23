# Jak si projít kód

Nemusíš hned rozumět všem řádkům. Nejprve si hru spusť a potom čti v tomto pořadí.

## 1. Stav hry: co už hráč udělal

V `pribeh.py` funkce `novy_stav()` vrací slovník:

```python
{"formular": 0}
```

Číslo vyjadřuje stav dokumentu: 0 = žádný, 1 = prázdný, 2 = podepsaný, 3 = odevzdaný. Změna `stav["formular"] = 1` znamená, že hráč právě sebral formulář. Nepotřebujeme kvůli tomu složitý inventář ani třídy.

## 2. Podmínky: co se stane po rozhodnutí

Ve funkci `proved()` najdi `if akce == "odevzdat"`. Podle čísla formuláře úřednice žádost odmítne, vrátí k doplnění nebo přijme. To je základ úkolu.

Funkce `dialog()` pouze zabalí nadpis, text a možnosti. Například `("Děkuji", "zavrit")` znamená tlačítko s nápisem Děkuji a akcí zavrit. `None` znamená, že není otevřený žádný dialog.

## 3. Souřadnice: kde je hráč

V `main.py` je `START = (576, 532)`. První číslo je poloha zleva, druhé shora. Při pohybu doprava roste x, při pohybu dolů roste y.

`pygame.Vector2` uchovává dvě čísla a usnadňuje výpočet vzdálenosti a směru. `pygame.Rect` představuje obdélník, například stůl.

## 4. Pohyb a překážky

`posun_hrace()` vypočítá další pozici. Pokud nový obdélník u nohou narazí do stolu nebo zdi, nepovolí příslušný posun. Osa x a y se zkouší zvlášť, takže můžeš klouzat podél stěny.

Rychlost se násobí časem od minulého snímku. Postava se tak pohybuje podobně na rychlém i pomalejším počítači. Normalizace směru hlídá, aby šikmá chůze nebyla rychlejší.

## 5. Hlavní smyčka

Na konci `main.py` najdi `while bezi:`. Opakuje se přibližně 60× za sekundu:

1. Přečte stisky kláves a myši.
2. Vyhodnotí zvolenou akci.
3. Posune hráče, pokud není otevřený dialog.
4. Nakreslí kancelář, hráče a rozhraní.
5. Ukáže hotový snímek pomocí `pygame.display.flip()`.

## Malé úpravy na vyzkoušení

- Změň `RYCHLOST = 190` na 150 a zkus pomalejší chůzi.
- Změň text první odpovědi úřednice v `pribeh.py`.
- Změň barvu oblečení v `kresli_hrace()`.
- Spusť testy a ověř, že jsi nezměnil pravidla hry nechtěně.

Kreslení nábytku si nech nakonec. Obsahuje hlavně opakované obdélníky a není nutné mu rozumět, abys pochopil úkol a herní smyčku.


## Dva konce příběhu (verze 0.5)

`zavery.py` obsahuje poslední rozhovor s úřednicí. `proved_zaver()` nejprve ověří recepci, dokumenty, kontrolu, razítko a rezervaci. Volbu uloží do `volba_zaveru`; až potvrzení nastaví `zaver` na `povoleno` nebo `zamitnuto`. Text výsledku vrací `konec_pribehu()`.

Na začátku `proved()` se kontroluje `stav.get("zaver")`. Po dokončení se vrací závěrečný dialog a stav už se nemění. Tlačítka `restart` a `konec` zachytává hlavní smyčka v `main.py`. Restart vytvoří `novy_stav()` a vrátí postavu na start, takže zmizí i rezervace a výsledek.
