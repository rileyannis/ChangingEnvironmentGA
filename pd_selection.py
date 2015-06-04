import pd_tournament

def get_best_half(paired_organism_payouts):
    """
    This will run a tournament with the given organisms and
    return a list of the top half of the organisms in terms of payout
    """
    sorted_pairs = sorted(paired_organism_payouts, key=lambda pair: pair[1], reverse=True)
    best_half_pairs = sorted_pairs[:len(paired_organism_payouts) // 2]
    return [org for org, _ in best_half_pairs]
    

    
    
