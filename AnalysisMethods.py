import numpy as np
from Constants import BETS, HOUR, HOUSES, LINK, TEAMS, DECIMALS


def analize_bet(bet):
    """
    It analize which is the value of a bet and the percentages to invest in each option for
    achieving this value
    :param bet: List of floats (or something convertible to float). List of possible bets
    :return:
    List of floats. Percentage to invest in each bet
    Float. Cost of winning a unit of money (if positive is a sure bet).
    """
    # Transform it to numpy for easier calculation
    bet = np.array(bet, dtype=np.float)
    # Check the cost of each odd (The amount of money you would need to invest to win an unit of money)
    odds_cost = 1/bet
    # Transform this cost to a percentage (The percentage that should be invested at each option)
    odd_percentage = odds_cost/np.sum(odds_cost)
    # Calculate the cost of the bet (The money that would cost to win an euro) [If positive it is a sure bet]
    total_euro_cost = 1-np.sum(odds_cost)

    return odd_percentage, total_euro_cost

def process_information(information):
    """
    Takes all the information extracted and prints all the sure bets and the general statistics
    :param information: List of dictionaries. List of dictionaries extracted from the MainScraper
    """
    sure_bets, bad_bets = [], []
    # For each sport
    for sport, days in information.items():
        # For each day
        for day, bets in days.items():
            #For each bet
            for bet in bets:
                # Get the value of the bet
                percentage, value = analize_bet(bet=bet[BETS])
                # If is sure
                if value > 0:
                    # Save it as sure and print the alert
                    sure_bets.append((value, percentage, sport, day, bet))
                    #print(get_surebet_text(sport=sport, day=day, bet=bet, percentage=percentage, value=value))
                # If not
                else:
                    # Add it to the bad bets list
                    bad_bets.append((value, percentage, sport, day, bet))
    # Print the alerts about surebets
    alert_about_all_surebets(sure_bets=sure_bets)
    # Print the summary of the analysis
    print(get_txt_summary(sure_bets=sure_bets, bad_bets=bad_bets))


def alert_about_all_surebets(sure_bets):
    """

    :param sure_bets:
    :return:
    """
    sure_bets = np.array(sure_bets, dtype=[('value', np.float), ('percentage', np.object), ('sport', '<U64'), ('day', '<U64'), ('dict', np.object)])
    sure_bets.sort(order='value')
    for sure_bet in sure_bets:
        print(get_surebet_text(sport=sure_bet['sport'], day=sure_bet['day'], bet=sure_bet['dict'],
                               percentage=sure_bet['percentage'], value=sure_bet['value']))

def get_best_credible_values(values, min_bet=5, max_bet=80):
    all_posible_bets = np.arange(start=min_bet, stop=max_bet, step=0.01, dtype=values.dtype)
    all_posible_bets = np.repeat(all_posible_bets, len(values)).reshape(-1, len(values))
    values = np.repeat(a=values, repeats=len(all_posible_bets)).reshape(len(values),-1).T
    possible_invests = values*all_posible_bets
    possible_rounded_invests = np.round(possible_invests)
    losses = np.sum(np.abs(possible_rounded_invests-possible_invests), axis=1)
    best_invest = possible_rounded_invests[np.argmin(losses)]
    return best_invest

def get_winning_range(rounded_bet, prices):
    wins = np.array(prices, dtype=np.float)*rounded_bet
    profitability = (wins/np.sum(rounded_bet))-1
    return wins, profitability

def get_surebet_text(sport, day, bet, percentage, value):
    """
    Get as human readable text all the information about a sure bet
    :param sport: str. Name of the sport
    :param day: str. String representing the day of the match
    :param bet: Dictionary. Dictionary with all the information about the match
    :param percentage: List of Floats. Percentage which should be bet to each option for achieving the value
    :param value: Float. Value of the bet
    :return:
    str. Text with all the information in a human readable format.
    """
    # Extract all the information of the bet
    teams, hour, bets, houses, link = bet[TEAMS], bet[HOUR], bet[BETS], bet[HOUSES], bet[LINK]
    best_rounded_bets = get_best_credible_values(values=percentage)
    winning_range, profitability_range = get_winning_range(rounded_bet=best_rounded_bets, prices=bets)
    # Write the advise an the information of the match
    txt = "-"*50+"\n" \
          "SURE BET FOUND! Sure win of {value}%\n" \
          "In {sport}, on the match of {day} at {hour}: " \
          "{teams}.\n".format(value=str(np.round(value*100, decimals=DECIMALS)),sport=sport,
                                          day=day, hour=hour, teams=' vs'.join(teams))
    # Write the summarized information of the bets including best values and houses
    txt += "Best bets are: {bet1} ({house1}) - ".format(bet1=bets[0], house1=houses[0])
    if len(bets) == 3:
        txt += "{betdraw} ({housedraw}) - ".format(betdraw=bets[1], housedraw=houses[1])
    txt += "{bet2} ({house2}).".format(bet2=bets[-1], house2=houses[-1])
    if 'both-score' in sport:
        teams[0], teams[1] = 'Yes', 'No'
    # Write the details of the teams which each bet corresponds to.
    txt += "\n({team1} - {betteam1}, ".format(team1=teams[0], betteam1=str(bets[0]))
    if len(bets) == 3:
        txt += "Draw - {drawvalue}, ".format(drawvalue=bets[1])
    txt += "{team2} - {betteam2})\n".format(team2=teams[-1], betteam2=str(bets[-1]))
    # Write the percentages which should be bet to each option
    txt += "You should bet {percentage1}% to {team1}, "\
        .format(percentage1=str(np.round(percentage[0]*100, decimals=DECIMALS)), team1=teams[0])
    if len(percentage) == 3:
        txt += "{percentagedraw}% to Draw, " \
            .format(percentagedraw=str(np.round(percentage[1] * 100, decimals=3)))
    txt += "{percentage2}% to {team2}\n" \
        .format(percentage2=str(np.round(percentage[-1] * 100, decimals=3)), team2=teams[-1])

    txt += "Best rounded bets: {roundedbet1}€ - ".format(roundedbet1=best_rounded_bets[0])
    if len(best_rounded_bets) == 3:
        txt += "{roundedbetdraw}€ - ".format(roundedbetdraw=best_rounded_bets[1])
    txt += "{roundedbet2}€. ".format(roundedbet2=best_rounded_bets[-1], team2=teams[-1])
    txt += "[Total bet: {total}€].\n".format(total=np.sum(best_rounded_bets))

    txt += "Profits range: {winning1}€ ({profit1}%) - "\
                    .format(winning1=np.round(winning_range[0] - np.sum(best_rounded_bets), decimals=DECIMALS),
                    profit1=np.round(profitability_range[0] * 100, decimals=DECIMALS))
    if len(winning_range) == 3:
        txt += "{winningdraw}€ ({profitdraw}%) - " \
            .format(winningdraw=np.round(winning_range[1] - np.sum(best_rounded_bets), decimals=DECIMALS),
                    profitdraw=np.round(profitability_range[1] * 100, decimals=DECIMALS))
    txt += "{winning2}€ ({profit2}%).\n" \
        .format(winning2=np.round(winning_range[-1] - np.sum(best_rounded_bets), decimals=DECIMALS),
                profit2=np.round(profitability_range[-1] * 100, decimals=DECIMALS))

    # Write the hyperlink for manually examining the information on oddschecker.
    txt += "Information extracted from {hyperlink}.\n".format(hyperlink=link)
    txt += "-" * 50 + "\n"
    return txt

def get_txt_summary(sure_bets, bad_bets):
    """
    Gets a text sumarizing the analysis performed
    :param sure_bets: List of tuples. Value of the sure bets and dictionary of each sure bet
    :param bad_bets: List of tuples. Value of the bad bets and dictionary of each bad bet
    :return: Str. Text to print defining the analysis
    """
    # Fuse the bets as structured array, for doing sorts by value
    allbets = np.array(sure_bets+bad_bets, dtype=[('value', np.float), ('percentage', np.object), ('sport', '<U64'), ('day', '<U64'), ('dict', np.object)])
    # Generates the text with the statistics.
    txt = '-'*50+'\n'
    txt+= "Bets analyzed: {totalbets}\n" \
          "Sure bets found: {surebets}\n" \
          "Bad bets found: {badbets}\n" \
          "Best value found {bestvalue}%".format(totalbets=len(sure_bets)+len(bad_bets), surebets=len(sure_bets),
                                                badbets=len(bad_bets),
                                                bestvalue=np.round(np.max(allbets['value'])*100, decimals=DECIMALS))
    return txt