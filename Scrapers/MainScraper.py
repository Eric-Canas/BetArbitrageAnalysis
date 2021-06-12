from requests import get
from requests.status_codes import codes
from lxml import html
from Scrapers.commons import *

from time import sleep
from random import uniform, shuffle
from Constants import *


class BetScraper():
    """
    Class that extract all the information of oddschecker.com/es/
    """
    def __init__(self):
        self.name = "OddsChecker" #Name of the spider
        self.urls = [BASE_WEB+sport for sport in sports] #Set of pages to check
        shuffle(self.urls)
        self.information = {}

    def get_information(self, sleep_time_min=0.5, sleep_time_max=1.5):
        """
        Scrap all the information of oddschecker.com/es/ for the sports selected
        :param sleep_time_min: float. Minimum amount of seconds to wait between requests to the web
        :param sleep_time_max: float. Maximum amount of seconds to wait between requests to the web
        :return: List of Dictionaries. All the information extracted from oddschecker.com/es/ organized
        as structured and nested dictionaries
        """
        # For each url to scrap
        for url in self.urls:
            # Wait a random time for neither overwhelm the page nor be easily detected.
            sleep(uniform(sleep_time_min, sleep_time_max))
            # Make the request and get the HTML of the page
            response = get(url=url)
            # If response gets code 200 (ok)
            if response.status_code == codes['ok']:
                # Gets the name of the sport
                sport = response.url[str.rfind(response.url, '/') + len('/'):]
                # Parse the web-page to transform it to an structure structure
                result = parse(response=html.fromstring(response.content), sport=sport)
                # If it gave a valid result
                if result != {}:
                    # Save it and print an advice
                    self.information[sport] = result
                    print(sport.title() + " processed")
                # If result gave was invalid
                else:
                    # Inform about it
                    print(RuntimeError(sport.title()+" bets have no tie possibility, thus are not ensurable"))
            # If response gave an error code go to the next url
            else:
                print(ReferenceError(response.url+" gave code "+str(response.status_code)))
        if self.information == {}:
            raise ValueError("No information found in www.oddschecker.com/es/")
        return self.information