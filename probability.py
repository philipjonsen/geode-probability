import itertools

BASE_PROBABILITIES = {
        'common': [0.2128, 0.0992, 0.024, 0.0062, 0.0014, 0.0003],
        'uncommon': [0.3737, 0.2512, 0.0691, 0.0186, 0.004, 0.001],
        'rare': [0.1568, 0.4951, 0.2457, 0.0765, 0.0175, 0.0042],
        'legendary': [0.0006, 0.1788, 0.4767, 0.2584, 0.0685, 0.017],
        'mythical': [0, 0.0003, 0.1367, 0.5191, 0.2661, 0.0778],
        'godlike': [0, 0, 0, 0.1117, 0.5444, 0.3439]
}

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

    return probabilities

# Test code

assert get_probabilities_based_on_num_prizes('godlike', [1,1,1,1,1,1]) == [0, 0, 0, 0.1117, 0.5444, 0.3439] # full prize pool
assert get_probabilities_based_on_num_prizes('godlike', [1,1,1,1,1,0]) == [0, 0, 0, 0.1117, 0.8883, 0] # missing godlike prizes
assert get_probabilities_based_on_num_prizes('godlike', [1,0,0,0,0,0]) == [1, 0, 0, 0, 0, 0] # godlik geode with only common prizes
assert get_probabilities_based_on_num_prizes('common', [0,0,0,0,0,1]) == [0, 0, 0, 0, 0, 0.0003] # common geode with only godlike prizes
assert get_probabilities_based_on_num_prizes('godlike', [0,0,0,0,0,0]) == [0, 0, 0, 0, 0, 0] # empty prize pool
assert get_probabilities_based_on_num_prizes('rare', [0,0,0,1,0,0]) == [0, 0, 0, 0.0982, 0, 0] # rare geode with only legendary prizes

# Iterate over all combinations of geode_rarity and num_prizes_available - sum of probabilities should always be the same as the sum of the base probabilities

supply_combinations = list(itertools.product([1, 0], repeat=6)) # Generate all combinations of 1 and 0 for a list of length 6

for geode_rarity, probabilities in BASE_PROBABILITIES.items():
    for num_prizes_available in supply_combinations:
        result = get_probabilities_based_on_num_prizes(geode_rarity, num_prizes_available)
        if sum(num_prizes_available) > 0:
            assert sum(result) == sum(probabilities)
        else:
            assert sum(result) == 0