/////////Imports///////////////////////////////

const serverless = require('serverless-http');
const express = require("express"); 
const app = express();
const bodyParser = require("body-parser");
const AWS = require("aws-sdk");
const db = new AWS.DynamoDB.DocumentClient();
const { v4: uuidv4 } = require('uuid'); // I am using uuidv4 for creating id's for our predictions
var fs = require('fs');

//content = fs.readFileSync('C:/Users/David/PycharmProjects/pythonProject1/json/predictions.json');
//var config = JSON.parse(content);
//x = config.name

//console.log(x);


app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

/////////////////////// Prediction Endpoints //////////////////////////////////////

//This adds a new prediction
app.post("/predictions", async (req, res) => {
  const data = req.body;
  data.forEach(async(value)=>{
    const params = {
      TableName: "predictionsTable",
      Item: {
        id: uuidv4(),
        homeTeam: value.homeTeam,
        awayTeam: value.awayTeam,
        homeTeamScore: value.homeTeamScore,
        awayTeamScore: value.awayTeamScore
      },
    };
  
    try {
      await db.put(params).promise();
      res.status(201).json({ prediction: params.Item});
    } catch (e) {
      res.status(500).json({ error: e.message });
    }
  })

});

//This edits the prediction by id
app.put("/predictions/:id", async (req, res) => {
  const data = req.body;
  const params = {
    TableName: "predictionsTable",
    Item: {
      id: data.id,
      homeTeam: data.homeTeam,
      awayTeam: data.awayTeam,
      homeTeamScore: data.homeTeamScore,
      awayTeamScore: data.awayTeamScore
    },
  }
  await db.put(params).promise();
  res.status(200).json({ prediction: params.Item});
});

//This gets all predictions in the database
app.get("/predictions", async (req, res) => {
  const params = {
    TableName: "predictionsTable",
  };

  const result = await db.scan(params).promise();
  res.status(200).json({ predictions: result });
});

//This deletes a prediction by id
app.delete("/predictions/:id", async (req, res) => {
  const params = {
    TableName: "predictionsTable",
    Key: {
      id: req.params.id
    },
  };

  await db.delete(params).promise();
  res.status(200).json({ success: true });

});


module.exports.app = serverless(app);