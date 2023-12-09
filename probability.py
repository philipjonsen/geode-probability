BASE_PROBABILITIES = {
        'common': [22, 6, 0, 0, 0, 0],
        'uncommon': [22, 15, 4, 0, 0, 0],
        'rare': [11, 25, 17, 4, 0, 0],
        'legendary': [5, 15, 30, 18, 3, 0],
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

def get_prize_rarity(random_number, probabilities):
    # random_number is a random integer between 0 and 99 (inclusive)
    # probabilities is a list of 6 integers beteween 0 and 100 (inclusive)
    # the index of the probability corresponds to the rarity of the prize
    
    # if the random number is outside the range, return None
    if random_number < 0 or random_number > 99:
        raise ValueError('random_number must be between 0 and 99 (inclusive)')

    # loop through the probabilities and add them to a cumulative sum
    # if the cumulative sum is less than the random number, return the rarity
    cumulative_sum = 0
    for i in range(len(probabilities)):
        cumulative_sum += probabilities[i]
        if random_number < cumulative_sum:
            return i

    # if the cumulative sum is still less than or equal to the random number, return None
    return None

# Test code

assert get_probabilities_based_on_num_prizes('godlike', [1,1,1,1,1,1]) == [0, 0, 0, 17, 54, 29] # full prize pool
assert get_probabilities_based_on_num_prizes('godlike', [1,1,1,1,1,0]) == [0, 0, 0, 17, 83, 0] # missing godlike prizes
assert get_probabilities_based_on_num_prizes('godlike', [1,0,0,0,0,0]) == [100, 0, 0, 0, 0, 0] # godlike geode with only common prizes
assert get_probabilities_based_on_num_prizes('common', [0,0,0,0,0,1]) == [0, 0, 0, 0, 0, 0] # common geode with only godlike prizes
assert get_probabilities_based_on_num_prizes('godlike', [0,0,0,0,0,0]) == [0, 0, 0, 0, 0, 0] # empty prize pool
assert get_probabilities_based_on_num_prizes('rare', [0,0,0,1,0,0]) == [0, 0, 0, 4, 0, 0] # rare geode with only legendary prizes
assert get_probabilities_based_on_num_prizes('godlike', [1,0,1,0,1,0]) == [0, 0, 17, 0, 83, 0]
assert get_probabilities_based_on_num_prizes('legendary', [1,0,1,0,1,0]) == [20, 0, 48, 0, 3, 0]

assert get_prize_rarity(0, [0, 0, 0, 0, 0, 0]) == None # empty prize pool
assert get_prize_rarity(99, [100, 0, 0, 0, 0, 0]) == 0 # even the highest number wins a common prize
assert get_prize_rarity(99, [0, 0, 0, 0, 0, 99]) == None # unlucky number with almost guaranteed godlike prize
assert get_prize_rarity(0, [0, 0, 0, 0, 0, 1]) == 5 # only godlike prize with lowest number
assert get_prize_rarity(50, [20, 30, 10, 0, 0, 0]) == 2  # random_number equals a cumulative probability
assert get_prize_rarity(10, [20, 30, 50, 0, 0, 0]) == 0  # random_number less than smallest probability
assert get_prize_rarity(60, [50, 30, 20, 0, 0, 0]) == 1  # probabilities not in ascending order