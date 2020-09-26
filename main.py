import json
from idlelib.multicall import r
import pandas
import requests

## League Tables ##
def tables():
    id = input("Enter the league table id \n")

    url = "https://api-football-v1.p.rapidapi.com/v2/leagueTable/{}".format(id)

    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.text
    jsonData = json.loads(data)
    pandas.json_normalize(jsonData)
    print(json.dumps(jsonData, indent=4))

## Teams ##
def teams():
    id = input("Enter the team id \n")
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/team/{}".format(id)
    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.text
    jsonData = json.loads(data)
    f = open("teams.json", "w")
    f.write(data)
    f.close()
    pandas.json_normalize(jsonData)
    print(json.dumps(jsonData, indent=4))
    with open('teams.json') as json_file:
        newdata = json.load(json_file)
        for p in newdata['api']['teams']:
            name = (p['name'])
            print(name)

## Stats ##
def stats():
    url = "https://api-football-v1.p.rapidapi.com/v2/statistics/524/33"

    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.text
    jsonData = json.loads(data)
    pandas.json_normalize(jsonData)
    print(json.dumps(jsonData, indent=4))

 ## Player ##
def player():
    choice = input("Enter player's name \n")
    url = "https://api-football-v1.p.rapidapi.com/v2/players/search/{}".format(choice)

    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.text
    jsonData = json.loads(data)
    pandas.json_normalize(jsonData)
    print(json.dumps(jsonData, indent=4))

## Predictions ##
def predictions():
    choice = input("Enter the required game id \n")
    url = "https://api-football-beta.p.rapidapi.com/predictions"

    querystring = {"fixture": choice}

    headers = {
        'x-rapidapi-host': "api-football-beta.p.rapidapi.com",
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.text
    jsonData = json.loads(data)
    pandas.json_normalize(jsonData)
    print(json.dumps(jsonData, indent=4))

## Todays matches and results ##
def fixtures():
    url = "https://api-football-beta.p.rapidapi.com/fixtures"
    choice = input("Enter the chosen league id\n")
    from datetime import datetime
    date = datetime.today().strftime('%Y-%m-%d')
    querystring = {"league": choice, "season": "2020", "date": date}

    headers = {
        'x-rapidapi-host': "api-football-beta.p.rapidapi.com",
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.text
    jsonData = json.loads(data)
    pandas.json_normalize(jsonData)
    print(json.dumps(jsonData, indent=4))

try:
    selection = input("What data do you want to view? \n")
    if selection == "tables":
        tables()
    if selection == "teams":
        teams()
    if selection == "stats":
        stats()
    if selection == "player":
        player()
    if selection == "predictions":
        predictions()
    if selection == "fixtures":
        fixtures()

except requests.exceptions.ConnectionError:
    r.status_code = "Connection refused"


