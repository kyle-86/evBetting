from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime

from gameTime import gameTime as gameTime
from setTimeZone import setTime as setTime
from setH2H import setH2H as setH2H
from setOverUnder import setOverUnder as setOverUnder


# def getGameInfo(url, linkOverUnder):
def getGameInfo(url):
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
    except TimeoutException as e:
        print(f"Error: {e}")
        # Continue to the next iteration in case of an exception
        return

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

        
        team1 = soup.find('span', {'class': 'max-mm:!order-last min-mm:!ml-auto order-first truncate max-sm:w-full'}).text
        team2 = soup.find('div', {'class': 'flex-center min-mm:gap-2 justify-content max-mm:truncate items-center gap-1'}).text

        print(team1, 'vs', team2)

        startTime = soup.find('div', {'class': 'text-gray-dark font-main item-center flex gap-1 text-xs font-normal'})
        startTime = startTime.text

        # Split the text into separate lines and extract the date and time parts
        date_part, time_part = map(str.strip, startTime.split(',')[1:])

        # Combine date and time parts into a single string
        start_time_str = f"{date_part} {time_part}"

        # Use the correct format string for the datetime.strptime
        startTime = datetime.strptime(start_time_str, '%d %b %Y %H:%M')
        print(startTime)

        # print(startTime)
        startDate = startTime.strftime('%d%m%Y')
        startTime = startTime.strftime('%d%m%Y, %H:%M')


        # startTime = startTime.find_next_sibling("div").text
        # startTime = startTime.split(',', 1)[1].strip()

        # print(startTime)

        # days, hours, minutes, seconds, countdown = gameTime(startTime)
            
        head2Head = setH2H(soup, team1, team2, startDate, startTime)
        # setOverUnder(soup, team1, team2, startTime, linkOverUnder)

    except Exception as e:
        print(f"An error occurred: {e} url: {url}")

    
    finally:
        # Close the browser
        driver.close()