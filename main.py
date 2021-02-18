import csv
import sys
from idlelib.multicall import r
import pandas
import requests
import json
import mysql.connector
import PySimpleGUI as sg

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
    import csv

    QUERY = 'SELECT * FROM premierLeague;'
    db = dbapi.connect(host="localhost",
        user="root",
        password="irule666")

    cur = db.cursor()
    cur.execute("USE footballPrediction;")
    cur.execute(QUERY)
    result = cur.fetchall()

    c = csv.writer(open('dataset/premierLeague.csv', 'w'))
    for x in result:
        c.writerow(x)


def textPrinting(file):
    import PySimpleGUI as sg

    sg.Print(do_not_reroute_stdout=False)
    f = open(file, 'r')
    file_contents = f.read()
    print(file_contents)
    f.close()


def predicting(homeTeam,awayTeam):
   import pandas as pd
   try:
        if('Man United' in homeTeam):
            dataset='dataset/ManUHome.csv'
        elif('Fulham' in homeTeam):
            dataset='dataset/FulhamHome.csv'
        elif('Fulham' in awayTeam):
            dataset='dataset/FulhamAway.csv'
        elif('Man United' in awayTeam):
            dataset='dataset/ManUAway.csv'



        df1 = pd.read_csv(dataset, usecols=['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR','HTR', 'HS', 'AS', 'HST', 'AST'
            , 'B365H', 'B365D', 'B365A'])
        df1.head()


        stdoutOrigin = sys.stdout
        sys.stdout = open("logs/log.txt", "w")

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
        textPrinting('logs/log.txt')

        import matplotlib.pyplot as plt
        plt.figure(figsize=(6, 8))
        plt.pie(df1['FTR'].value_counts(), labels=['Home Win', 'Home Loss', 'Draw'], autopct='%1.1f%%', shadow=True, startangle=0)
        plt.axis('equal')
        plt.title('Win Percentage', size=18)
        plt.show()

        sg.Popup("Complete")

   except:
        sg.Popup("No Matches")



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
            dataset = 'dataset/ManUHome.csv'
        elif ('Fulham' in homeTeam):
            dataset = 'dataset/FulhamHome.csv'
        elif ('Newcastle' in homeTeam):
            dataset = 'dataset/NewcastleHome.csv'
        elif ('Man City' in homeTeam):
            dataset = 'dataset/ManCHome.csv'
        elif ('Wolves' in homeTeam):
            dataset = 'dataset/WolvesHome.csv'
        elif ('Liverpool' in homeTeam):
            dataset = 'dataset/LiverpoolHome.csv'
        elif ('Southampton' in homeTeam):
            dataset = 'dataset/SouthamptonHome.csv'


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
        plt.savefig('img/goals_vs_shots_home')
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
            dataset = 'dataset/ManUAway.csv'
        elif ('Fulham' in awayTeam):
            dataset = 'dataset/FulhamAway.csv'
        elif ('Newcastle' in awayTeam):
            dataset = 'dataset/NewcastleAway.csv'
        elif ('Man City' in awayTeam):
            dataset = 'dataset/ManCAway.csv'
        elif ('Wolves' in awayTeam):
            dataset = 'dataset/WolvesAway.csv'
        elif ('Liverpool' in awayTeam):
            dataset = 'dataset/LiverpoolAway.csv'
        elif ('Southampton' in awayTeam):
            dataset = 'dataset/SouthamptonAway.csv'

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
        plt.savefig('img/goals_vs_shots_away')
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
            dataset = 'dataset/ManUHome.csv'
        elif ('Fulham' in homeTeam):
            dataset = 'dataset/FulhamHome.csv'
        elif ('Newcastle' in homeTeam):
            dataset = 'dataset/NewcastleHome.csv'
        elif ('Man City' in homeTeam):
            dataset = 'dataset/ManCHome.csv'
        elif ('Wolves' in homeTeam):
            dataset = 'dataset/WolvesHome.csv'
        elif ('Liverpool' in homeTeam):
            dataset = 'dataset/LiverpoolHome.csv'
        elif ('Southampton' in homeTeam):
            dataset = 'dataset/SouthamptonHome.csv'

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
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50,train_size=0.50, random_state=324)
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        ##Perform Prediction using Linear Regression Model
        y_prediction = regressor.predict(X_test)



        sg.Print('Prediction for Home Team...', do_not_reroute_stdout=False)

        ##What is the mean of the expected target value in test set ?
        #print(y_test.describe())
        ##Evaluate Linear Regression Accuracy using Root Mean Square Error
        RMSE = sqrt(mean_squared_error(y_true=y_test, y_pred=y_prediction))
        #formatted_Home_RMSE = "{:.2f}".format(RMSE)
        formatted_Home_RMSE = round(RMSE)



        print("\nPredicted amount of goals using Linear Regression for {0}\nin their next game against {2} is: {1}".format(homeTeam, formatted_Home_RMSE,awayTeam))
        #print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_prediction))
        #print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_prediction))
        #print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_prediction)))

        ##Decision Tree Regressor - Fit a new regression model to the training set
        regressor = DecisionTreeRegressor(max_depth=20)
        regressor.fit(X_train, y_train)

        ##Perform Prediction using Decision Tree Regressor
        y_prediction = regressor.predict(X_test)
        y_prediction

        ##Evaluate Decision Tree Regression Accuracy using Root Mean Square Error
        RMSE2 = sqrt(mean_squared_error(y_true=y_test, y_pred=y_prediction))
        #formatted_Home_RMSE2 = "{:.2f}".format(RMSE2)
        formatted_Home_RMSE2 = round(RMSE2)
        print("\nPredicted amount of goals using Decision Tree Regression for {0}\nin their next game against {2} is: {1}".format(homeTeam, formatted_Home_RMSE2,awayTeam))



    except:
        sg.Popup("No dataset available")

    try:

        if ('Man United' in awayTeam):
            dataset = 'dataset/ManUAway.csv'
        elif ('Fulham' in awayTeam):
            dataset = 'dataset/FulhamAway.csv'
        elif ('Newcastle' in awayTeam):
            dataset = 'dataset/NewcastleAway.csv'
        elif ('Man City' in awayTeam):
            dataset = 'dataset/ManCAway.csv'
        elif ('Wolves' in awayTeam):
            dataset = 'dataset/WolvesAway.csv'
        elif ('Liverpool' in awayTeam):
            dataset = 'dataset/LiverpoolAway.csv'
        elif ('Southampton' in awayTeam):
            dataset = 'dataset/SouthamptonAway.csv'

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
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.75, train_size=0.25,random_state=324)
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        ##Perform Prediction using Linear Regression Model
        y_prediction = regressor.predict(X_test)



        sg.Print('\nPrediction for Away Team...', do_not_reroute_stdout=False)

        ##What is the mean of the expected target value in test set ?
        #print(y_test.describe())
        ##Evaluate Linear Regression Accuracy using Root Mean Square Error
        RMSE = sqrt(mean_squared_error(y_true=y_test, y_pred=y_prediction))
        #formatted_Away_RMSE = "{:.2f}".format(RMSE)
        formatted_Away_RMSE = round(RMSE)

        print("\nPredicted amount of goals using Linear Regression for {0}\nin their next game against {2} is: {1}".format(awayTeam, formatted_Away_RMSE,homeTeam))

        ##Decision Tree Regressor - Fit a new regression model to the training set
        regressor = DecisionTreeRegressor(max_depth=20)
        regressor.fit(X_train, y_train)

        ##Perform Prediction using Decision Tree Regressor
        y_prediction = regressor.predict(X_test)
        y_prediction

        ##Evaluate Decision Tree Regression Accuracy using Root Mean Square Error
        RMSE2 = sqrt(mean_squared_error(y_true=y_test, y_pred=y_prediction))
        #formatted_Away_RMSE2 = "{:.2f}".format(RMSE2)
        formatted_Away_RMSE2 = round(RMSE2)
        print("\nPredicted amount of goals using Decision Tree Regression for {0}\nin their next game against {2} is: {1}".format(awayTeam, formatted_Away_RMSE2,homeTeam))



    except:
        sg.Popup("No dataset available")

    #formatted_Home_RMSE = round(formatted_Home_RMSE)
    #formatted_Away_RMSE = round(formatted_Away_RMSE)

    #print("Predicted Match Score {0} : {1} - {2} : {3}".format(homeTeam,formatted_Home_RMSE,awayTeam,formatted_Away_RMSE))



f = open('dataset/E0.csv','r')
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


except requests.exceptions.ConnectionError:
    r.status_code = "Connection refused"