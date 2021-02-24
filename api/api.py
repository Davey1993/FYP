import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>API Creation</h1><p>Testing API setup.</p>"

app.run()