"""

"""

import random

MAX_BITS_OF_MEMORY = None

class MemoryPDGenotype(object):
    """
    """

    def __init__(self, number_of_bits_of_memory, decision_list):
        assert len(decision_list) == 2 ** number_of_bits_of_memory
        self.number_of_bits_of_memory = number_of_bits_of_memory
        self.decision_list = decision_list
    
    def __eq__(self, other):
        return (self.number_of_bits_of_memory == other.number_of_bits_of_memory and
                self.decision_list == other.decision_list)
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return "MemoryPDGenotype({}, {})".format(self.number_of_bits_of_memory, self.decision_list)
    
    def __repr__(self):
        return str(self)

    def get_mutant_of_self(self):
        """
        Returns a mutant of the current genotype.
        Mutations are as equally likely to happen to any single location in the decision 
        list as to change the number of bits of memory.
        Thus, the number of possible mutations is the length of the decision list plus one
        (possibility of changing length).
        """

        def get_bits_of_memory_mutant():
            should_increase_memory = random.choice([True, False])
            if self.number_of_bits_of_memory == 0 and not should_increase_memory:
                return self
            if self.number_of_bits_of_memory == MAX_BITS_OF_MEMORY and should_increase_memory:
                return self
            if should_increase_memory:
                new_number_of_bits_of_memory = self.number_of_bits_of_memory + 1
                new_decision_list = self.decision_list * 2
                return MemoryPDGenotype(new_number_of_bits_of_memory, new_decision_list)
            # should decrease memory
            new_number_of_bits_of_memory = self.number_of_bits_of_memory - 1
            length_of_new_decision_list = len(self.decision_list) // 2
            new_decision_list = self.decision_list[:length_of_new_decision_list]
            return MemoryPDGenotype(new_number_of_bits_of_memory, new_decision_list)

        def decision_list_mutant(mutation_location):
            new_decision_list = self.decision_list[:]
            new_decision_list[mutation_location] = not new_decision_list[mutation_location]
            return MemoryPDGenotype(self.number_of_bits_of_memory, new_decision_list)

        mutation_location = random.randrange(len(self.decision_list) + 1)
        if mutation_location == len(self.decision_list):
            return get_bits_of_memory_mutant()
        return decision_list_mutant(mutation_location)


class PDOrg(object):
    """
        
        
        
    """
    
    def __init__(self, genotype=None):
        if genotype is None:
            genotype = _create_random_genotype()
        self.genotype = genotype
    
    def fitness(self, environment):
        pass
    
    def get_mutant(self):
        return PDOrg(self.genotype.get_mutant_of_self())
    
    def __eq__(self, other):
        return self.genotype == other.genotype
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return "PDOrg({})".format(self.genotype)
    
    def __repr__(self):
        return str(self)
    
    def is_better_than(self, other, environment):
        pass

def _create_random_genotype():
    number_of_bits_of_memory = random.randrange(MAX_BITS_OF_MEMORY + 1)

    length = 2 ** number_of_bits_of_memory
    decision_list = [random.choice([True, False]) for _ in range(length)]

    return MemoryPDGenotype(number_of_bits_of_memory, decision_list)



