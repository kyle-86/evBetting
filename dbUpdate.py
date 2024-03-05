import requests
import config

def dbUpdate(refrenceId, teams=None, betTeam=None, value=None, eventTime=None, odds=None, agency=None, league=None, sport=None, betType=None, line=None, betResult=None):
    API = config.API_URL
    PARAMS = {}

    PARAMS["refrenceId"] = refrenceId
    PARAMS["teams"] = teams
    PARAMS["betTeam"] = betTeam
    PARAMS["value"] = value
    PARAMS["eventTime"] = eventTime
    PARAMS["odds"] = odds
    PARAMS["agency"] = agency
    PARAMS["league"] = league
    PARAMS["sport"] = sport
    PARAMS["betType"] = betType
    PARAMS["line"] = line
    PARAMS["betResult"] = betResult

    response = requests.get(API, params=PARAMS)

    if response.status_code == 200:
        existing_entries = response.json()

        if existing_entries:
            # Entry already exists, update the existing record
            entry_updated = False
            for i, existing_entry in enumerate(existing_entries):
                if existing_entry["refrenceId"] == refrenceId:
                    if teams is not None:
                        existing_entries[i]['teams'] = teams
                    if betTeam is not None:
                        existing_entries[i]['betTeam'] = betTeam
                    if value is not None:
                        existing_entries[i]['value'] = value
                    if eventTime is not None:
                        existing_entries[i]['eventTime'] = eventTime
                    if odds is not None:
                        existing_entries[i]['odds'] = odds
                    if agency is not None:
                        existing_entries[i]['agency'] = agency
                    if league is not None:
                        existing_entries[i]['league'] = league
                    if sport is not None:
                        existing_entries[i]['sport'] = sport
                    if betType is not None:
                        existing_entries[i]['betType'] = betType
                    if line is not None:
                        existing_entries[i]['line'] = line
                    if betResult is not None:
                        existing_entries[i]['betResult'] = betResult

                    response = requests.put(API + f"{existing_entries[i]['id']}", json=existing_entries[i])
                    print("Existing entry updated.")
                    entry_updated = True
                    

            if not entry_updated:
                if teams is not None:  # Check if teams is not None before sending the request
                    # If no matching entry is found, save the new entry
                    response = requests.post(API, json=PARAMS)
                    print("New entry saved.")
                else:
                    print("Results Not needed")
        else:
            # No existing entries found, save the new entry
            response = requests.post(API, json=PARAMS)
            print("New entry saved.")
    else:
        print("Error checking existing entries:", response.status_code)
