import pd_tournament
import random

TOURNAMENT_SIZE = None

def get_best_half(organisms):
    """
    This will run a tournament with the given organisms and
    return a list of the top half of the organisms in terms of payout
    """
    sorted_orgs = sorted(organisms, key=lambda org: org.average_payout, reverse=True)
    best_half_orgs = sorted_orgs[:len(organisms) // 2]
    return best_half_orgs[:]
    
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
    number_of_tournaments = len(organisms) // TOURNAMENT_SIZE
    if not len(organisms) % TOURNAMENT_SIZE:
        number_of_tournaments += 1
        
    def generate_contenders(organisms):
        while True:
            random.shuffle(organisms)
            for i in range(number_of_tournaments):
                yield organisms[TOURNAMENT_SIZE * i: TOURNAMENT_SIZE * (i + 1)]         
                   
    next_generation = []
    #function that adds things to next generation
    contender_generator = generate_contenders(organisms)
   
    #pick organisms for tournament
    #gets organisms average payout

    for _ in range(number_of_tournaments):
        contenders = next(contender_generator)
        pd_tournament.get_average_payouts(contenders)


    while len(next_generation) < len(organisms):
        #pick organisms for the tournament
        contenders = next(contender_generator)
        #gets winners of contenders
        winners = get_best_half(contenders)
        #add winners to the next generation
        next_generation += winners
    #make next_generation same length as organisms
    return next_generation[:len(organisms)]
    
