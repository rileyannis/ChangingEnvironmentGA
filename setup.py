from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'Changing Environment GA',
  ext_modules = cythonize("cython_fitness_function.pyx"),
)
