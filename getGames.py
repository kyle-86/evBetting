from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from getGameInfo import getGameInfo as getGameInfo
from setOverUnder import setOverUnder as setOverUnder
# from getResults import getResults as getResults
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
from dateutil import parser
import time

def get_games(URL):
    # Start a web browser and navigate to the page
    # Create a Chrome driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-cache')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the desired website
        driver.get(URL)
    except TimeoutException  as e:
        print(f"Error: {e}")
    
    # Set the first cookie
    first_cookie = {'name': 'op_user_full_time_zone', 'value': '86'}
    driver.add_cookie(first_cookie)

    # Set the second cookie
    second_cookie = {'name': 'op_user_time_zone', 'value': '10'}
    driver.add_cookie(second_cookie)

    for _ in range(4):  # Scroll 5 times (adjust as needed)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for a brief moment after scrolling to give time for content to load
        time.sleep(5)

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.border-black-borders.group.flex.border-l.border-r')))
    
    # Use Beautiful Soup to parse the page source
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # next-m:flex next-m:!mt-0 ml-2 mt-2 min-h-[32px] w-full hover:cursor-pointer

    # Find the table with the upcoming games
    allGames = soup.find_all('div', {'class': 'eventRow flex w-full flex-col text-xs'})
    count = 0
    allMatches = soup.find_all('a', {'class': 'next-m:flex next-m:!mt-0 ml-2 mt-2 min-h-[32px] w-full hover:cursor-pointer'})
    totalCount = len(allMatches)

    print(totalCount)
    matchDate = ''
    if totalCount > 0:
        for eachGame in allGames:

            matchDate_element = eachGame.find('div', {'class': 'text-black-main font-main w-full truncate text-xs font-normal leading-5'})

            if matchDate_element:
                matchDate = matchDate_element.text

                parsed_date = parser.parse(matchDate, fuzzy=True)

                # Check if the parsed date is within the current date
                current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                time_difference = abs(parsed_date - current_date)
                within_48_hours = time_difference.total_seconds() <= 48 * 3600
                within_72_hours = time_difference.total_seconds() <= 72 * 3600

            if within_48_hours:
                allEvents = eachGame.find_all('a', {'class': 'next-m:flex next-m:!mt-0 ml-2 mt-2 min-h-[32px] w-full hover:cursor-pointer'})
                
                for event in allEvents:

                    count += 1
                    link = event.find('a')['href']
                    link = link[:-1]

                    gameLink = 'https://www.oddsportal.com' + link
                    # linkHomeAway = 'https://www.oddsportal.com' + link + '#home-away;1'
                    linkOverUnder = 'https://www.oddsportal.com' + link + '#over-under'
                    # getScores = 'https://www.oddsportal.com' + link

                    beenPlayed = event.find('div', {'class': 'flex gap-1 font-bold font-bold'})
                    
                    teamOdds = event.find_all('div', {'class': 'flex-center border-black-main min-w-[60px] max-w-[60px] flex-col gap-1 border-l border-opacity-10'})

                    skip_remaining = False

                    for teamOdd in teamOdds:

                        oddsAvailable = teamOdd.text

                        # print (oddsAvailable)

                        if oddsAvailable == '-':
                            print('No odds found')
                            skip_remaining = True
                            break
                    
                    if skip_remaining:
                        continue

                    if not beenPlayed :
                        getGameInfo(gameLink)
                        # setOverUnder(linkOverUnder)

                    # if beenPlayed :
                        # getResults(getScores)
                        # getResults(gameLink)

                    print(count, 'of', totalCount)
            else:
                print('over 2 days time')

            # print(matchDate)
        
    # Close the browser
    driver.close()

# while True:
#     current_hour = time.localtime().tm_hour

# get_games('https://www.oddsportal.com/football/bulgaria/parva-liga') # 17th Feb
# get_games('https://www.oddsportal.com/football/europe/champions-league/')
# get_games('https://www.oddsportal.com/football/england/premier-league')
get_games('https://www.oddsportal.com/hockey/finland/mestis')
get_games('https://www.oddsportal.com/hockey/switzerland/national-league')
get_games('https://www.oddsportal.com/football/switzerland/super-league')
get_games('https://www.oddsportal.com/hockey/usa/nhl')
get_games('https://www.oddsportal.com/american-football/usa/nfl')
get_games('https://www.oddsportal.com/basketball/usa/ncaa')
get_games('https://www.oddsportal.com/basketball/usa/nba')
get_games('https://www.oddsportal.com/hockey/usa/ahl')
get_games('https://www.oddsportal.com/football/australia/a-league')
get_games('https://www.oddsportal.com/football/germany/2-bundesliga')

print('completed checking for EV bets')

    # get_games('https://www.oddsportal.com/football/england/fa-cup/')
    

    # time.sleep(100)  # 7200 seconds = 2 hour 