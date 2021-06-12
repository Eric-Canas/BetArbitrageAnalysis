from Constants import *
import numpy as np

#Defining the sports which information is easily computable
sports = ['tenis-mesa/tenis-de-mesa', 'e-sports', 'baloncesto',
          'rugby', 'tenis', 'futbol-americano', '/boxeo-mma/boxeo',
          'boxeo-mma/ufc-mma', 'futbol']
# Defining sports where draw is not possible
sports_with_no_draw = ['tenis-de-mesa', 'baloncesto', 'tenis', 'e-sports']

def parse(response, sport='Some sport'):
    """
    Parse the content of the HTML and transform it to an structured dictionary
    :param response: HTML response. Web-page HTML downloaded
    :return: Dictionary. Structured dictionary with the response
    """
    # Take the different boxes containing each day matches
    each_day_matches = response.xpath(MATCHES_XPATH)
    # If it was an error in the web-page return an empty dict
    if len(each_day_matches) == 0:
        return {}
    # Extract the date of each of those matches
    dates = [str(valid_match.xpath(DAY_OF_MATCH_XPATH+'/text()')[0]) for valid_match in each_day_matches]
    #Transform to an organized list of selectors with one response by each match
    table_of_days = {}
    for day, day_matches in zip(dates, each_day_matches):
        if day in table_of_days:
            table_of_days[day].extend(day_matches.xpath(TABLE_OF_DAY_XPATH))
        else:
            table_of_days[day] = day_matches.xpath(TABLE_OF_DAY_XPATH)
    # Get the count of how many bets where incomplete
    discarded = 0
    # For each day check all its matches
    for day, matches in table_of_days.items():
        # For each match
        for i, match in enumerate(matches):
            # Extract all information from the bet
            hour = str(match.xpath(HOUR_OF_MATCH_XPATH+'/text()')[0])
            teams = [str(team) for team in match.xpath(TEAMS_XPATH+'/text()')]
            bets = [str(bet) for bet in match.xpath(BETS_XPATH+'/text()')]
            houses = [get_house_name(str(house)) for house in match.xpath(HOUSE_XPATH)]
            link = match.xpath(LINK_XPATH)[0]

            # Check if it have any incomplete information
            try:
                np.array(bets, dtype=np.float)
            except:
                # If the error was because draw was invalid in a no draw sport. Erase the invalid draw
                if sport in sports_with_no_draw:
                    bets = [bets[0], bets[-1]]
                else:
                    table_of_days[day][i] = INCOMPLETE_INFO
                    discarded += 1
                    continue
                # Check if there is any additional incomplete information
                try:
                    np.array(bets, dtype=np.float)
                except:
                    # In that case fill it as incomplete info
                    #print(ValueError("Information not complete for "+sport+" match: "+str(' vs'.join(teams))+" -- Bets = "+str(bets)))
                    table_of_days[day][i] = INCOMPLETE_INFO
                    discarded += 1
                    continue

            # Compose and save the bet
            bet = {HOUR:hour, TEAMS:teams, BETS:bets, HOUSES:houses, LINK:link}
            table_of_days[day][i] = bet
    # Clean the incomplete information of the dictionary
    table_of_days = clean_dictionary(table_of_days)
    # If any bet was discarded print the information about how many were discarded
    if discarded > 0:
        print("Discarded "+str(discarded)+" bets in "+sport+" by incomplete information.")
    return table_of_days

def clean_dictionary(dictionary):
    """
    Clean the dictionary of the incomplete information that it could contain
    :param dictionary: Dictionary. Dictionary containing all the bets of a sport
    :return: Dictionary. The input dictionary cleared
    """
    # Erase all the cases which contained incomplete information
    dictionary = {date : [{key : value for key, value in match.items()}
                        for match in matches if match != INCOMPLETE_INFO]
                            for date, matches in dictionary.items()}
    # Clean all the dates which ended up by not containing any day
    dictionary = {date : matches for date, matches in dictionary.items() if len(matches)>0}
    return dictionary

def get_house_name(house_class):
    """
    Translate the betting house class code to the human readable name of the house
    :param house_class: Complete class name of the div where the best house was encoded
    :return: str. The human readable name of the house or houses offering the best price.
    """
    # Extract the from the complete code the concrete code of the house
    house_codes = house_class[len(HOUSE_CLASS_1 + ' bg'):-len('-ES')].replace(',', ' ').split()
    try:
        # Translate it to human readable code
        house_names = ' or '.join([HOUSE_CODE[code] for code in house_codes])
        return house_names
    except:
        # If the code was not known alert about it and return the str with that information
        house_alert = 'Unknown-House-Code('+str(house_codes)+')'
        print(house_alert)
        return house_alert