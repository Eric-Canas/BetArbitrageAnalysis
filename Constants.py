BASE_WEB = "https://www.oddschecker.com/es/"

# Keys for data dictionary
BETS = 'bets'
HOUR = 'hour'
LINK = 'link'
TEAMS = 'teams'
HOUSES = 'houses'

# Internal values
DECIMALS = 2

INCOMPLETE_INFO = 'incomplete info'

# HOUSES
HOUSE_CODE = {'B3': 'Bet365', 'PS': 'Bet-Stars', 'WA': 'Betway-Sports', 'FS': 'Betfair',
              'XS': 'Betfair-Exchange', 'EE':'888-Sport', 'LU': 'Luckya', 'UM': 'Sportium',
              'M1': 'Marathon-Bet', 'MC': 'Marca-Apuestas', 'WH': 'William-Hill', 'WS': 'Bwin'}

# CLASS CODES OF THE WEB
PRINCIPAL_COMPETITIONS = '_2D9z5o'
EACH_DAY = '_2nWFsl'

HEADER_OF_MATCH = '_2x2ato'
DAY_OF_MATCH = '_1svvs0'

TABLE_OF_DAY = '_2zQ8KU'
ENTRY_OF_DAY = '_3f0k2k '

HOUR_OF_MATCH = '_1ob6_g'

TEAM = '_2tehgH'

BETS_DIV = '_1_WXMs'
PRICE = '_1NtPy1'

HOUSE_CLASS_1 = '_2Fd57i'
HOUSE_EXCLUSION = '_3fM9dR'

MORE_PRICES_LINK = '_1V7UJb'

# XPATHS TO PARSE
MATCHES_XPATH = '//div[@class="{competitions}"]//div[@class="{ofday}"]'.format(competitions=PRINCIPAL_COMPETITIONS, ofday=EACH_DAY)
DAY_OF_MATCH_XPATH = './div[@class="{header}"]//div[@class="{day}"]'.format(header=HEADER_OF_MATCH, day=DAY_OF_MATCH)
TABLE_OF_DAY_XPATH = './ul[@class="{table}"]//li[@class="{entry}"]'.format(table=TABLE_OF_DAY, entry=ENTRY_OF_DAY)
HOUR_OF_MATCH_XPATH = './/div[@class="{hour}"]'.format(hour=HOUR_OF_MATCH)
TEAMS_XPATH = './/div[@class="{team}"]'.format(team=TEAM)
BETS_XPATH = './/div[@class="{betplace}"]//div[@class="{price}"]'.format(betplace=BETS_DIV, price=PRICE)
HOUSE_XPATH = './/button/div[@class!="{nothouse}"]/@class'.format(nothouse=HOUSE_EXCLUSION)
LINK_XPATH = './/a[@class="{link}"]//@href'.format(link=MORE_PRICES_LINK)

# SELENIUM CLASS CODES
CHANGE_MARKET = "eNQgkw"
BOTTOM_CHANGE_MARKET_BUTTON = "kCBJkO"
BOTH_TEAMS_WILL_SCORE_TEXT = "Ambos equipos marcarán"

# SELENIUM XPATHS
CHANGE_MARKET_BUTTON_XPATH = '//div[@class="{changenmarket}"]'.format(changenmarket=CHANGE_MARKET)
BOTTOM_BOTH_TEAMS_WILL_SCORE_XPATH = '//div[@class="{button}"]/span[contains(text(),"{bothteamstext}")]'\
    .format(button=BOTTOM_CHANGE_MARKET_BUTTON, bothteamstext=BOTH_TEAMS_WILL_SCORE_TEXT)