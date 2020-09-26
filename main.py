from idlelib.multicall import r
import pandas
import requests
import json
import mysql.connector
from mysql.connector import Error, cursor
from sqlalchemy import null


def create_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="irule666"
    )

    print(mydb)
    mycursor = mydb.cursor()

    mycursor.execute("USE footballPrediction;")
    mycursor.execute("Select * from premierLeague;")

    for x in mycursor:
        print(x)


## League Tables ##
def tables():
    id = input("Enter the league table id \n")

    url = "https://api-football-v1.p.rapidapi.com/v2/leagueTable/{}".format(id)
    id + 1

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
    url = "https://api-football-beta.p.rapidapi.com/teams"

    querystring = {"league": "39", "season": "2020"}

    headers = {
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc",
        'x-rapidapi-host': "api-football-beta.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    data = response.text
    jsonData = json.loads(data)
    f = open("teams.json", "w")
    f.write(data)
    f.close()
    pandas.json_normalize(jsonData)
    print(json.dumps(jsonData, indent=4))






## Stats ##
def stats():
    date = pandas.datetime.today().strftime('%Y-%m-%d')

    url = "https://api-football-v1.p.rapidapi.com/v2/statistics/2/33/{}".format(date)

    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.text
    jsonData = json.loads(data)
    f = open("stats.json", "w")
    f.write(data)
    f.close()
    pandas.json_normalize(jsonData)
    print(json.dumps(jsonData, indent=4))
    with open('teams.json') as json_file:
        newdata = json.load(json_file)
        for p in newdata['api']['results']['matchs']['wins']:
            name = [p['total']]
            print(name)


def writeData():

    with open('leagues.json') as json_file:

        newdata = json.load(json_file)
        teamName = (newdata['response']['team']['name'])
       # print(teamName)
        totalWins = (newdata['response']['fixtures']['wins']['total'])
      #  print("Number of wins this season: ", totalWins)
        totalDraws = (newdata['response']['fixtures']['draws']['total'])
       # print("Number of draws this season: ", totalDraws)
        totalLoses = (newdata['response']['fixtures']['loses']['total'])
      #  print("Number of losses this season: ", totalLoses)

        teamId = (newdata['response']['team']['id'])
        teamName = (newdata['response']['team']['name'])
        teamHomeWins = (newdata['response']['fixtures']['wins']['home'])
        teamHomeDraws = (newdata['response']['fixtures']['draws']['home'])
        teamHomeLosses = (newdata['response']['fixtures']['loses']['home'])
        teamAwayWins = (newdata['response']['fixtures']['wins']['away'])
        teamAwayDraws = (newdata['response']['fixtures']['draws']['away'])
        teamAwayLosses = (newdata['response']['fixtures']['loses']['away'])
        goalsForHome = (newdata['response']['goals']['for']['total']['home'])
        goalsForAway = (newdata['response']['goals']['for']['total']['away'])
        goalsConcededHome = (newdata['response']['goals']['against']['total']['home'])
        goalsConcededAway = (newdata['response']['goals']['against']['total']['away'])

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="irule666"
        )

        print(mydb)
        mycursor = mydb.cursor()

        mycursor.execute("USE footballPrediction;")
        #mycursor.execute("Select * from premierLeague;")

        for x in mycursor:
            print(x)

        mycursor = mydb.cursor()

        sql = "INSERT INTO premierLeague(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(teamId,teamName,teamHomeWins,teamHomeDraws,teamHomeLosses,teamAwayWins,teamAwayDraws,teamAwayLosses,goalsForHome,goalsForAway,goalsConcededHome,goalsConcededAway)

        sql = ("""INSERT INTO
                  premierLeague
                  (teamId,teamName,teamHomeWins,teamHomeDraws,teamHomeLosses,teamAwayWins,teamAwayDraws,teamAwayLosses,goalsForHome,goalsForAway,goalsConcededHome,goalsConcededAway)
               VALUES
                  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

        insert_tuple = (teamId,teamName,teamHomeWins,teamHomeDraws,teamHomeLosses,teamAwayWins,teamAwayDraws,teamAwayLosses,goalsForHome,goalsForAway,goalsConcededHome,goalsConcededAway)
        mycursor.execute(sql, insert_tuple)
        mydb.commit()

        print(mycursor.rowcount, "record inserted.")

        ##Using data
        #totalMatchesPlayed = totalWins + totalDraws + totalLoses
        #winPercentage = totalWins / totalMatchesPlayed
        #drawPercentage = totalDraws / totalMatchesPlayed
        #losePercentage = totalWins / totalMatchesPlayed
        #print("Win Percentage this season = ", winPercentage)
        #print("Draw Percentage this season = ", drawPercentage)
        #print("Loss Percentage this season = ", losePercentage)


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


def leagues():
    url = "https://rapidapi.p.rapidapi.com/v2/fixtures/league/524/last/10"

    querystring = {"timezone": "Europe/London"}

    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def getData():
    premierLeagueTeamIds = [46,47,40,41,49,66,45,52,39,50,42,48,34,33,63,51,36,60,44,62]

    teamId = input("Enter the team ID\n")
    url = "https://api-football-beta.p.rapidapi.com/teams/statistics"

    querystring = {"team": teamId, "season": "2020", "league": "39"}

    headers = {
        'x-rapidapi-host': "api-football-beta.p.rapidapi.com",
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.text
    jsonData = json.loads(data)
    f = open("leagues.json", "w")
    f.write(data)
    f.close()
    pandas.json_normalize(jsonData)
    print(json.dumps(jsonData, indent=4))
    writeData()



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
    if selection == "leagues":
        leagues()
    if selection == "write":
        writeData()
    if selection == "get":
        getData()
    if selection == "sql":
        create_connection()

except requests.exceptions.ConnectionError:
    r.status_code = "Connection refused"
