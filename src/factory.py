from models import Part  # Potřebujeme znát strukturu dílu

class ProductionLine:
    """
    Tato třída řídí celou výrobní linku. 
    Obsahuje seznam robotů a zajišťuje logiku předávání dílů mezi nimi.
    """
    def __init__(self):
        # Kompozice: Linka se skládá ze seznamu robotů
        self.robots = []
        # Fronta dílů, které na linku teprve vstoupí
        self.input_queue = []
        # Seznam úspěšně dokončených dílů
        self.finished_parts = []
        # Celkový čas simulace
        self.total_time = 0

    def add_robot(self, robot):
        """Přidá robota na konec výrobní linky."""
        self.robots.append(robot)
        print(f"Do linky byl přidán robot: {robot.name}")

    def add_part_to_line(self, part):
        """Vloží nový díl na začátek výrobního procesu."""
        self.input_queue.append(part)

    def tick(self, dt=1):
        """
        Jeden časový krok celé linky. 
        Zajišťuje pohyb dílů mezi roboty a volá tick u každého robota.
        """
        self.total_time += dt
        
        # 1. Posun dílů mezi roboty (Odzadu, aby se díly nekupily)
        # Obrácené pořadí využito, aby bylo nejdříve uvolněno místo u posledního robota
        for i in range(len(self.robots) - 1, -1, -1):
            current_robot = self.robots[i]
            
            # Necháme robota pracovat (zavoláme jeho tick)
            finished_part = current_robot.tick(dt)
            
            # Pokud robot právě dokončil práci na dílu:
            if finished_part:
                print(f"Čas {self.total_time}s: [{current_robot.name}] dokončil díl {finished_part.part_id}")
                
                # Pokud je to poslední robot v řadě, díl jde do skladu
                if i == len(self.robots) - 1:
                    self.finished_parts.append(finished_part)
                else:
                    # Jinak díl předáme dalšímu robotovi v seznamu
                    next_robot = self.robots[i + 1]
                    next_robot.process(finished_part)

        # 2. Přísun nových dílů z fronty
        # Pokud máme v hlavní frontě díly a první robot má místo, předáme mu ho
        if self.input_queue and self.robots:
            first_robot = self.robots[0]
            # Zkusíme předat první díl z fronty - index 0
            if first_robot.process(self.input_queue[0]):
                self.input_queue.pop(0)

    def get_statistics(self):
        """Vypočítá a vypíše statistiky výkonu linky."""
        print("\n" + "="*30)
        print("Statistiky výrobní linky")
        print("="*30)
        print(f"Celkový čas simulace: {self.total_time} s")
        print(f"Počet hotových výrobků: {len(self.finished_parts)}")
        
        for robot in self.robots:
            # Každý robot má specifické statistiky
            status = f"Robot {robot.name}: stav={robot.state}, ve frontě={len(robot.queue)}"
            
            # Pokud je robot typu Inspector - kontrola extra atributů
            if hasattr(robot, 'passed_count'):
                status += f" (OK: {robot.passed_count}, Zmetky: {robot.failed_count})"
            
            print(status)
        print("="*30)
