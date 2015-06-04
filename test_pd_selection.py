import unittest
import pd_selection

class TestSelection(unittest.TestCase):
    def setUp(self):
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
        """
        Get next generation by selection is a function that takes a list of organisms
        
        For a given tournament size, it runs a tournament, selects the best half and adds
        them to a population that becomes the next generation
        It repeats more tournaments until the next generation reaches the population size
        """
        pass
        
if __name__ == "__main__":
    unittest.main()