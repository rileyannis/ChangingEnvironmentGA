"""
This module takes two PD orgs and determines 
their score in an iterated Prisoner's Dilemma
"""

import pd_org
import itertools

NUMBER_OF_ROUNDS = 64

TEMPTATION = 5
REWARD = 3
PUNISHMENT = 1
SUCKER = 0

PROPORTION_COST_PER_MEMORY_BIT = .01

def pd_payout(a_cooperates, b_cooperates):
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
            
    if a_cooperates and b_cooperates:
        return REWARD, REWARD
    elif a_cooperates and not b_cooperates:
        return SUCKER, TEMPTATION
    elif not a_cooperates and b_cooperates:
        return TEMPTATION, SUCKER
    elif not a_cooperates and not b_cooperates:
        return PUNISHMENT, PUNISHMENT
    raise AssertionError("Impossible To Get Here")


def run_game(organism_a, organism_b):
    """
    Run a game of NUMBER OF ROUNDS long
    Return payout for both organisms
    """
    organism_a.initialize_memory()
    organism_b.initialize_memory()
    
    total_payout_a = 0
    total_payout_b = 0
    
    for _ in range(NUMBER_OF_ROUNDS):
        a_cooperates = organism_a.will_cooperate()
        b_cooperates = organism_b.will_cooperate()

        payout_a, payout_b = pd_payout(a_cooperates, b_cooperates)
        
        organism_a.opponent_cooperated_last_round(b_cooperates)
        organism_b.opponent_cooperated_last_round(a_cooperates)
    
        total_payout_a += payout_a
        total_payout_b += payout_b
    
    organism_a.initialize_memory()
    organism_b.initialize_memory()
    
    return total_payout_a, total_payout_b
    
def adjusted_payout(organism_a, organism_b):
    """
    Returns adjusted payout reward for each organism
    """
    def proportion_cost(org):
        return PROPORTION_COST_PER_MEMORY_BIT * org.genotype.number_of_bits_of_memory
    
    def get_adjusted_payout(payout, proportion_cost):
        return payout * (1 - proportion_cost)
        
    payout_a, payout_b = run_game(organism_a, organism_b)
    a_proportion_cost = proportion_cost(organism_a)
    b_proportion_cost = proportion_cost(organism_b)
    
    adj_payout_a = get_adjusted_payout(payout_a, a_proportion_cost)
    adj_payout_b = get_adjusted_payout(payout_b, b_proportion_cost)
   
    return adj_payout_a, adj_payout_b
    
def get_average_payouts(organisms):
    """    
    Lists all possible pairs of organisms, calls adj_payout
    Averages all together
    Returns a generator of pairs of orgs and their avg payout
    """
    total_payouts = [0.0 for _ in organisms]
    all_pairs = itertools.combinations(range(len(organisms)), 2)
    for i, j in all_pairs:
        org_a = organisms[i]
        org_b = organisms[j]
        payout_a, payout_b = adjusted_payout(org_a, org_b)
        total_payouts[i] += payout_a
        total_payouts[j] += payout_b
            
    number_of_games_per_org = len(organisms) - 1
    average_payouts = [payout / number_of_games_per_org for payout in total_payouts] 
  
    return zip(organisms, average_payouts)