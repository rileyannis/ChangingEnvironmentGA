import main
import unittest

class TestMainModule(unittest.TestCase):
    
    def test_get_fitness_perfect(self):
        fitness = main.get_fitness(main.TARGET_STRING)
        self.assertEqual(fitness, len(main.TARGET_STRING))

    def test_get_fitness_worst(self):
        terrible_org = "0" * len(main.TARGET_STRING)
        fitness = main.get_fitness(terrible_org)
        self.assertEqual(fitness, 0)

    def test_get_fitness_one_off(self):
        one_off = main.TARGET_STRING[:-1] + "0"
        fitness = main.get_fitness(one_off)
        self.assertEqual(fitness, len(main.TARGET_STRING) - 1)

    def test_get_mutated_organism(self):
        for _ in range(200):
            mutated_org = main.get_mutated_organism(main.TARGET_STRING)
            self.assertNotEqual(mutated_org, main.TARGET_STRING)

    def test_create_random_organism(self):
        org = main.create_random_organism()
        self.assertEqual(len(org), len(main.TARGET_STRING))

    def test_create_initial_population(self):
        pop = main.create_initial_population()
        self.assertEqual(len(pop), main.NUMBER_OF_ORGANISMS)

if __name__ == "__main__":
    unittest.main()
