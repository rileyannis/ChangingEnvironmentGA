"""
This module takes two PD orgs and determines 
their score in an iterated Prisoner's Dilemma
"""

import pd_org

NUMBER_OF_ROUNDS = 500

TEMPTATION = 4
REWARD = 3
PUNISHMENT = 2
SUCKER = 1

def my_reward(self_is_cooperator, other_is_cooperator):
    """
    Function my_reward determines reward given by the state of self and other
        
    Another way to implement below code:
    if self_is_cooperator:
        if other_is_cooperator:
            return reward
            return sucker
    if other_is_cooperator:
        return temptation
    return punishment
    """
            
    if self_is_cooperator and other_is_cooperator:
        return REWARD
    elif self_is_cooperator and not other_is_cooperator:
        return SUCKER
    elif not self_is_cooperator and other_is_cooperator:
        return TEMPTATION
    elif not self_is_cooperator and not other_is_cooperator:
        return PUNISHMENT
    raise AssertionError("Impossible To Get Here")





def run_game(organism_a, organism_b):
    pass

