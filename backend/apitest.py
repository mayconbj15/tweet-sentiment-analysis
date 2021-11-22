from flask import Flask, json, request, jsonify

import flask
from flask.wrappers import Response

import main
import machinelearning
import fileprocessing
import preprocessing
import constants
import analysis

app = Flask(__name__)
app.config["DEBUG"] = True


KaggleAttributes = ['tweet_text', 'sentiment']
model = None

# Train model


def TrainAndSaveModel(baseName):
    dataFrame = main.KaggleDataFrame(
        constants.KAGGLE_BASE_PATH + baseName)

    model = machinelearning.NeuralNetwork()

    original_text, sentiments = fileprocessing.PredictVectors(
        dataFrame, KaggleAttributes)

    model = machinelearning.TrainModel(model, original_text, sentiments)
    machinelearning.SaveModel(
        model, constants.MODEL_BASE_PATH + baseName.replace('.csv', '.sav'))


if machinelearning.trained == False:
    print("Training models")
    #dataFrame = TrainAndSaveModel(constants.KAGGLE_TRAINING_50_SUFFIX)
    #dataFrame = TrainAndSaveModel(constants.KAGGLE_TRAINING_100_SUFFIX)
    #dataFrame = TrainAndSaveModel(constants.KAGGLE_TRAINING_200_SUFFIX)
    #dataFrame = TrainAndSaveModel(constants.KAGGLE_TRAINING_300_SUFFIX)
    #dataFrame = TrainAndSaveModel(constants.KAGGLE_TRAINING_400_SUFFIX)
    #dataFrame = TrainAndSaveModel(constants.KAGGLE_TRAINING_500_SUFFIX)
    model = machinelearning.LoadModel(
        constants.MODEL_BASE_PATH + "NaiveBayesFinalModel.sav")
    machinelearning.trained = True
    trained = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.post("/tweets/sentiments")
def predict_sentiments():
    tweets = json.loads(request.data)["data"]
    trend = request.args["Trend"]

    sentiments = machinelearning.PredictList(model, tweets, trend)
    responseBody = {}
    responseBody["data"] = []

    for i in range(0, len(tweets)):
        responseBody["data"].append(
            {"tweet": tweets[i], "sentiment": int(sentiments[i])})

    responseBody["distribution"] = {'positive': 0, 'negative': 0, 'neutral': 0}
    quantPositive = 0
    quantNeutral = 0
    quantNegative = 0
    for i in range(0, len(tweets)):
        if int(sentiments[i]) == 0:
            quantNegative += 1
        elif int(sentiments[i]) == 1:
            quantPositive += 1
        else:
            quantNeutral += 1

    responseBody["distribution"]["negative"] = quantNegative
    responseBody["distribution"]["positive"] = quantPositive
    responseBody["distribution"]["neutral"] = quantNeutral

    preProcessingsTweets = preprocessing.PreProcessingList(tweets)
    responseBody["group"] = analysis.GroupWords(preProcessingsTweets)

    r = (0.75*quantPositive + 0.94*quantNeutral + 0.78*quantNegative) / \
        (quantPositive+quantNeutral+quantNegative)
    responseBody["globalSentiment"] = r

    response = app.response_class(
        response=json.dumps(responseBody),
        status=200,
        mimetype='application/json',
        headers={"Access-Control-Allow-Origin": "*"}
    )

    return response


@app.post("/tweets/groupwords")
def groupWords():
    tweets = json.loads(request.data)["data"]

    group = analysis.GroupWords(tweets)

    response = app.response_class(
        response=json.dumps(group),
        status=200,
        mimetype='application/json',
        headers={"Access-Control-Allow-Origin": "*"}
    )


@app.post("/tweets/sentiments_teste")
def teste():
    if request.is_json:
        tweets = request.get_json()["data"]
        responseBody = {}
        responseBody["data"] = []

        responseBody["data"].append("teste")

        response = app.response_class(
            response=json.dumps(responseBody),
            status=200,
            mimetype='application/json',
            headers={"Access-Control-Allow-Origin": "*"}
        )

        return response
    return {"error": "Request must be JSON"}, 415


app.run(use_reloader=False, port=5001)
