from models import Part, Welder, Inspector, Painter, Assembler
from factory import ProductionLine

def run_simulation():
    # 1. Spuštění linky
    line = ProductionLine()

    # 2. Vytvoření robotů
    # Nastavení jmen a časů cyklů (sekundy)
    welder = Welder("Svářeč-01", cycle_time=3)
    inspector = Inspector("Kontrolor-01", cycle_time=2, success_rate=0.85)
    painter = Painter("Lakýrník-01", cycle_time=4)
    assembler = Assembler("Montážník-01", cycle_time=5)

    # 3. Sestavení linky
    # Pořadí, v jakém roboty přidáme, určuje tok výroby
    line.add_robot(welder)
    line.add_robot(inspector)
    line.add_robot(painter)
    line.add_robot(assembler)

    # 4. Příprava dílů
    # Vytvoření 5-i dílů, které mají projít linkou
    for i in range(1, 6):
        new_part = Part(part_id=f"DIL-{i:03d}", part_type="karoserie")
        line.add_part_to_line(new_part)

    print("\n>>> START SIMULACE <<<")
    
    # 5. Simulační smyčka
    # Simulujeme 40 sekund provozu
    for second in range(40):
        line.tick(dt=1)
        
        # Každých 10 sekund může vypsat průběžný stav
        if second % 10 == 0 and second > 0:
            print(f"--- Probíhá {second}. sekunda simulace ---")

    # 6. Výstup jednotlivých statistik
    print("\n>>> SIMULACE DOKONČENA <<<")
    line.get_statistics()

if __name__ == "__main__":
    run_simulation()
