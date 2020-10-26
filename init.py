from flask import Flask, send_file
from src.predict import predict
from tensorflow.keras.models import load_model


app = Flask(__name__)


@app.route("/")
def hello():
    return "Working!"


@app.route("/getGraph", methods=['GET'])
def get_graph():
    model = load_model('./models/model.h5')
    predict('./data/bitcoin.csv', model)
    return send_file('images/prediction.png', mimetype='image/png')


if __name__ == "__main__":
    app.run()