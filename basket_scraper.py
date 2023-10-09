import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from game import Game


def get_basket_schedule(url):
    """
    Parameters
    ----------
    url : str
        Url for the team page in basket.fi

    Returns
    -------
        schedule : dict of Game objects with round number as key.
    """
    #options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    browser = webdriver.Chrome(service=Service('chromedriver.exe'))#, options=options)
    browser.get(url)
    #print(browser.current_url)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, '2-200-tab-1'))).click()
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, '2-200-filter-month'))).click()
    select = Select(browser.find_element(By.ID, '2-200-filter-month'))
    select.select_by_visible_text('Kaikki kuukaudet')
    time.sleep(1)
    table = browser.find_element(By.ID, '2-200-schedule-and-results-table-container').text
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, '2-200-page-2'))).click()  # Go to page 2
    time.sleep(1)
    table2 = browser.find_element(By.ID, '2-200-schedule-and-results-table-container').text
    """
    Example of table content:
    07.10.2023 17:00 Runkosarja Raholan Pyrkivä 99 : 78 Pyrintö Akatemia A Tesoman palloiluhalli V
    13.10.2023 18:30 Runkosarja Turun NMKY   Raholan Pyrkivä Nunnavuoren palloiluhalli
    """

    schedule_dict = {}
    def parse_table(table_text):
        """
        Parameters
        ----------
        table_text : str
            The content from the table element with table.text()
        """
        print(table_text)
        for i, row in enumerate(table_text.split('\n')):
            if row[-1] == 'V' or row[-1] == 'T':  # If game was already played
                continue
            p1, p2 = row.split('   ')  # Split to two parts

            gdate, gtime, phase = p1.split(' ')[0], p1.split(' ')[1], p1.split(' ')[2]
            home = ' '.join(p1.split(' ')[3:])

            away = ' '.join(p2.split(' ')[:2])  # Just take two parts for the away team name
            #print(home, "-", away)
            schedule_dict[i] = Game(i+1, None, gdate, gtime, home, away, place=None, additional=' '.join(p2.split(' ')[2:]))

    parse_table(f'{table}\n{table2}')

    browser.quit()

    return schedule_dict


# For debugging:
if __name__ == '__main__':
    schedule_dict = get_basket_schedule('https://www.basket.fi/basket/sarjat/joukkue/?team_id=4600311&season_id=127056&league_id=2')
