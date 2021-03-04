import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
with open('C:/Users/David/PycharmProjects/pythonProject1/json/predictions.json', 'r') as myfile:
    data = myfile.read()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Football Prediction Application</h1>
<p>A prototype API for Premier League Predictions</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/football/premierLeague/all', methods=['GET'])
def api_all():
    return jsonify(data)


app.run()
