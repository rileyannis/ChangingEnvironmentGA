import unittest
from pd_org import MemoryPDGenotype as Geno

class TestMemoryPDGenotype(unittest.TestCase):

    def setUp(self):
        self.num_bits = 2
        self.decision_list = [True, False, False, True]
        self.initial_mem = [True, False]
        self.geno = Geno(self.num_bits, self.decision_list, self.initial_mem)
        
    def test_init(self):
        self.assertEqual(self.num_bits, self.geno.number_of_bits_of_memory)
        self.assertEqual(self.decision_list, self.geno.decision_list)
        self.assertEqual(self.initial_mem, self.geno.initial_memory)

    def test_init_bad(self):
        with self.assertRaises(AssertionError):
            Geno(2, [True]*4, [False])

        with self.assertRaises(AssertionError):
            Geno(2, [True]*3, [False]*2)

    def test_eq(self):
        geno2 = Geno(self.num_bits, self.decision_list, self.initial_mem)
        self.assertEqual(self.geno, geno2)
        
        geno3 =  Geno(1, [False, True], [False])
        self.assertNotEqual(self.geno, geno3)
        
        geno4 = Geno(self.num_bits, [True, True, False, True], self.initial_mem)
        self.assertNotEqual(self.geno, geno4)
        
        geno5 = Geno(self.num_bits, self.decision_list, [False, True])
        self.assertNotEqual(self.geno, geno5)
        
    def test_str(self):
        expected = "MemoryPDGenotype(2, [True, False, False, True], [True, False])"
        result = str(self.geno)
        self.assertEqual(expected, result)
        
        result_repr = repr(self.geno)
        self.assertEqual(expected, result_repr)
    
    def test_decision_list_mutant(self):
        mutant = self.geno._decision_list_mutant()
        self.assertNotEqual(mutant, self.geno)
        

if __name__ == "__main__":
    unittest.main()
