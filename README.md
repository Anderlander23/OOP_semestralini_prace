# Simulace výrobní linky
Tento projekt se zabývá simulací výrobní linky společně s implementací OOP principů.

---

## Klíčové Funkce
* **Diskrétní čas:** Simulace běží po sekundových krocích (`tick`).
* **Stavy robotů:** Každý robot sleduje svůj stav (`waiting`, `working`) a zbývající čas cyklu.
* **Kontrola kvality:** Robot `Inspector` náhodně vyřazuje vadné díly na základě nastavitelné úspěšnosti.
* **Statistiky:** Automatický výpočet celkového času, počtu hotových výrobků a výkonu stanic.

---

## Navigace v Projektu
```text
production_simulation/
├── src/                  # Zdrojové kódy aplikace
│   ├── __init__.py       # Označuje složku jako Python balíček
│   ├── models.py         # Datové modely (Part) a třídy robotů
│   └── factory.py        # Logika výrobní linky a koordinace
├── tests/                # Automatizované testy
│   └── test_simulation.py
├── main.py               # Vstupní bod pro spuštění simulace
├── README.md             # Tato dokumentace
└── .gitignore            # Soubory ignorované verzovacím systémem Git

---

## Instalace
### 1. Připravené programy
* **Python 3.8+** (nainstalovaný a přidaný do systémové cesty PATH)
* **Git** (pro klonování repozitáře)

### 2. Klonování projektu
Nejprve si stáhněte projekt do svého počítače:
```bash
git clone [https://github.com/Anderlander23/OOP_semestralini_prace.git](https://github.com/Anderlander23/OOP_semestralini_prace.git)
cd OOP_semestralini_prace

### 3. Spuštění
* Příkaz
python main.py

### 4. Testy
* Příkaz
python -m unittest discover tests