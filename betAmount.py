def kelly_03(odds, probability_of_winning, bankroll):
    """
    Calculate the actual bet amount using the .3 Kelly betting strategy.
    :param odds: The decimal odds of the bet
    :param probability_of_winning: The probability of winning the bet
    :param bankroll: The total bankroll available
    :return: The actual bet amount
    """
    odds = float(odds)
    probability_of_winning = float(probability_of_winning) / 100
    bankroll = int(bankroll)

    # print(odds)
    # print(probability_of_winning)
    # print(bankroll)

    probability_of_losing = 1 - probability_of_winning
    fraction = 0.030 * ((odds * probability_of_winning) - probability_of_losing) / odds
    bet_amount = fraction * bankroll

    return round(bet_amount)