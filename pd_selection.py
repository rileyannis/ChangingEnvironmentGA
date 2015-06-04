import pd_tournament
import random

TOURNAMENT_SIZE = None

def get_best_half(paired_organism_payouts):
    """
    This will run a tournament with the given organisms and
    return a list of the top half of the organisms in terms of payout
    """
    sorted_pairs = sorted(paired_organism_payouts, key=lambda pair: pair[1], reverse=True)
    best_half_pairs = sorted_pairs[:len(paired_organism_payouts) // 2]
    return [org for org, _ in best_half_pairs]
    
def get_next_generation_by_selection(organisms):
    """
    Get next generation by selection is a function that takes a list of organisms
    
    Shuffle the organisms and group them into TOURNAMENT_SIZEd clumps
    For a given tournament size, it runs a tournament
    selects the best half
    Adds them to a population that becomes the next generation
    If more tournaments more need to be run after all the clumps are used, we shuffle the
    population and make more clumps
    It repeats more tournaments until the next generation reaches the population size
    """
    def generate_contenders(organisms):
        random.shuffle(organisms)
        number_of_tournaments = len(organisms) // TOURNAMENT_SIZE
        if not len(organisms) % TOURNAMENT_SIZE:
            number_of_tournaments += 1
        for i in range(number_of_tournaments):
            organisms[TOURNAMENT_SIZE * i: TOURNAMENT_SIZE * (i + 1)]
            
            
            
            
    next_generation = []
    #function that adds things to next generation
    while len(next_generation) < len(organisms):
        #pick organisms for the tournament
        
        #get the winners of the tournament
        #add winners to the next generation
    #make next_generation same length as organisms
    return next_generation[:len(organisms)]
    