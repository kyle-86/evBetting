from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import config

import requests

from setOverUnder import setOverUnder as setOverUnder

from dbUpdate import dbUpdate

def getResults(url):
    print(url)
    # Start a web browser and navigate to the page

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-cache')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    try:
        # Navigate to the desired website
        driver.get(url)
        # time.sleep(30)
    except TimeoutException  as e:
        print(f"Error: {e}")

    try:    

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

        team1 = soup.find('span', {'class': 'max-sm:w-full order-first max-mm:!order-last truncate min-mm:!ml-auto'}).text
        team2 = soup.find('div', {'class': 'flex-center items-center gap-1 min-mm:gap-2 justify-content max-mm:truncate'}).text

        # print(team1)
        # print('vs')
        # print(team2)

        oddsTabs = soup.find_all(
            'ul', {'class': 'no-scrollbar flex h-10 overflow-x-auto hide-menu'})

        for oddsTab in oddsTabs:

            activeTab = oddsTab.select('li.active-odds')
            betType = activeTab[0].select_one('div').text

            if '/' in betType:
            # Replace '/' with '_'
                betType = betType.replace('/', '_')

        startTime = soup.find('div', {'class': 'flex text-xs font-normal text-gray-dark font-main item-center gap-1'})
        startTime = startTime.text
        index_of_comma = startTime.index(',')
        startTime = startTime[index_of_comma + 1:].strip()
        startTime = datetime.strptime(startTime, '%d %b  %Y,%H:%M')
        # print(startTime)
        startDate = startTime.strftime('%d%m%Y')
        startTime = startTime.strftime('%d%m%Y, %H:%M')

        gameScores = soup.find('div', {'class': 'relative px-[12px] flex max-mm:flex-col w-auto min-sm:w-full pb-5 pt-5 min-mm:items-center font-semibold text-[22px] text-black-main gap-2 border-b border-[1px solid rgba(0, 0, 0, 0.12)] font-secondary'})
        # theScore = gameScores.find('div', {'class': 'flex flex-wrap'})

        # Extract values from theScore
        # gameStatus = theScore.text
        # currentScore = theScore.find('strong').text
        # halfBreakdown = theScore.text.split('(')[-1].split(')')[0]

        # split_text = halfBreakdown.replace('\xa0', ' ')
        # split_text = split_text.split(',')
        # firstHalfScore = split_text[0].strip()
        # secondHalfScore = split_text[1].strip()

        refrenceId = team1.replace(" ", "_" ) + '_' + team2.replace(" ", "_" ) + '_' + startDate + betType

        print(refrenceId)

        gameResult = soup.find('div', {'class': 'flex max-sm:gap-2'})
        gameStatus = gameResult.text

        homeScore = gameScores.find('div', {'class': 'flex flex-wrap w-full gap-2 text-gray-dark'}).text
        awayScore = gameScores.find('div', {'class': 'flex order-first max-mm:order-last max-mm:gap-2'}).text

        # # Print the extracted values
        # print("Game Status:", gameStatus)
        # print("Current Score:", currentScore)
        # print("First Half:", firstHalfScore)
        # print("Second Half:", secondHalfScore)
        # print("refrenceId:", refrenceId)

        winner = None  # Default value for the winner

        if "Final" in gameStatus:
            home_num = int(homeScore)
            away_num = int(awayScore)

            if home_num > away_num:
                winner = team1
            elif home_num < away_num:
                winner = team2
            else:
                winner = "Draw"

        print('The winner was:', winner)

        API = config.API_URL

        existing_entry_check = requests.get(API, params={"refrenceId": refrenceId})
        existing_entries = existing_entry_check.json()

        if existing_entries:
            dbUpdate(refrenceId, teams=None, betTeam=None, value=None, eventTime=None, odds=None, agency=None, league=None, sport=None, betType=None, line=None, betResult=winner)

    except Exception as e:
        print(f"An error occurred: {e} url: {url}")

    
    finally:
        # Close the browser
        driver.close()