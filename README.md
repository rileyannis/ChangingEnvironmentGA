#Changing Environments
This project will observe the relative improvement in fitness of a digital organism moved from its natural environment to a new one, and then back.

##Researchers:
Riley Annis, Josh Nahum, Emily Dolson

##Dependencies:
Numpy, Scipy, Cython

###Necessary Files:
* changing_environments_ga.py
* main.py
* fitness_function.pyx
* cpp_fitness_function.cpp
* string_org.py
* real_value_vector_org.py
* pd files

###Config File Arguenments:
* Necessary for all types:
  * org_type
  * number_of_organisms
  * mutation_rate
  * number_of_generations
  * tournament_size
  * verbose
  * output_frequency
* Necessary for string orgs:
  * target_string
  * letters
* Necessary for real value vector orgs:
  * fitness_function_type
  * crowding
  * range_minimum
  * range_maximum
  * mutation_effect_size
  * alternate_environment_corr
  * length
* Necessary for pd orgs:
  * Will fill in later

###changing_environments_ga.py Command Line Arguements:
* -c  config file location
* -o  desired output directory

###Use With String Orgs:
Not used, possibly broken.

###Use With Real Value Vector Orgs:
I'll get to this soon, I promise.

###Use With PD Orgs (Static Environment):
Might fill this in
