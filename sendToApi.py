# importing the requests library
import requests
import config

# api-endpoint
API = config.API_URL
  
# location given here
location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API
PARAMS = {
  "teams": "teab3",
  "sport": "NBA",
  "league": "Seconds",
  "eventTime": "Tuesday",
  "agency": "Bet365",
  "line": "Win",
  "value": "3%",
  "betType": "Plus",
  "betTeam": "First Team",
  "betAmount": 1232,
  "odds": 2
}
  
# sending get request and saving the response as response object
r = requests.post(url = URL, json = PARAMS)
  
# extracting data in json format
data = r.json()

print(data)