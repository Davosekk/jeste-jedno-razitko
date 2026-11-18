# Ještě jedno razítko — Python 0.2

Malá 2D příběhová adventura na téma **úřad a byrokracie**. Všechno se píše jako běžný Python kód ve VS Code. Používáme knihovnu Pygame, žádný herní editor.

## Spuštění ve VS Code

1. Nainstaluj Python 3.12 pro svůj systém a ve VS Code rozšíření **Python od Microsoftu**.
2. Rozbal projekt a ve VS Code otevři celou jeho složku.
3. Otevři terminál ve VS Code. Na Windows zadej:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

Aktivace virtuálního prostředí není pro tyto příkazy potřeba. Pro F5 otevři paletu příkazů, vyber **Python: Select Interpreter**, zvol `.venv` a spusť konfiguraci **Spustit hru**.

Na Linuxu/macOS:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

## Ovládání

- WASD / šipky: chůze.
- E: interakce zblízka.
- Myš nebo šipky + Enter: volba v rozhovoru.
- Esc: zavřít rozhovor nebo otevřít pauzu.
- R: nabídnout restart.

Úvodní úkol: získej formulář A-38, vyplň ho u stolku vpravo a odevzdej úřednici. Potom se otevře archiv vlevo. Projdi mezi regály, vyber záznam o sálu a vrať se spodními dveřmi. Se záznamem vstup do schvalovací kanceláře vpravo a obejdi přepážky k panu Dvořákovi. Dvě finální zakončení ještě nejsou hotová.

## Co otevřít jako první

- `pribeh.py` — krátké funkce a podmínky pro dokumenty a rozhovory. Začni tady.
- `main.py` — čtyři označené části: nastavení, pohyb, kreslení a hlavní smyčka.
- `JAK_KOD_FUNGUJE.md` — vysvětlení základních principů.
- `PLAN.md` — omezený rozsah a denní kroky.
- `tests/test_hra.py` — ověření úkolu, dialogů a kolizí.

## Nové ve verzi 0.2

Tři průchozí místnosti, zamčený archiv, podmíněný vstup ke schválení, regály a přepážky s kolizemi, výběr správného záznamu a druhý úředník. Mapy jsou v `mistnosti.py`. Celkem 20 testů včetně dostupnosti všech interakcí, návaznosti úkolů a rozměrů dialogů.

## Windows .exe

Aktuální aplikaci hledej v posledním úspěšném běhu na kartě **Actions**. Původní verze 0.1 je v [prvním sestavení](https://github.com/Davosekk/jeste-jedno-razitko/actions/runs/44131689905) dole v části **Artifacts → Jeste-jedno-razitko-Windows**. Stáhni ZIP, rozbal ho a spusť `Jeste_jedno_razitko.exe`. Je potřeba být přihlášený k účtu s přístupem do tohoto soukromého repozitáře. Tento výstup je uchován 14 dní; nový lze vytvořit v Actions přes Run workflow.

Vlastní .exe můžeš sestavit v terminálu VS Code na Windows:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onefile --windowed --name Jeste_jedno_razitko main.py
```

Výsledek je `dist/Jeste_jedno_razitko.exe`. Hráč už Python ani Pygame instalovat nemusí. Skript `vytvor_exe.bat` provede instalaci závislostí, testy a sestavení přes Python dostupný jako `python`.

GitHub Actions postup `windows.yml` spustí testy a sestaví .exe na Windows po odeslání do repozitáře.

## Testy

```sh
python -m unittest discover -s tests -v
```

Repozitář nemá obsahovat `.venv`, `__pycache__`, `build` ani `dist`. Commity mají odpovídat skutečné práci, bez zpětného vytváření falešné denní historie.

## Ověření verze 0.1

Prošlo 17 automatických testů pravidel, celého úkolu, dialogových větví a kolizí. Celý úvodní úkol byl dohrán klávesnicí v grafickém okně Pygame na Linuxu. Dne 17. 11. 2026 prošly testy i sestavení .exe na Windows v GitHub Actions (commit `757665d`). Samotné hraní ve Windows .exe zatím nebylo ručně ověřené.
