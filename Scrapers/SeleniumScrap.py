from selenium import webdriver
from Constants import *
from time import sleep
from random import uniform, shuffle
from lxml import html
from Scrapers.commons import *

sports_with_other_markets = ['futbol']

class SeleniumScrap():
    def __init__(self):
        self.driver = webdriver.Chrome('./Drivers/chromedriver.exe')
        self.urls = [BASE_WEB + sport for sport in sports_with_other_markets]  # Set of pages to check
        shuffle(self.urls)
        self.information = {}

    def scroll_to_center_of_view(self,button):
        window_size = self.driver.get_window_size()
        self.driver.execute_script("window.scroll(" + str(window_size.get('height')) + ", " + str(
            button.location['y'] - window_size.get('width') / 2) + ");")
        sleep(uniform(0.2, 0.3))

    def get_information(self, sleep_time_min=2.5, sleep_time_max = 3.5):
        # For each url to scrap
        for url in self.urls:
            self.driver.get(url=url)
            # Wait a random time for neither overwhelm the page nor be easily detected.
            bottom_button = self.driver.find_element_by_xpath(xpath=BOTTOM_BOTH_TEAMS_WILL_SCORE_XPATH)
            self.scroll_to_center_of_view(button=bottom_button)
            bottom_button.click()
            sleep(uniform(sleep_time_min, sleep_time_max))
            sport = url[str.rfind(url, '/') + len('/'):]
            bets = parse(response=html.fromstring(html=self.driver.page_source, base_url=url))
            if bets != {}:
                self.information[sport+'-both-score'] = bets
            else:
                print("No bets found for "+sport)
        return self.information