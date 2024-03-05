from compareEV import compare_ev as compare_ev
from betAmount import kelly_03 as kelly_03
import requests
import config

def get_homeAway(soup, team1, team2, startTime):

    API = config.API_URL
    PARAMS = dict()

    bet365Home = 0
    bet365Away = 0
    pinnacleHome = 0
    pinnacleAway = 0

    oddsTabs = soup.find_all(
        'ul', {'class': 'flex w-full h-10 overflow-auto visible-links bg-black-main odds-tabs'})

    for oddsTab in oddsTabs:

        activeTab = oddsTab.select('li.active-odds')
        betType = activeTab[0].select_one('div').text


    uls = soup.find_all(
        'ul', {'class': 'flex px-[10px] space-x-2 items-center'})

    for li in uls:

        info = li.select('li')

        sport = info[4].select_one('a').text
        sport = sport.replace(" ", "")

        location = info[6].select_one('a').text
        location = location.replace(" ", "")

        league = info[8].select_one('a').text
        league = league.replace(" ", "")

    # each odds line on Home/Away Line
    divs = soup.find_all('div', {'class': 'flex text-xs border-b h-9'})
       
    for div in divs:

        bookmaker = div.find(
            'img', {'class': 'bg-no-repeat bg-cover bookmaker-logo'})
        bookmaker = bookmaker['title']

        # Home Away Odds
        TeamOdds = div.select('.flex.flex-col.items-center.justify-center.gap-1')

        homeOdds = TeamOdds[0].select_one('p').text

        print(homeOdds)

        if betType == '1x2':
            drawOdds = TeamOdds[1].select_one('p').text
            awayOdds = TeamOdds[2].select_one('p').text
        else:
            drawOdds = 0
            awayOdds = TeamOdds[1].select_one('p').text

        # if bet365
        if bookmaker == 'bet365':
            bet365Home = float(homeOdds)
            bet365Draw = float(drawOdds)
            bet365Away = float(awayOdds)

        # if Pinnacle
        if bookmaker == 'Pinnacle':
            pinnacleHome = float(homeOdds)
            pinnacleDraw = float(drawOdds)
            pinnacleAway = float(awayOdds)

    homePercentage_difference = 0
    awayPercentage_difference = 0

    # print(bet365Home)
    # print(pinnacleHome)
    # print(bet365Away)
    # print(pinnacleAway)

    if bet365Home and pinnacleHome and bet365Away and pinnacleAway:

        homePercentage_difference, homeProbability_winning1, homeProbability_winning2 = compare_ev(
            bet365Home, pinnacleHome)
        awayPercentage_difference, awayProbability_winning1, awayProbability_winning2 = compare_ev(
            bet365Away, pinnacleAway)

        if homePercentage_difference > 0:

            betValue = kelly_03(bet365Home, homeProbability_winning2, 1700)

            PARAMS["refrenceId"] = team1 + ' vs ' + team2
            PARAMS["teams"] = team1 + ' vs ' + team2
            PARAMS["betTeam"] = team1
            PARAMS["value"] = str(homePercentage_difference) + '%'
            PARAMS["eventTime"] = startTime
            PARAMS["odds"] = bet365Home
            PARAMS["agency"] = "bet365"
            PARAMS["league"] = location + ' - ' + league
            PARAMS["sport"] = sport
            PARAMS["betType"] = betType

            # sending get request and saving the response as response object
            r = requests.post(url = API, json = PARAMS)
            
            # extracting data in json format
            data = r.json()

            print('Added to API - Team 1')

        elif awayPercentage_difference > 0:
            betValue = kelly_03(bet365Away, awayProbability_winning2, 1700)

            PARAMS["refrenceId"] = team1 + ' vs ' + team2
            PARAMS["teams"] = team1 + ' vs ' + team2
            PARAMS["betTeam"] = team2
            PARAMS["value"] = str(awayPercentage_difference) + '%'
            PARAMS["eventTime"] = startTime
            PARAMS["odds"] = bet365Away
            PARAMS["agency"] = "bet365"
            PARAMS["league"] = location + ' - ' + league
            PARAMS["sport"] = sport
            PARAMS["betType"] = betType

            print(team2)

            # sending get request and saving the response as response object
            r = requests.post(url = API, json = PARAMS)
            
            # extracting data in json format
            data = r.json()

            print('Added to API - Team 2')

        # else:
        #     print(team1 + ' vs ' + team2)
        #     print('There is a negative Expected ROI')

    # else:
    #     print(team1 + ' vs ' + team2)
    #     print('There are no odds yet!!')
