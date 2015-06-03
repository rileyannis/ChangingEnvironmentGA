import unittest
from pd_org import MemoryPDGenotype as Geno

class TestMemoryPDGenotype(unittest.TestCase):

    def test_init(self):
        num_bits = 2
        decision_list = [True, False, False, True]
        initial_mem = [True, False]
        geno = Geno(num_bits, decision_list, initial_mem)
        self.assertEqual(num_bits, geno.number_of_bits_of_memory)
        self.assertEqual(decision_list, geno.decision_list)
        self.assertEqual(initial_mem, geno.initial_memory)

    def test_init_bad(self):
        with self.assertRaises(AssertionError):
            Geno(2, [True]*4, [False])

        with self.assertRaises(AssertionError):
            Geno(2, [True]*3, [False]*2)

    def test_eq(self):
        num_bits = 2
        decision_list = [True, False, False, True]
        initial_mem = [True, False]
        geno = Geno(num_bits, decision_list, initial_mem)
        geno2 = Geno(num_bits, decision_list, initial_mem)
        self.assertEqual(geno, geno2)
        
        geno3 =  Geno(1, [False, True], [False])
        self.assertNotEqual(geno, geno3)
        
        geno4 = Geno(num_bits, [True, True, False, True], initial_mem)
        self.assertNotEqual(geno, geno4)
        
        geno5 = Geno(num_bits, decision_list, [False, True])
        self.assertNotEqual(geno, geno5)

if __name__ == "__main__":
    unittest.main()
