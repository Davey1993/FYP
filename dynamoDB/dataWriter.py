import json

import boto3
import uuid


with open('C:/Users/David/PycharmProjects/FinalYearProject/project4-Davey1993/json/predictions.json') as data_file:
    data = json.load(data_file)
#print(data)



myUUID = str(uuid.uuid4())

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
dynamoTable = dynamodb.Table('predictionsTable')
dynamoTable.put_item(
    Item={
        "id": myUUID,
        "awayTeamScore": data['awayTeamScore'],
        "homeTeam": data['homeTeam'],
        "homeTeamScore": data['awayTeamScore'],
        "awayTeam": data['awayTeam']
    })
