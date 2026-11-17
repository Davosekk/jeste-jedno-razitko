# Ještě jedno razítko — Python 0.1

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

Úvodní úkol: získej formulář A-38, vyplň ho u stolku vpravo a odevzdej úřednici. Tato krátká verze ještě neobsahuje všechny zóny ani závěry plánované finální hry.

## Co otevřít jako první

- `pribeh.py` — krátké funkce a podmínky pro dokumenty a rozhovory. Začni tady.
- `main.py` — čtyři označené části: nastavení, pohyb, kreslení a hlavní smyčka.
- `JAK_KOD_FUNGUJE.md` — vysvětlení základních principů.
- `PLAN.md` — omezený rozsah a denní kroky.
- `tests/test_hra.py` — ověření úkolu, dialogů a kolizí.

## Windows .exe

Python verzi je potřeba sestavit na Windows; staré .exe z Godotu není sestavení tohoto kódu. V terminálu VS Code na Windows:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onefile --windowed --name Jeste_jedno_razitko main.py
```

Výsledek je `dist/Jeste_jedno_razitko.exe`. Hráč už Python ani Pygame instalovat nemusí. Skript `vytvor_exe.bat` provede instalaci závislostí, testy a sestavení přes Python dostupný jako `python`.

Připravený GitHub Actions postup `windows.yml` spustí stejné testy a sestaví .exe na Windows po odeslání do repozitáře. Dokud běh skutečně neskončí úspěšně, není Windows sestavení této verze potvrzené.

## Testy

```sh
python -m unittest discover -s tests -v
```

Repozitář nemá obsahovat `.venv`, `__pycache__`, `build` ani `dist`. Commity mají odpovídat skutečné práci, bez zpětného vytváření falešné denní historie.

## Ověření verze 0.1

Prošlo 17 automatických testů pravidel, celého úkolu, dialogových větví a kolizí. Celý úvodní úkol byl dohrán klávesnicí v grafickém okně Pygame na Linuxu. Windows sestavení Python verze zatím nebylo vytvořené ani spuštěné; připravený postup je uveden výše.
