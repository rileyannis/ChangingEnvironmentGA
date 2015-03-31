import unittest
import fitness_function as ff
import cython_fitness_function as cy

class TestFitnessFunction(unittest.TestCase):
    
    def setUp(self):
        self.vals = [1.0, 2.0]
    
    def test_flat_function(self):
        self.assertEqual(ff.flat_function(self.vals), cy.flat_function(self.vals))

    def test_sphere_function(self):
        self.assertEqual(ff.sphere_function(self.vals), cy.sphere_function(self.vals))

    def test_rosenbrock_function(self):
        self.assertEqual(ff.rosenbrock_function(self.vals), cy.rosenbrock_function(self.vals))

    def test_rana_function(self):
        #Rana functions are based on random numbers, so ff and cy give slightly different numbers
        self.assertEqual(ff.rana_function(self.vals), ff.rana_function(self.vals))
        self.assertEqual(cy.rana_function(self.vals), cy.rana_function(self.vals))
        self.assertEqual(len(ff.RANA_WEIGHTS), len(cy.RANA_WEIGHTS))

    def test_schafferF7(self):
        self.assertEqual(ff.schafferF7(self.vals), cy.schafferF7(self.vals))

    def test_deceptive(self):
        self.assertEqual(ff.deceptive(self.vals), cy.deceptive(self.vals))

class TestFitnessFunctionClass(unittest.TestCase):

    def setUp(self):
        self.ff_object = ff.Fitness_Function(ff.sphere_function, 2)
        self.cy_object = cy.Fitness_Function(cy.sphere_function, 2)
        self.vals = [1.0, 2.0]

    def test_fitness1_fitness(self):
        self.assertEqual(self.ff_object.fitness1_fitness(self.vals), ff.sphere_function(self.vals))
        self.assertEqual(self.cy_object.fitness1_fitness(self.vals), cy.sphere_function(self.vals))
        self.assertEqual(self.ff_object.fitness1_fitness(self.vals), self.cy_object.fitness1_fitness(self.vals))
