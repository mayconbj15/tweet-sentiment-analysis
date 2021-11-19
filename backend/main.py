import pandas as pd
from scipy.sparse import data

import fileprocessing
import machinelearning
import preprocessing
import lexicon
import utils
import constants

CoronaSentimentList = ['Positive', 'Negative']
CoronaAttributes = ["OriginalTweet", "Sentiment"]
CoronaSentimentFieldName = 'Sentiment'

#KaggleSentimentList = ['Positivo', 'Negativo']
KaggleSentimentList = ['0', '1']
KaggleAttributes = ['tweet_text', 'sentiment']
KaggleSentimentFieldName = 'sentiment'


def GetData(file_name, separator=','):
    df = pd.read_csv(file_name, sep=separator)
    #utils.PlotDf(df, 'sentiment')

    return df


def CoronaDataFrame():
    dataFrame = GetData(constants.CORONA_NLP_FULL_FILE_PATH)[CoronaAttributes]
    fileprocessing.PrintMetrics(dataFrame, CoronaSentimentFieldName)
    dataFrame = fileprocessing.ProcessBase(
        dataFrame, CoronaSentimentFieldName, CoronaSentimentList)
    dataFrame[CoronaAttributes[0]] = preprocessing.PreProcessingList(
        dataFrame[CoronaAttributes[0]])

    return dataFrame


def KaggleDataFrame(file_path):
    dataFrame = GetData(file_path, separator=';')[KaggleAttributes]
    fileprocessing.PrintMetrics(dataFrame, KaggleSentimentFieldName)
    #dataFrame = fileprocessing.ProcessBase(dataFrame, KaggleSentimentFieldName, KaggleSentimentList)

    return dataFrame


def CoronaPredict(dataFrame, model):
    original_text, sentiment = fileprocessing.PredictVectors(
        dataFrame, CoronaAttributes)

    machinelearning.CrossValidation(model, original_text,
                                    sentiment, CoronaSentimentList)


def KaggleCrossValidation(dataFrame, model):
    original_text, sentiments = fileprocessing.PredictVectors(
        dataFrame, KaggleAttributes)

    sentiments_list = utils.GetSentimentList(dataFrame, 'sentiment')

    machinelearning.CrossValidation(
        model, original_text, sentiments, sentiments_list)


def KagglePredictLexicon(dataFrame):
    sentiments_list = dataFrame['sentiment'].unique().tolist()
    sentiments_list = [str(i) for i in sentiments_list]

    #dataFrame[KaggleAttributes[0]] = preprocessing.PreProcessingList(dataFrame[KaggleAttributes[0]])

    lexicon.LoadSentilex()
    lexicon.Predict(
        dataFrame, KaggleAttributes[0], KaggleAttributes[1], sentiments_list)


if __name__ == "__main__":
    #dataFrame = CoronaDataFrame()
    dataFrame = KaggleDataFrame(constants.KAGGLE_TRAIN_3CLASSES)

    dataFrame[KaggleAttributes[0]] = preprocessing.PreProcessingList(
        dataFrame[KaggleAttributes[0]])

    #model = machinelearning.LoadModel(constants.MODEL_BASE_PATH + 'Neural3Classes.sav')

    #machinelearning.CrossValidation2(model, dataFrame)
    model = machinelearning.NaiveBayesClassifier()
    # model = machinelearning.TrainModel(
    #    model, dataFrame[KaggleAttributes[0]], dataFrame[KaggleAttributes[1]])

    #machinelearning.SaveModel(model, constants.MODEL_BASE_PATH + '\\NaiveBayes3ClassesHidden1.sav')

    #test_data = GetData(constants.KAGGLE_TEST, separator=';')[KaggleAttributes]

    KaggleCrossValidation(dataFrame, model)
    # KagglePredictLexicon(dataFrame)

    print('para')
