from AnalysisMethods import process_information
from Scrapers.MainScraper import BetScraper
from Scrapers.SeleniumScrap import SeleniumScrap

# Scrap all the information of the web
information = BetScraper().get_information(sleep_time_min=1.0, sleep_time_max=2.0)
# Process it for finding sure bets
print('-'*50+'\nWin - Draw - Loss')
process_information(information=information)

try:
    information = SeleniumScrap().get_information()
    print('-'*50+'\nBoth Teams will score')
    process_information(information=information)
except:
    print("Information about 'Both teams will score' could not be extracted")

