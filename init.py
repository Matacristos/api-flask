from flask import Flask, send_file
app = Flask(__name__)


@app.route("/")
def hello():
    return "Working!"


@app.route("/getGraph", methods=['GET'])
def get_graph():
    return send_file('images/graph.png', mimetype='image/png')


if __name__ == "__main__":
    app.run()