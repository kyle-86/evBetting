from compareEV import compare_ev as compare_ev
from betAmount import kelly_03 as kelly_03
from dbUpdate import dbUpdate


def setH2H(soup, team1, team2, startDate, startTime):

    betType = ''  # Initialize betType with a default value

    bet365Home = 0
    bet365Draw = 0
    bet365Away = 0
    pinnacleHome = 0
    pinnacleDraw = 0
    pinnacleAway = 0

    oddsTabs = soup.find_all(
        'ul', {'class': 'visible-links bg-black-main odds-tabs flex w-full'})

    for oddsTab in oddsTabs:

        activeTab = oddsTab.select('li.active-odds')
        betType = activeTab[0].select_one('div').text

        if '/' in betType:
        # Replace '/' with '_'
            betType = betType.replace('/', '_')

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

    # print('-------------------')
    # print(info)
    # print(sport)
    # print(location)
    # print(league)
    # print('-------------------')

    # each odds line on Home/Away Line
    agencies = soup.find_all('div', {'class': 'border-black-borders flex h-9 border-b border-l border-r text-xs'})

    for agency in agencies:

        bookmaker = agency.find(
            'img', {'class': 'bookmaker-logo bg-cover bg-no-repeat'})
        bookmaker = bookmaker['title']

        # print(bookmaker)

        # Home Away Odds
        homeOdds = agency.find_all('div', recursive=False)[1].select_one('p').text

        if betType == '1X2':
            drawOdds = agency.find_all('div', recursive=False)[2].select_one('p').text
            awayOdds = agency.find_all('div', recursive=False)[3].select_one('p').text
        else:
            drawOdds = 0.00
            awayOdds = agency.find_all('div', recursive=False)[2].select_one('p').text

        # if bet365
        if bookmaker == 'bet365':
            bet365Home = float(homeOdds)
            bet365Draw = float(drawOdds)
            bet365Away = float(awayOdds)

            # print('BET365 AWAY')
            # print(bet365Away)

        # if Pinnacle
        if bookmaker == 'Pinnacle':
            pinnacleHome = float(homeOdds)
            pinnacleDraw = float(drawOdds)
            pinnacleAway = float(awayOdds)

            # print('PINNACLE AWAY')
            # print(pinnacleAway)

    homePercentage_difference = 0
    awayPercentage_difference = 0

    # print('HOME')
    # print(bet365Home) 
    # print(pinnacleHome)
    # print('---------')
    # print('Draw')
    # print(bet365Draw) 
    # print(pinnacleDraw)
    # print('---------')
    # print('AWAY')
    # print(bet365Away) 
    # print(pinnacleAway)

    # print(betType)

    if bet365Home is not None and pinnacleHome is not None and bet365Away is not None and pinnacleAway is not None and bet365Draw is not None and pinnacleDraw is not None:

        homePercentage_difference, homeProbability_winning1, homeProbability_winning2 = compare_ev(
            bet365Home, pinnacleHome)
        drawPercentage_difference, drawProbability_winning1, drawProbability_winning2 = compare_ev(
            bet365Draw, pinnacleDraw)
        awayPercentage_difference, awayProbability_winning1, awayProbability_winning2 = compare_ev(
            bet365Away, pinnacleAway)
        
        refrenceId = team1.replace(" ", "_" ) + '_' + team2.replace(" ", "_" ) + '_' + startDate + betType
        teams =  team1 + ' vs ' + team2
        agency = "bet365"
        league = location + ' - ' + league
        sport = sport
        betType = betType
        eventTime = startTime
        line = betType
        betResult = ''

        print(refrenceId)

        if homePercentage_difference > 0:
            betTeam = team1
            value = str(homePercentage_difference)
            odds = bet365Home

            # betValue = kelly_03(bet365Home, homeProbability_winning2, 1700)
            print(team1 + ' vs ' + team2 + ' = ' + team1)
            dbUpdate(refrenceId, teams, betTeam, value, eventTime, odds, agency, league, sport, betType, line, betResult)

        elif drawPercentage_difference > 0:
            betTeam = 'Draw'
            value = str(drawPercentage_difference)
            odds = bet365Draw

            print(team1 + ' vs ' + team2 + ' = Draw')
            dbUpdate(refrenceId, teams, betTeam, value, eventTime, odds, agency, league, sport, betType, line, betResult)

        elif awayPercentage_difference > 0:
            # betValue = kelly_03(bet365Away, awayProbability_winning2, 1700)

            betTeam = team2
            value = str(awayPercentage_difference)
            odds = bet365Away
            # betValue = kelly_03(bet365Home, homeProbability_winning2, 1700)

            print(team1 + ' vs ' + team2 + ' = ' + team2)
            dbUpdate(refrenceId, teams, betTeam, value, eventTime, odds, agency, league, sport, betType, line, betResult)

        else:
            print(team1 + ' vs ' + team2 + ' = No Value')
            dbUpdate(refrenceId, teams, 'NA', 'no value', eventTime, 'NA', agency, league, sport, betType, line, betResult)

    else:
        print(team1 + ' vs ' + team2)
        print('There are no odds yet!!')
