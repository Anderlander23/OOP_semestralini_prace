import random
from abc import ABC, abstractmethod

# TŘÍDA PRO DÍLY
class Part:
    """
    Představuje nějaký díl, který se pohybuje po výrobní lince.
    Každý díl má při tom své unikátní ID a typ, který určuje, kdo ho může zpracovat.
    """
    def __init__(self, part_id, part_type):
        self.part_id = part_id
        self.part_type = part_type
        # Vytváří seznam pro ukládání historie aby bylo vidět kdo na tomto dílu pracoval a kdy to bylo
        self.history = []

    def __repr__(self):
        """Metoda pro lepší výpis objektu, např. při ladění (print)."""
        return f"Díl(ID={self.part_id}, Typ='{self.part_type}')"

# ABSTRAKTNÍ ZÁKLAD PRO ROBOTY
class Robot(ABC):
    """
    Víceméně šablona - nesmí být přímo vytvořena,
    ale na základě ní se pomocí dědičnosti bude dědit logika pro konkrétní specifické roboty.
    """
    def __init__(self, name, cycle_time, allowed_part_type):
        self.name = name
        self.cycle_time = cycle_time  # Jak dlouho bude konkrétnímu robotovi práce trvat
        self.allowed_part_type = allowed_part_type # Jaký typ dílu umí robot zpracovávat
        
        self.state = "waiting"      # Stavy: "waiting" (čeká), "working" (pracuje), "malfunction" (porucha)
        self.current_part = None    # Díl, na kterém se právě pracuje
        self.time_left = 0          # Odpočet do konce aktuální operace
        self.queue = []             # Fronta dílů čekajících na zpracování u tohoto robota

    def process(self, part):
        """
        Pokusí se přijmout díl do fronty. 
        Vrátí True, pokud je díl přijat, jinak vrátí False (např. špatný typ).
        """
        if part.part_type == self.allowed_part_type:
            self.queue.append(part)
            return True
        return False

    def tick(self, dt):
        """
        Jedná se o hlavní motor simulace. Volá se v nějakém určitém časovém kroku (třeba každou sekundu).
        dt = delta time (klasická změna času, obvykle 1).
        """
        # 1. Pokud robot nepracuje, ale má něco ve frontě, vezme si první díl co tam má
        if self.state == "waiting" and self.queue:
            self.current_part = self.queue.pop(0)
            self.state = "working"
            self.time_left = self.cycle_time
            # Zde by se dal přidat log: "Robot začal pracovat"

        # 2. Pokud robot právě pracuje, tak se odečítá čas
        if self.state == "working":
            self.time_left -= dt
            
            # 3. Kontrola, jestli už robot práci na konkrétním díle dokončil
            if self.time_left <= 0:
                finished_part = self.current_part
                # Zapíše se jméno robota do historie dílů
                finished_part.history.append(self.name)
                
                # Robot je připraven na další práci
                self.current_part = None
                self.state = "waiting"
                
                # Vrátíme hotový díl na linku a na řadu může přijít další robot
                return finished_part
                
        # Pokud práce stále probíhá nebo se nic neděje, vracíme None
        return None

# KONKRÉTNÍ SPECIFIČTÍ ROBOTI
class Welder(Robot):
    """Svářeč - první který na díl nastupuje - pracuje tedy na surových dílech."""
    def __init__(self, name, cycle_time):
        # Zavoláme 'super' abychom přivolali rodičovskou třídu Robot a nastavíme typ na 'karoserie'
        super().__init__(name, cycle_time, "karoserie")

class Inspector(Robot):
    """Kontrolor, který ověřuje kvalitu a může díl vyřadit jako zmetek."""
    def __init__(self, name, cycle_time, success_rate=0.9):
        super().__init__(name, cycle_time, "karoserie")
        self.success_rate = success_rate # Pravděpodobnost (0.0 až 1.0), že díl projde
        self.passed_count = 0  # Statistika kolik dílů prošlo
        self.failed_count = 0  # Statistika kolik dílů neprošlo

    def tick(self, dt):
        # Nejdříve necháme proběhnout standardní práci robota (odpočet času)
        part = super().tick(dt)
        
        # Pokud nám robot vrátil hotový díl k posouzení:
        if part:
            if random.random() < self.success_rate:
                # Díl je v pořádku
                self.passed_count += 1
                return part
            else:
                # Díl je zmetek - nevrátíme ho (nepůjde dál po lince)
                self.failed_count += 1
                return None
        return None

class Painter(Robot):
    """Lakýrník, který nanáší barvu na zkontrolovaný díl."""
    def __init__(self, name, cycle_time):
        super().__init__(name, cycle_time, "karoserie")

class Assembler(Robot):
    """Montážník, který kompletuje díl - je to poslední krok výroby."""
    def __init__(self, name, cycle_time):
        super().__init__(name, cycle_time, "karoserie")
