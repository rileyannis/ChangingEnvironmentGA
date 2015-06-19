import unittest
import pd_selection
import pd_org

class TestSelection(unittest.TestCase):
    def setUp(self):
        pd_org.MAX_BITS_OF_MEMORY = 5
        
        pd_selection.TOURNAMENT_SIZE = 2
        self.organism_a = pd_org.PDOrg(pd_org.MemoryPDGenotype(1,[True, False], [False]))
        self.organism_b = pd_org.PDOrg(pd_org.MemoryPDGenotype(2,[True, False, False, True], [False, True]))
        self.organisms = [self.organism_a, self.organism_b]
        self.organism_a.average_payout = 0
        self.organism_b.average_payout = 9.8

    def test_get_best_half(self):
        result = pd_selection.get_best_half(self.organisms)
        expected = [self.organism_b]
        self.assertNotEqual(len(self.organisms), len(result))
    
    def test_get_next_generation_by_selection(self):
        result = pd_selection.get_next_generation_by_selection(self.organisms)
        self.assertEqual(len(self.organisms),len(result))
        

        
if __name__ == "__main__":
    unittest.main()
