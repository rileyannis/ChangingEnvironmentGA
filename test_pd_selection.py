import unittest
import pd_selection
import pd_org

class TestSelection(unittest.TestCase):
    def setUp(self):
        pd_org.MAX_BITS_OF_MEMORY = 5
        self.paired_organism_payouts = [('org',   2.15), 
                                        ('org2',  3.96), 
                                        ('org3',  32.3), 
                                        ('org4',  13.2)]
                                        
    def test_get_best_half(self):
        result = pd_selection.get_best_half(self.paired_organism_payouts)
        expected = ['org3', 'org4']
        self.assertEqual(len(result), len(expected))
        self.assertEqual(set(result), set(expected))
        
    def test_get_next_generation_by_selection(self):
        pd_selection.TOURNAMENT_SIZE = 2
        organism_a = pd_org.PDOrg(pd_org.MemoryPDGenotype(1,[True, False], [False]))
        organism_b = pd_org.PDOrg(pd_org.MemoryPDGenotype(2,[True, False, False, True], [False, True]))
        organisms = [organism_a, organism_b]
        result = pd_selection.get_next_generation_by_selection(organisms)
        self.assertEqual(len(organisms),len(result))
        self.assertTrue(set(organisms) >= set(result))
        
if __name__ == "__main__":
    unittest.main()