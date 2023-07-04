import itertools

BASE_PROBABILITIES = {
        'common': [0.22, 0.06, 0, 0, 0, 0],
        'uncommon': [0.22, 0.15, 0.04, 0, 0, 0],
        'rare': [0.11, 0.25, 0.17, 0.04, 0, 0],
        'legendary': [0.05, 0.15, 0.3, 0.18, 0.03, 0],
        'mythical': [0, 0.08, 0.18, 0.38, 0.2, 0.02],
        'godlike': [0, 0, 0, 0.17, 0.54, 0.29]
}

def round_list_of_floats(list_of_floats, precision):
    return [round(x, precision) for x in list_of_floats]

def get_probabilities_based_on_num_prizes(geode_rarity, num_prizes_available):
    
    probabilities = BASE_PROBABILITIES[geode_rarity]

    # loop backwards through the probabilities - godlike to uncommon
    # if there aren't prizes available, add the probability to the next lower rarity and set that probability to zero
    for i in range(len(probabilities) - 1, 0, -1):
        if (num_prizes_available[i] == 0):
            probabilities[i - 1] += probabilities[i]
            probabilities[i] = 0
    
    # for common, just set it to zero if there are no prizes available
    if num_prizes_available[0] == 0:
        probabilities[0] = 0

    return round_list_of_floats(probabilities, 2) # only rounding here for the sake of the test code

# Test code

assert get_probabilities_based_on_num_prizes('godlike', [1,1,1,1,1,1]) == [0, 0, 0, 0.17, 0.54, 0.29] # full prize pool
assert get_probabilities_based_on_num_prizes('godlike', [1,1,1,1,1,0]) == [0, 0, 0, 0.17, 0.83, 0] # missing godlike prizes
assert get_probabilities_based_on_num_prizes('godlike', [1,0,0,0,0,0]) == [1, 0, 0, 0, 0, 0] # godlike geode with only common prizes
assert get_probabilities_based_on_num_prizes('common', [0,0,0,0,0,1]) == [0, 0, 0, 0, 0, 0] # common geode with only godlike prizes
assert get_probabilities_based_on_num_prizes('godlike', [0,0,0,0,0,0]) == [0, 0, 0, 0, 0, 0] # empty prize pool
assert get_probabilities_based_on_num_prizes('rare', [0,0,0,1,0,0]) == [0, 0, 0, 0.04, 0, 0] # rare geode with only legendary prizes

# Iterate over all combinations of geode_rarity and num_prizes_available - sum of probabilities should always be the same as the sum of the base probabilities

supply_combinations = list(itertools.product([1, 0], repeat=6)) # Generate all combinations of 1 and 0 for a list of length 6

for geode_rarity, probabilities in BASE_PROBABILITIES.items():
    for num_prizes_available in supply_combinations:
        result = get_probabilities_based_on_num_prizes(geode_rarity, num_prizes_available)
        if sum(num_prizes_available) > 0:
            assert round(sum(result),2) == round(sum(probabilities),2)
        else:
            assert sum(result) == 0