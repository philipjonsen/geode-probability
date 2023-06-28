CUMULATIVE_PROBABILITIES = {
    'common': [0.3439, 0.1311, 0.0319, 0.0079, 0.0017, 0.0003],
    'uncommon': [0.7176, 0.3439, 0.0927, 0.0236, 0.005, 0.001],
    'rare': [0.9958, 0.8390, 0.3439, 0.0982, 0.0217, 0.0042],
    'legendary': [1, 0.9994, 0.8206, 0.3439, 0.0855, 0.0170],
    'mythical': [1, 1, 0.9997, 0.8630, 0.3439, 0.0778],
    'godlike': [1, 1, 1, 1, 0.8883, 0.3439]
}

RARITIES = list(CUMULATIVE_PROBABILITIES.keys())

def get_individual_probabilities(rarity):

    probabilities = []
    cumulative_probabilities = CUMULATIVE_PROBABILITIES[rarity]
    
    # subtract each probability from the next one to get the individual probability
    for i in range(0, len(cumulative_probabilities) - 1):
        probability = cumulative_probabilities[i] - cumulative_probabilities[i + 1]
        probabilities.append(round(probability, 4))

    # godlike probability doesn't change
    probabilities.append(round(cumulative_probabilities[-1], 4))
    return probabilities