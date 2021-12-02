import os
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from keras_preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

LOCATE_PY_DIRECTION_PATH = os.path.abspath(os.path.dirname(__file__))
model = load_model(LOCATE_PY_DIRECTION_PATH + '/model2.h5')

num_words = 10000
tokenizer = Tokenizer(num_words=num_words)
maxlen = 150

APP = Flask(__name__)
API = Api(APP)

parser = reqparse.RequestParser()
parser.add_argument('text')


class Predict(Resource):

    @staticmethod
    def post():
        args = parser.parse_args()
        text = args['text']
        text = [text]
        text = tokenizer.texts_to_sequences(text)
        text = pad_sequences(text, maxlen=maxlen, dtype='int32', value=0)
        score = model.predict(text, batch_size=1, verbose=2)[0]
        score = score.tolist()
        result = ""
        if score[0] < 0.5:
            result = "negative"
        elif score[0] >= 0.5:
            result = "positive"


        return {"Label:": result, "Score:": score}


API.add_resource(Predict, '/predict')

if __name__ == '__main__':
    APP.run(port='5000')
