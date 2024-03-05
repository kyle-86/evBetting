from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from compareEV import compare_ev as compare_ev
from betAmount import kelly_03 as kelly_03
import config

from dbUpdate import dbUpdate


def setOverUnder(linkOverUnder):
    # Start a web browser and navigate to the page

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-cache')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    try:
        # Navigate to the desired website
        driver.get(linkOverUnder)
        # time.sleep(30)
    except TimeoutException as e:
        print(f"Error: {e}")

    # Set the first cookie
    first_cookie = {'name': 'op_user_full_time_zone', 'value': '86'}
    driver.add_cookie(first_cookie)

    # Set the second cookie
    second_cookie = {'name': 'op_user_time_zone', 'value': '10'}
    driver.add_cookie(second_cookie)

    driver.refresh()

    time.sleep(5)
    # Wait for the page to load
    driver.implicitly_wait(10)  # seconds

    # Use Beautiful Soup to parse the page source
    soup = BeautifulSoup(driver.page_source, 'lxml')

    API = config.API_URL
    PARAMS = dict()

    oddsTabs = soup.find_all(
        'ul', {'class': 'visible-links bg-black-main odds-tabs flex w-full'})

    for oddsTab in oddsTabs:

        activeTab = oddsTab.select('li.active-odds')
        betType = activeTab[0].select_one('div').text

        print(betType)

        if '/' in betType:
            # Replace '/' with '_'
            betType = betType.replace('/', '_')

    team1 = soup.find('span', {
                      'class': 'max-sm:w-full order-first max-mm:!order-last truncate min-mm:!ml-auto'}).text
    team2 = soup.find('div', {
                      'class': 'flex-center items-center gap-1 min-mm:gap-2 justify-content max-mm:truncate'}).text
    
    startTime = soup.find('div', {'class': 'flex text-xs font-normal text-gray-dark font-main item-center gap-1'})
    startTime = startTime.text
    index_of_comma = startTime.index(',')
    startTime = startTime[index_of_comma + 1:].strip()
    startTime = datetime.strptime(startTime, '%d %b  %Y,%H:%M')
    print(startTime)
    startDate = startTime.strftime('%d%m%Y')
    startTime = startTime.strftime('%d%m%Y, %H:%M')

    print(team1, 'vs', team2)
    print(startTime)

    breadCrumbs = soup.find_all(
        'ul', {'class': 'max-mt:!hidden flex items-center space-x-2 px-[10px]'})

    for breadCrumb in breadCrumbs:

        info = breadCrumb.select('li')

        sport = info[1].select_one('a').text
        sport = sport.replace(" ", "")

        location = info[2].select_one('a').text
        location = location.replace(" ", "")

        league = info[3].select_one('a').text
        league = league.replace(" ", "")

        league = location + ' - ' + league


        print(sport)
        print(location)
        print(league)

        wait = WebDriverWait(driver, 10)

        elements = driver.find_elements(
            By.CSS_SELECTOR, 'div[class="border-black-borders hover:bg-gray-light flex h-9 cursor-pointer border-b border-l border-r text-xs"]')
        print(f"Found {len(elements)} elements")

        # create an instance of ActionChains
        actions = ActionChains(driver)

        for element in elements:

            eachLine = BeautifulSoup(
                element.get_attribute('innerHTML'), 'html.parser')

            currentLine = eachLine.find('p', {'class': 'max-sm:!hidden'}).text
            totalAgencies_text = eachLine.find(
                'p', {'class': 'ml-auto pr-3 text-xs font-normal'}).text
            totalAgencies = int(totalAgencies_text)

            print(totalAgencies)

            if totalAgencies > 3:

                # move to the element
                # actions.move_to_element(element).perform()
                driver.execute_script("arguments[0].scrollIntoView()", element)

                # wait for the overlay to disappear or for the accept button to appear
                try:
                    # Use a shorter timeout, e.g., 5 seconds
                    wait = WebDriverWait(driver, 5)
                    wait.until(EC.invisibility_of_element_located(
                        (By.ID, 'onetrust-policy-text')))
                except TimeoutException:
                    # If the overlay doesn't disappear, look for the accept button
                    try:
                        accept_button = driver.find_element(
                            By.CLASS_NAME, 'onetrust-accept-btn-handler')

                        # Click the accept button
                        accept_button.click()
                    except NoSuchElementException:
                        print("Accept button not found or not visible.")

                try:
                    wait = WebDriverWait(driver, 20)
                    clickable_element = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '//div[@class="border-black-borders hover:bg-gray-light flex h-9 cursor-pointer border-b border-l border-r text-xs"]')))

                    # click the element
                    clickable_element.click()
                except TimeoutException as e:
                    print(f"Timeout waiting for element to be clickable: {e}")

                sibling_elements = element.find_elements(
                    By.XPATH, 'following-sibling::div')

                # do something with the sibling elements
                for sibling_element in sibling_elements:

                    # perform some action on the sibling element
                    # actions.move_to_element(sibling_element).perform()
                    driver.execute_script(
                        "arguments[0].scrollIntoView()", sibling_element)

                    # agencies = wait.until(EC.visibility_of_element_located((By.XPATH, './/div[@class="flex text-xs border-b h-9 border-l border-r bg-gray-med_light border-black-borders border-b"]')))

                    agencies = sibling_element.find_elements(
                        By.CSS_SELECTOR, 'div.flex.text-xs.border-b.h-9.border-l.border-r.bg-gray-med_light.border-black-borders.border-b')

                    print(currentLine)

                    bet365Over = 0
                    bet365Under = 0
                    pinnacleOver = 0
                    pinnacleUnder = 0

                    for agency in agencies:

                        agency_soup = BeautifulSoup(
                            agency.get_attribute('innerHTML'), 'html.parser')

                        bookmaker = agency_soup.find(
                            'img', {'class': 'bookmaker-logo bg-cover bg-no-repeat'})['title']

                        # Home Away Odds
                        overOdds = agency_soup.find_all('div', recursive=False)[
                            2].select_one('p').text
                        underOdds = agency_soup.find_all('div', recursive=False)[
                            3].select_one('p').text

                        # if bet365
                        if bookmaker == 'bet365':
                            bet365Over = float(overOdds)
                            bet365Under = float(underOdds)

                        # if Pinnacle
                        if bookmaker == 'Pinnacle':
                            pinnacleOver = float(overOdds)
                            pinnacleUnder = float(underOdds)

                    if bet365Over > 0 and bet365Under > 0 and pinnacleOver > 0 and pinnacleUnder > 0:
                        print('Total points')
                        print(currentLine)
                        print(' - ')
                        print('bet365Over: ')
                        print(bet365Over)
                        print('pinnacleOver: ')
                        print(pinnacleOver)
                        print(' - ')
                        print('bet365Under: ')
                        print(bet365Under)
                        print('pinnacleUnder: ')
                        print(pinnacleUnder)
                        print('------')

                    if bet365Over is not None and pinnacleOver is not None and bet365Under is not None and pinnacleUnder is not None:

                        homePercentage_difference, homeProbability_winning1, homeProbability_winning2 = compare_ev(
                            bet365Over, pinnacleOver)
                        awayPercentage_difference, awayProbability_winning1, awayProbability_winning2 = compare_ev(
                            bet365Under, pinnacleUnder)
                        
                        refrenceId = team1.replace(" ", "_" ) + '_' + team2.replace(" ", "_" ) + '_' + startDate + betType + currentLine.replace(" ", "_" )
                        teams =  team1 + ' vs ' + team2
                        agency = "bet365"
                        sport = sport
                        betType = betType
                        eventTime = startTime
                        line = betType
                        betResult = ''

                        print(refrenceId)

                        if homePercentage_difference > 0:
                            betTeam = 'Over ' + currentLine
                            value = str(homePercentage_difference)
                            odds = bet365Over

                            # betValue = kelly_03(bet365Over, homeProbability_winning2, 1700)
                            print(team1 + ' vs ' + team2 + ' = ' + team1)
                            dbUpdate(refrenceId, teams, betTeam, value, eventTime, odds, agency, league, sport, betType, line, betResult)

                        elif awayPercentage_difference > 0:
                            # betValue = kelly_03(bet365Under, awayProbability_winning2, 1700)

                            betTeam = 'Under ' + currentLine
                            value = str(awayPercentage_difference)
                            odds = bet365Under
                            # betValue = kelly_03(bet365Over, homeProbability_winning2, 1700)

                            print(team1 + ' vs ' + team2 + ' = ' + team2)
                            dbUpdate(refrenceId, teams, betTeam, value, eventTime, odds, agency, league, sport, betType, line, betResult)

                        else:
                            print(team1 + ' vs ' + team2 + ' = No Value')
                            dbUpdate(refrenceId, teams, 'NA', 'no value', eventTime, 'NA', agency, league, sport, betType, line, betResult)

                    else:
                        print(team1 + ' vs ' + team2)
                        print('There are no odds yet!!')