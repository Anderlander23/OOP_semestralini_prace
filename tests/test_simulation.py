import unittest
# Importování tříd
from src.models import Part, Welder, Inspector

class TestRobotLogic(unittest.TestCase):
    """
    Třída TestRobotLogic obsahuje sadu testů určených pro ověření základní logiky robotů.
    Každá metoda začínající 'test_' je automaticky spuštěna jako test.
    """

    def setUp(self):
        """
        Metoda setUp se spustí před každým testem.
        Budou tam připraveny čerstvé objekty pro testování.
        """
        self.part = Part(part_id="TEST-01", part_type="karoserie")
        self.welder = Welder("Test-Svářeč", cycle_time=5)

    def test_robot_accepts_valid_part(self):
        """Testuje, jestli robot přijme správný typ dílu."""
        # Robot 'Welder' má nastaveno, že přijímá 'karoserie'
        accepted = self.welder.process(self.part)
        self.assertTrue(accepted, "Robot by měl přijmout díl typu 'karoserie'.")
        self.assertEqual(len(self.welder.queue), 1, "Ve frontě by měl být 1 díl.")

    def test_robot_rejects_invalid_part(self):
        """Testuje, jestli robot odmítne nesprávný typ dílu."""
        wrong_part = Part(part_id="CHYBA", part_type="motor")
        accepted = self.welder.process(wrong_part)
        self.assertFalse(accepted, "Robot by neměl přijmout díl typu 'motor'.")
        self.assertEqual(len(self.welder.queue), 0, "Fronta by měla zůstat prázdná.")

      def test_inspector_logic(self):
        """Testuje, jestli Inspector čas od času vyřadí díl."""
        # Úspěšnost nastavena na 0%, aby každý díl byl zmetek
        bad_inspector = Inspector("Přísný-Kontrolor", cycle_time=1, success_rate=0.0)
        bad_inspector.process(self.part)
        bad_inspector.tick(1) # Spustí práci
        result = bad_inspector.tick(1) # Dokončí práci
        
        self.assertIsNone(result, "Při 0% úspěšnosti by měl inspektor díl zahodit (vrátit None).")
        self.assertEqual(bad_inspector.failed_count, 1)

if __name__ == "__main__":
    unittest.main()
