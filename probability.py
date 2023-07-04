BASE_PROBABILITIES = {
        'common': [22, 6, 0, 0, 0, 0],
        'uncommon': [22, 15, 4, 0, 0, 0],
        'rare': [11, 25, 17, 4, 0, 0],
        'legendary': [5, 15, 3, 18, 3, 0],
        'mythical': [0, 8, 18, 38, 20, 2],
        'godlike': [0, 0, 0, 17, 54, 29]
}

def get_probabilities_based_on_num_prizes(geode_rarity, num_prizes_available):
    
    probabilities = BASE_PROBABILITIES[geode_rarity].copy()

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

assert get_probabilities_based_on_num_prizes('godlike', [1,1,1,1,1,1]) == [0, 0, 0, 17, 54, 29] # full prize pool
assert get_probabilities_based_on_num_prizes('godlike', [1,1,1,1,1,0]) == [0, 0, 0, 17, 83, 0] # missing godlike prizes
assert get_probabilities_based_on_num_prizes('godlike', [1,0,0,0,0,0]) == [100, 0, 0, 0, 0, 0] # godlike geode with only common prizes
assert get_probabilities_based_on_num_prizes('common', [0,0,0,0,0,1]) == [0, 0, 0, 0, 0, 0] # common geode with only godlike prizes
assert get_probabilities_based_on_num_prizes('godlike', [0,0,0,0,0,0]) == [0, 0, 0, 0, 0, 0] # empty prize pool
assert get_probabilities_based_on_num_prizes('rare', [0,0,0,1,0,0]) == [0, 0, 0, 4, 0, 0] # rare geode with only legendary prizes