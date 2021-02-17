import csv
import sys
from idlelib.multicall import r
from tkinter import ttk
from tkinter.tix import Tk
from tkinter.ttk import Combobox
from turtle import pd

import pandas
import requests
import json
import mysql.connector
from datetime import datetime, date
from mysql.connector import Error, cursor


from sqlalchemy import null
# Used for plotting data
import matplotlib.pyplot as plt
# Used for data storage and manipulation
import numpy as np
import pandas as pd
import PySimpleGUI as sg
# Used for Regression Modelling
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.model_selection import train_test_split, GridSearchCV
# Used for Acc metrics
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
# For stepwise regression
import statsmodels.api as sm
# box plots
import seaborn as sns
# pairplot
from seaborn import pairplot
# Correlation plot
from statsmodels.graphics.correlation import plot_corr
from sklearn.model_selection import train_test_split
from statsmodels.stats import proportion




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


## Teams  ##
def teams():
    url = "https://api-football-beta.p.rapidapi.com/teams"

    querystring = {"league": "37", "season": "2020"}

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

## Writing data to the sql database
def writeData():

    with open('leagues.json') as json_file:

        newdata = json.load(json_file)

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
    sg.popup('Tables Created')

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

    import requests

    url = "https://api-football-beta.p.rapidapi.com/players/topscorers"

    querystring = {"season": "2020", "league": "39"}

    headers = {
        'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc",
        'x-rapidapi-host': "api-football-beta.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)



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

## Finding team by id and writing to json file then calling the writeData() method
#def getData():
    premierLeagueTeamIds = [46,47,40,41,49,66,45,52,39,50,42,48,34,33,63,51,36,60,44,62]

 #   teamId = input("Enter the team ID\n")
 #   url = "https://api-football-beta.p.rapidapi.com/teams/statistics"

  #  querystring = {"team": teamId, "season": "2020", "league": "39"}

  #  headers = {
  #      'x-rapidapi-host': "api-football-beta.p.rapidapi.com",
  #      'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc"
  #  }
   # response = requests.request("GET", url, headers=headers, params=querystring)
   # data = response.text
   # jsonData = json.loads(data)
#    f.write(data)
  #  f.close()
  #  pandas.json_normalize(jsonData)
  #  print(json.dumps(jsonData, indent=4))
  #  writeData()

def seasons():

    import requests
    for i in range(1,150):
        url = "https://api-football-beta.p.rapidapi.com/leagues"

        querystring = {"id": i}

        headers = {
            'x-rapidapi-key': "302263ea25msh9a7e14f76d93cb7p1aa44djsnd0501e5ec3cc",
            'x-rapidapi-host': "api-football-beta.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)




def writeData(newdata):


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
        # mycursor.execute("Select * from premierLeague;")

        for x in mycursor:
            print(x)

        mycursor = mydb.cursor()

        sql = ("""INSERT INTO
                  premierLeague
                  (teamId,teamName,teamHomeWins,teamHomeDraws,teamHomeLosses,teamAwayWins,teamAwayDraws,teamAwayLosses,goalsForHome,goalsForAway,goalsConcededHome,goalsConcededAway)
               VALUES
                  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

        insert_tuple = (
        teamId, teamName, teamHomeWins, teamHomeDraws, teamHomeLosses, teamAwayWins, teamAwayDraws, teamAwayLosses,
        goalsForHome, goalsForAway, goalsConcededHome, goalsConcededAway)
        mycursor.execute(sql, insert_tuple)
        mydb.commit()

        print(mycursor.rowcount, "record inserted.")




def updateData(newdata):
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
    # mycursor.execute("Select * from premierLeague;")

    for x in mycursor:
        print(x)

    mycursor = mydb.cursor()

    sql = ("""UPDATE
              premierLeague
              SET
              teamHomeWins = %s,teamHomeDraws = %s,teamHomeLosses  = %s,teamAwayWins  = %s,teamAwayDraws = %s,teamAwayLosses = %s,goalsForHome = %s,goalsForAway = %s,goalsConcededHome = %s,goalsConcededAway = %s WHERE teamId = %s""")

    insert_tuple = (
    teamHomeWins, teamHomeDraws, teamHomeLosses, teamAwayWins, teamAwayDraws, teamAwayLosses,
    goalsForHome, goalsForAway, goalsConcededHome, goalsConcededAway,teamId)
    mycursor.execute(sql, insert_tuple)
    mydb.commit()



    print(mycursor.rowcount, "record updated.")

def iteration():
    try:
        premierLeagueTeamIds = [46, 47, 40, 41, 49, 66, 45, 52, 39, 50, 42, 48, 34, 33, 63, 51, 36, 60, 44, 62]

        for i in premierLeagueTeamIds:
            url = "https://api-football-beta.p.rapidapi.com/teams/statistics"
            querystring = {"team": i, "season": "2020", "league": "39"}

            headers = {
            'x-rapidapi-host': "api-football-beta.p.rapidapi.com",
            'x-rapidapi-key': "040797c46dmshfe1b04e202c5b85p19f211jsn29020fbab24f",
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.text
            jsonData = json.loads(data)
            writeData(jsonData)
            pandas.json_normalize(jsonData)
            print(json.dumps(jsonData, indent=4))
        sg.popup('Tables Created')
    except:
        sg.popup('Tables already exist')

def update():
    try:
        premierLeagueTeamIds = [46, 47, 40, 41, 49, 66, 45, 52, 39, 50, 42, 48, 34, 33, 63, 51, 36, 60, 44, 62]

        for i in premierLeagueTeamIds:
            url = "https://api-football-beta.p.rapidapi.com/teams/statistics"
            querystring = {"team": i, "season": "2020", "league": "39"}

            headers = {
            'x-rapidapi-host': "api-football-beta.p.rapidapi.com",
            'x-rapidapi-key': "040797c46dmshfe1b04e202c5b85p19f211jsn29020fbab24f",
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.text
            jsonData = json.loads(data)
            updateData(jsonData)
            pandas.json_normalize(jsonData)
            print(json.dumps(jsonData, indent=4))
        sg.popup('Tables updated')
    except:
        sg.popup('Tables already up to date')


def save():
    import MySQLdb as dbapi
    import sys
    import csv

    QUERY = 'SELECT * FROM premierLeague;'
    db = dbapi.connect(host="localhost",
        user="root",
        password="irule666")

    cur = db.cursor()
    cur.execute("USE footballPrediction;")
    cur.execute(QUERY)
    result = cur.fetchall()

    c = csv.writer(open('premierLeague.csv', 'w'))
    for x in result:
        c.writerow(x)

def machineLearning():
    import seaborn as sns
    # -------------Load data--------------------------
    data = pd.read_csv("premierLeague1.csv")
    # Check out shape
    print(data.shape)
    (12144, 18)

    # return only rows where the Home goals is greater than 0
    current = data[(data['goalsForHome'] > 0)]
    # check for the null values in each column
    current.isna().sum()
    #checks out current dataframe
    current.info()
    # Gives you summary statistics on your numeric columns
    current.describe()

    ##-------------Data preperation-----------------
    ##Format Data
    # Store needed columns into new dataframe named df
    df = [['teamHomeWins'], ['teamHomeDraws'], ['teamHomeLosses'], ['teamAwayWins'], ['teamAwayDraws'],['teamAwayLosses'],['goalsForHome'],['goalsForAway'],['goalsConcededHome'],['goalsConcededHome'],['goalsConcededAway']]
    # Check out our new df
    #df.info()
    #pairplot(df)
    ##-----------------Format Data---------------
    # Store needed columns from final into new dataframe named df



    ##------------------Create Training & Testing Set-----------------
    X = pd.DataFrame(df, columns=['weather_temperature', 'home_or_away'])
    y = pd.DataFrame(df, columns=['score'])
    # WITH a random_state parameter:
    #  (Same split every time! Note you can change the random state to any integer.)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)


    ##-------------Building Model----------------------------------

    # Create linear regression model
    lin_reg_mod = LinearRegression()
    # Fit linear regression
    lin_reg_mod.fit(X_train, y_train)
    # Make prediction on the testing data
    pred = lin_reg_mod.predict(X_test)

    print(pred)



def machineLearning1():
    import pandas as pd
    import numpy as np
    import sys

    stdoutOrigin = sys.stdout
    sys.stdout = open("log.txt", "w")

    df11 = pd.read_csv('premierLeague1.csv', usecols=['teamHomeWins', 'teamHomeDraws', 'teamHomeLosses', 'teamAwayWins', 'teamAwayDraws', 'teamAwayLosses','goalsForHome','goalsForAway','goalsConcededHome','goalsConcededAway','lastMatchResult'])
    df11.head()
    conf = proportion.proportion_confint((df11['lastMatchResult'] == 'H').sum(), df11['lastMatchResult'].count(),
                                         alpha=0.05, method='normal')
    print('The chance of home team to win with %95 confidence interval falls in :{}'.format(conf))

    sys.stdout.close()
    sys.stdout = stdoutOrigin
    textPrinting('log.txt')

##This pie graph shows the home team has higher chance to win the game. We can find confidence interval for our hypothesis.
    import matplotlib.pyplot as plt
    plt.figure(figsize=(6, 8))
    plt.pie(df11['lastMatchResult'].value_counts(), labels=['Home', 'Away', 'Draw'], autopct='%1.1f%%', shadow=True, startangle=0)
    plt.axis('equal')
    plt.title('Win percentages', size=18)
    plt.show()




    #df2 = pd.read_csv('premierLeague.csv',
    #                  usecols=['teamHomeWins', 'teamHomeDraws', 'teamHomeLosses', 'teamAwayWins', 'teamAwayDraws',
    #                           'teamAwayLosses', 'goalsForHome', 'goalsForAway', 'goalsConcededHome',
    #                           'goalsConcededAway', 'lastMatchResult'])
    #df2.head()

    ##This pie graph shows the home team goals breakdown. We can find confidence interval for our hypothesis.
  #  import matplotlib.pyplot as plt
  #  plt.figure(figsize=(6, 8))
  #  plt.pie(df2['goalsForHome'].value_counts(), autopct='%1.1f%%', shadow=True,
  #          startangle=0)
  #  plt.axis('equal')
  #  plt.title('Home Goals Breakdown', size=18)
  #  plt.show()





   # from statsmodels.stats import proportion
   # conf = proportion.proportion_confint((df2['goalsForHome'] >= 10).sum(), df2['goalsForHome'].count(), alpha=0.05, method='normal')
   # print('The chance of home team to have scored ten or more home goals this season with %95 confidence interval falls in :{}'.format(conf))



def make_data(df):
    ##add points for away and home team : win 3 points, draw 1 point, loss 0 point
    df['HP']=np.select([df['FTR']=='H',df['FTR']=='D',df['FTR']=='A'],[3,1,0])
    df['AP']=np.select([df['FTR']=='H',df['FTR']=='D',df['FTR']=='A'],[0,1,3])
    ## add difference in goals for home and away team
    df['HDG']=df['FTHG']-df['FTAG']
    df['ADG']=-df['FTHG']+df['FTAG']
    ##add momentum to data
    cols=['Team','Points','Goal','Shoot','TargetShoot','DiffG']
    df1=df[['HomeTeam','AwayTeam','HP','AP','FTHG','FTAG','HS','AS','HST','AST','HDG','ADG']]
    df1.columns=[np.repeat(cols,2),['Home','Away']*len(cols)]
    d1=df1.stack()
    ##find momentum of previous five games for each team
    mom5 = d1.groupby('Team').apply(lambda x: x.shift().rolling(5, 4).mean())
    mom=d1.groupby('Team').apply(lambda x: pd.Series.mean(x.shift()))
    ##add the found momentum to the dataframe
    df2=d1.assign(MP=mom5['Points'],MG=mom5['Goal'],MS=mom5['Shoot'],MST=mom5['TargetShoot'],MDG=mom5['DiffG'],AP=mom['Points'],AG=mom['Goal'],AS=mom['Shoot'],AST=mom['TargetShoot'],ADG=mom['DiffG']).unstack()
    df2=df2.drop(['Points','Goal','Shoot','TargetShoot','DiffG'],axis=1)
    df_final=pd.merge(df[['HomeTeam','AwayTeam','FTR','B365H','B365D','B365A','Ade','Aatt','Apo','Atot','Hde','Hatt','Hpo','Htot']],df2,left_on=['HomeTeam','AwayTeam'],right_on=[df2['Team']['Home'],df2['Team']['Away']])
    df_final=df_final.dropna(axis=0,how='any')
    ##Full time results ('FTR') : Home=0,Draw=1,Away=2
    Y_all=df_final['FTR']
    ##Full time results ('FTR') : Home=0,Draw=1,Away=2
    ##Prediction of betting company (bet365)=Y_Bet
    Y_Bet=df_final[['B365H','B365D','B365A']].apply(lambda x:1/x)
    ## winner based on bet365 data
    Y_Bet_FTR=np.select([Y_Bet.idxmax(axis=1)=='B365H',Y_Bet.idxmax(axis=1)=='B365D',Y_Bet.idxmax(axis=1)=='B365A'],['H','D','A'])
    ##scale data
    df_X=df_final.drop([('Team', 'Home'),('Team', 'Away'),'FTR','HomeTeam','AwayTeam','B365H','B365D','B365A'],axis=1)

    #print(mom)
    #print(mom5)
    import PySimpleGUI as sg

    sg.Print('Re-routing the stdout', do_not_reroute_stdout=False)

    print(df1)





def textPrinting(file):
    import PySimpleGUI as sg

    sg.Print(do_not_reroute_stdout=False)
    f = open(file, 'r')
    file_contents = f.read()
    print(file_contents)
    f.close()


def predicting(homeTeam,awayTeam):

   try:
        if('Man United' in homeTeam):
            dataset='ManUHome.csv'
        elif('Fulham' in homeTeam):
            dataset='FulhamHome.csv'
        elif('Fulham' in awayTeam):
            dataset='FulhamAway.csv'
        elif('Man United' in awayTeam):
            dataset='ManUAway.csv'





        import pandas as pd

        df1 = pd.read_csv(dataset, usecols=['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR','HTR', 'HS', 'AS', 'HST', 'AST'
            , 'B365H', 'B365D', 'B365A'])
        df1.head()


        #print("################Parameter Check#######################")

        #print(homeTeam)




        stdoutOrigin = sys.stdout
        sys.stdout = open("log.txt", "w")

        from statsmodels.stats import proportion
        confHome = proportion.proportion_confint((df1['FTR'] == 'H').sum(), df1['FTR'].count(), alpha=0.05, method='wilson')
        confAway = proportion.proportion_confint((df1['FTR'] == 'A').sum(), df1['FTR'].count(), alpha=0.05, method='wilson')
        confDraw = proportion.proportion_confint((df1['FTR'] == 'D').sum(), df1['FTR'].count(), alpha=0.05, method='wilson')
        print('The chance of home team to win with %95 confidence interval falls in :{}'.format(confHome))
        print('--------------------------------------------------------------------------------')
        print('The chance of away team to win with %95 confidence interval falls in :{}'.format(confAway))
        print('--------------------------------------------------------------------------------')
        print('The chance of a draw with %95 confidence interval falls in :{}'.format(confDraw))

        sys.stdout.close()
        sys.stdout = stdoutOrigin
        textPrinting('log.txt')

        import matplotlib.pyplot as plt
        plt.figure(figsize=(6, 8))
        plt.pie(df1['FTR'].value_counts(), labels=['Home Win', 'Home Loss', 'Draw'], autopct='%1.1f%%', shadow=True, startangle=0)
        plt.axis('equal')
        plt.title('Win Percentage', size=18)
        plt.show()

        sg.Popup("Complete")

   except:
        sg.Popup("No Matches")



def prediction(homeTeam,awayTeam):
    if ('Man United' in homeTeam):
        dataset = 'ManUHome.csv'
    elif ('Fulham' in homeTeam):
        dataset = 'FulhamHome.csv'
    elif ('Fulham' in awayTeam):
        dataset = 'FulhamAway.csv'
    elif ('Man United' in awayTeam):
        dataset = 'ManUAway.csv'

    import pandas as pd
    import numpy as np
    df1 = pd.read_csv(dataset, usecols=['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HS', 'AS', 'HST', 'AST'
        , 'B365H', 'B365D', 'B365A'])
    df1.head()

    ##add new data to data frame
    dfSq = pd.read_csv('dataE0.csv', index_col='Team').dropna(axis=0, how='any')
    ##Hde: Home Defense    Hatt: Home Attack    Hpo: Home possession    Htot : Home total power
    ##Ade: Away defense   Aatt: away attack    Apo : Away possession :  Atot: Away total power
    dfSq.head()
    dff = df1.join(dfSq[['Hde', 'Hatt', 'Hpo', 'Htot']], on='HomeTeam')
    df = dff.join(dfSq[['Ade', 'Aatt', 'Apo', 'Atot']], on='AwayTeam')
    make_data(df)


def logisticRegression(homeTeam,awayTeam):

    import pandas as pd
    import numpy as np
    from sklearn import preprocessing
    import matplotlib.pyplot as plt
    plt.rc("font", size=14)
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    import seaborn as sns

    try:

        if ('Man United' in homeTeam):
            dataset = 'ManUHome.csv'
        elif ('Fulham' in homeTeam):
            dataset = 'FulhamHome.csv'
        elif ('Newcastle' in homeTeam):
            dataset = 'NewcastleHome.csv'


        sns.set(style="white")
        sns.set(style="whitegrid", color_codes=True)

        data = pd.read_csv(dataset, sep =',',header=0)
        data = data.dropna()
        print(data.shape)
        print(list(data.columns))

        data.head()

     ##Predict Variable / Desired Target

        data['FTHG'].value_counts()
        #sns.countplot(x='FTHG', data=data, palette='hls')
        #plt.show()
        #plt.savefig('count_plot')

        #data.groupby('FTHG').mean()
        #data.groupby('HS').mean()
        #data.groupby('HST').mean()

        pd.crosstab(data.FTHG, data.HS).plot(kind='bar')
        plt.title('{} home goals vs. shots'.format(homeTeam))
        plt.xlabel('Goals')
        plt.ylabel('Shots')
        plt.savefig('goals_vs_shots_home')
        plt.show()

        #data.FTHG.hist()
        #plt.title('Histogram of Home Goals')
       # plt.xlabel('Goals')
       # plt.ylabel('Frequency')
        #plt.savefig('hist_goals')

    except:
        sg.Popup("No dataset available")

    try:

        if ('Man United' in awayTeam):
            dataset = 'ManUAway.csv'
        elif ('Fulham' in awayTeam):
            dataset = 'FulhamAway.csv'
        elif ('Newcastle' in awayTeam):
            dataset = 'NewcastleAway.csv'

        sns.set(style="white")
        sns.set(style="whitegrid", color_codes=True)

        data = pd.read_csv(dataset, sep=',', header=0)
        data = data.dropna()
        print(data.shape)
        print(list(data.columns))

        data.head()

        ##Predict Variable / Desired Target

        data['FTAG'].value_counts()
        # sns.countplot(x='FTHG', data=data, palette='hls')
        # plt.show()
        # plt.savefig('count_plot')

        # data.groupby('FTHG').mean()
        # data.groupby('HS').mean()
        # data.groupby('HST').mean()

        pd.crosstab(data.FTAG, data.AS).plot(kind='bar')
        plt.title('{} away goals vs. shots'.format(awayTeam))
        plt.xlabel('Goals')
        plt.ylabel('Shots')
        plt.savefig('goals_vs_shots_away')
        plt.show()


        # data.FTHG.hist()
        # plt.title('Histogram of Home Goals')
    # plt.xlabel('Goals')
    # plt.ylabel('Frequency')
    # plt.savefig('hist_goals')

    except:
        sg.Popup("No dataset available")



def linearRegression(homeTeam,awayTeam):
    import pandas as pd
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error
    from math import sqrt

    try:

        if ('Man United' in homeTeam):
            dataset = 'ManUHome.csv'
        elif ('Fulham' in homeTeam):
            dataset = 'FulhamHome.csv'
        elif ('Newcastle' in homeTeam):
            dataset = 'NewcastleHome.csv'

        ##Read Data from the Database into pandas
        df = pd.read_csv(dataset, sep =',',header=0)


        ##Declare the Columns You Want to Use as Features
        features = ['HTHG','HS','HST']

        ##Specify the Prediction Target
        target = ['FTHG']
        ##Clean Data
        df = df.dropna()
        ##Extract Features and Target ('Full time home goals') Values into Separate Dataframes
        X = df[features]
        y = df[target]

        ##Typical row from features
        print(X.iloc[2])

        ##Linear Regression: Fit a model to the training set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=324)
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        ##Perform Prediction using Linear Regression Model
        y_prediction = regressor.predict(X_test)

        sg.Print('Prediction for Home Team...', do_not_reroute_stdout=False)

        ##What is the mean of the expected target value in test set ?
        #print(y_test.describe())
        ##Evaluate Linear Regression Accuracy using Root Mean Square Error
        RMSE = sqrt(mean_squared_error(y_true=y_test, y_pred=y_prediction))
        formatted_RMSE = "{:.2f}".format(RMSE)


        print("\nPredicted amount of goals using Linear Regression for {0}\nin their next game against {2} is: {1}".format(homeTeam, formatted_RMSE,awayTeam))

        ##Decision Tree Regressor - Fit a new regression model to the training set
        regressor = DecisionTreeRegressor(max_depth=20)
        regressor.fit(X_train, y_train)

        ##Perform Prediction using Decision Tree Regressor
        y_prediction = regressor.predict(X_test)
        y_prediction

        ##Evaluate Decision Tree Regression Accuracy using Root Mean Square Error
        RMSE2 = sqrt(mean_squared_error(y_true=y_test, y_pred=y_prediction))
        formatted_RMSE2 = "{:.2f}".format(RMSE2)
        print("\nPredicted amount of goals using Decision Tree Regression for {0}\nin their next game against {2} is: {1}".format(homeTeam, formatted_RMSE2,awayTeam))


    except:
        sg.Popup("No dataset available")

    try:

        if ('Man United' in awayTeam):
            dataset = 'ManUAway.csv'
        elif ('Fulham' in awayTeam):
            dataset = 'FulhamAway.csv'
        elif ('Newcastle' in awayTeam):
            dataset = 'NewcastleAway.csv'

        ##Read Data from the Database into pandas
        df = pd.read_csv(dataset, sep =',',header=0)


        ##Declare the Columns You Want to Use as Features
        features = ['HTAG','AS','AST']

        ##Specify the Prediction Target
        target = ['FTAG']
        ##Clean Data
        df = df.dropna()
        ##Extract Features and Target ('Full time away goals') Values into Separate Dataframes
        X = df[features]
        y = df[target]

        ##Typical row from features
        #print(X.iloc[2])

        ##Linear Regression: Fit a model to the training set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=324)
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        ##Perform Prediction using Linear Regression Model
        y_prediction = regressor.predict(X_test)

        sg.Print('\nPrediction for Away Team...', do_not_reroute_stdout=False)

        ##What is the mean of the expected target value in test set ?
        #print(y_test.describe())
        ##Evaluate Linear Regression Accuracy using Root Mean Square Error
        RMSE = sqrt(mean_squared_error(y_true=y_test, y_pred=y_prediction))
        formatted_RMSE = "{:.2f}".format(RMSE)


        print("\nPredicted amount of goals using Linear Regression for {0}\nin their next game against {2} is: {1}".format(awayTeam, formatted_RMSE,homeTeam))

        ##Decision Tree Regressor - Fit a new regression model to the training set
        regressor = DecisionTreeRegressor(max_depth=20)
        regressor.fit(X_train, y_train)

        ##Perform Prediction using Decision Tree Regressor
        y_prediction = regressor.predict(X_test)
        y_prediction

        ##Evaluate Decision Tree Regression Accuracy using Root Mean Square Error
        RMSE2 = sqrt(mean_squared_error(y_true=y_test, y_pred=y_prediction))
        formatted_RMSE2 = "{:.2f}".format(RMSE2)
        print("\nPredicted amount of goals using Decision Tree Regression for {0}\nin their next game against {2} is: {1}".format(awayTeam, formatted_RMSE2,homeTeam))


    except:
        sg.Popup("No dataset available")





f = open('E0.csv','r')
reader = csv.reader(f)
homeTeam = []
awayTeam = []

for row in reader:
    homeTeam.append([row[3]])
    awayTeam.append([row[4]])

dictOfWords = { i : homeTeam[i] for i in range(0, len(homeTeam) ) }
#print(dictOfWords)




layout = [[sg.Combo(values=homeTeam, default_value=homeTeam[0],enable_events=True, key='combo'),sg.Combo(values=awayTeam,default_value=awayTeam[0],enable_events=True, key='combo1'),sg.Button('Stats Prediction'),sg.Button('ML Prediction'),sg.Button('Save Data to .CSV'), sg.Button('Update Tables'),sg.Button('Create Tables'),sg.Cancel()]]


window = sg.Window('Football Prediction', layout)



try:
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Stats Prediction':
            comboHome = values['combo']
            comboAway = values['combo1']  # use the combo key
            logisticRegression(comboHome,comboAway)
        elif event == 'ML Prediction':
            comboHome = values['combo']
            comboAway = values['combo1']  # use the combo key
            #prediction(comboHome,comboAway)
            linearRegression(comboHome,comboAway)
        elif event == 'Update Tables': #or date.today().weekday() == 1:
            update()
        elif event == 'Create Tables':
            iteration()
        elif event == 'Save Data to .CSV':
            save()
            sg.popup('Data saved to csv file')
    window.close()






   #  Data Scehduler Code
     ##   update()

   # selection = input("What data do you want to view? \n")
   # if selection == "tables":
  #      tables()
   # if selection == "teams":
   #     teams()
   # if selection == "stats":
   #     stats()
   # if selection == "player":
   #     player()
  #  if selection == "prediction":
  #     prediction()
  #  if selection == "fixtures":
  #      fixtures()
  #  if selection == "leagues":
   #     leagues()
  #  if selection == "write":
  #      writeData()
  #  if selection == "insert":
   #     iteration()
  #  if selection == "update":
  #      update()
  #  if selection == "save":
  #      save()
  #  if selection == "sql":
  #      create_connection()
  #  if selection == "seasons":
  #      seasons()
   # if selection == "predict":
   #     machineLearning()
   # if selection == "pie":
   #machineLearning1()






except requests.exceptions.ConnectionError:
    r.status_code = "Connection refused"