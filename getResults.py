from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime
import config
from dateutil import parser

import requests

from setOverUnder import setOverUnder as setOverUnder

from dbUpdate import dbUpdate

def getResults(url):
    # Start a web browser and navigate to the page
    # Create a Chrome driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-cache')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the desired website
        driver.get(url)
    except TimeoutException  as e:
        print(f"Error: {e}")

    # Set the first cookie
    first_cookie = {'name': 'op_user_full_time_zone', 'value': '86'}
    driver.add_cookie(first_cookie)

    # Set the second cookie
    second_cookie = {'name': 'op_user_time_zone', 'value': '10'}
    driver.add_cookie(second_cookie)

    for _ in range(5):  # Scroll 5 times (adjust as needed)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for a brief moment after scrolling to give time for content to load
        time.sleep(2)

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.border-black-borders.group.flex.border-l.border-r')))
    
    # Use Beautiful Soup to parse the page source
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # border-black-borders flex cursor-pointer flex-col border-b

    # Find the table with the upcoming games
    allGames = soup.find_all('div', {'class': 'eventRow flex w-full flex-col text-xs'})
    count = 0
    totalCount = len(allGames)
    matchDate = ''

    for eachGame in allGames:

        matchDate_element = eachGame.find('div', {'class': 'text-black-main font-main w-full truncate text-xs font-normal leading-5'})

        if matchDate_element:
            matchDate = matchDate_element.text

        print(matchDate)
  
        team_elements = eachGame.find_all('p', class_='participant-name truncate')

        if len(team_elements) >= 2:
            team1 = team_elements[0].text
            team2 = team_elements[1].text
        else:
            print("Error: Less than two team elements found.")

        parsed_date = parser.parse(matchDate, fuzzy=True)
        # Format the date as %d%m%Y
        formatted_date = parsed_date.strftime("%d%m%Y")
    
        refrenceId = team1.replace(" ", "_" ) + '_' + team2.replace(" ", "_" ) + '_' + formatted_date

        print(refrenceId)

        gameScores = eachGame.find('div', class_='flex gap-1 font-bold font-bold')
        
        # gameResult = eachGame.find('div', {'class': 'ml-[2px] font-semibold'})
        # gameStatus = gameResult.text

        if gameScores is not None and hasattr(gameScores, 'find_all'):

            score_divs = gameScores.find_all('div')

            if len(score_divs) >= 2:

                homeScore = score_divs[0].text
                awayScore = score_divs[-1].text

                # # Print the extracted values
                # print("Game Status:", gameStatus)
                # print("Current Score:", currentScore)
                # print("First Half:", firstHalfScore)
                # print("Second Half:", secondHalfScore)
                # print("refrenceId:", refrenceId)

                winner = None  # Default value for the winner

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

                matchTypes = ['Home_Away', '1X2']

                for matchType in matchTypes:
                    if existing_entries:
                        dbUpdate(refrenceId + matchType, teams=None, betTeam=None, value=None, eventTime=None, odds=None, agency=None, league=None, sport=None, betType=None, line=None, betResult=winner)


# getResults('https://www.oddsportal.com/hockey/finland/mestis/results')
# getResults('https://www.oddsportal.com/hockey/switzerland/national-league/results')
# getResults('https://www.oddsportal.com/football/switzerland/super-league/results')
# getResults('https://www.oddsportal.com/hockey/usa/nhl/results')
# getResults('https://www.oddsportal.com/american-football/usa/nfl/results')
# getResults('https://www.oddsportal.com/basketball/usa/ncaa/results')
# getResults('https://www.oddsportal.com/basketball/usa/nba/results')
# getResults('https://www.oddsportal.com/hockey/usa/ahl/results')
# getResults('https://www.oddsportal.com/football/australia/a-league/results')
# getResults('https://www.oddsportal.com/football/germany/2-bundesliga/results')

getResults('https://www.oddsportal.com/basketball/usa/ncaa/results/#/page/2')
getResults('https://www.oddsportal.com/basketball/usa/ncaa/results/#/page/3')
getResults('https://www.oddsportal.com/basketball/usa/ncaa/results/#/page/4')
getResults('https://www.oddsportal.com/basketball/usa/ncaa/results/#/page/5')
getResults('https://www.oddsportal.com/basketball/usa/ncaa/results/#/page/6')
