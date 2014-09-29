
import unittest
from string_org import *

class TestStringOrgModule(unittest.TestCase):
    
    def test_get_fitness_perfect(self):
        fitness = get_fitness(TARGET_STRING)
        self.assertEqual(fitness, len(TARGET_STRING))

    def test_get_fitness_worst(self):
        terrible_org = "0" * len(TARGET_STRING)
        fitness = get_fitness(terrible_org)
        self.assertEqual(fitness, 0)

    def test_get_fitness_one_off(self):
        one_off = TARGET_STRING[:-1] + "0"
        fitness = get_fitness(one_off)
        self.assertEqual(fitness, len(TARGET_STRING) - 1)

    def test_get_mutated_organism(self):
        for _ in range(200):
            mutated_org = get_mutated_organism(TARGET_STRING)
            self.assertNotEqual(mutated_org, TARGET_STRING)

    def test_create_random_organism(self):
        create_random_organism()

    def test_create_initial_population(self):
        pop = main.create_initial_population()
        self.assertEqual(len(pop), main.NUMBER_OF_ORGANISMS)

if __name__ == "__main__":
    unittest.main()
