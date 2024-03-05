def compare_ev(odds_Agency1, odds_Agency2):

    if odds_Agency2 == 0 or odds_Agency1 == 0:
        return (0, 0, 0)
    else:
        # Calculate the percentage difference between the two odds
        percentage_difference = ((odds_Agency1 - odds_Agency2) / odds_Agency2) * 100

        # Calculate the implied probabilities of winning for each option
        probability_winning1 = 1 / odds_Agency1
        probability_winning2 = 1 / odds_Agency2

        # Return the percentage difference and the probabilities as a tuple
        return (round(percentage_difference, 3), round(probability_winning1, 3), round(probability_winning2, 3))
