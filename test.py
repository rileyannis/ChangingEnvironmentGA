#!/usr/bin/python

import random
population = []
for _ in range(100):
    org = random.randrange(1, 101)
    population.append(org)


if __name__ == "__main__":
    print(population)
