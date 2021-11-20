import pandas as pd
from scipy.sparse import data
from sklearn.naive_bayes import MultinomialNB

import fileprocessing
import machinelearning
import preprocessing
import lexicon
import utils
import constants

KaggleSentimentList = ['0', '1']
KaggleAttributes = ['tweet_text', 'sentiment']
KaggleSentimentFieldName = 'sentiment'


def GetData(file_name, separator=','):
    df = pd.read_csv(file_name, sep=separator)
    #utils.PlotDf(df, 'sentiment')

    return df


def KaggleDataFrame(file_path):
    dataFrame = GetData(file_path, separator=';')[KaggleAttributes]
    fileprocessing.PrintMetrics(dataFrame, KaggleSentimentFieldName)
    #dataFrame = fileprocessing.ProcessBase(dataFrame, KaggleSentimentFieldName, KaggleSentimentList)

    return dataFrame


def KaggleCrossValidation(dataFrame, model):
    original_text, sentiments = fileprocessing.PredictVectors(
        dataFrame, KaggleAttributes)

    sentiments_list = utils.GetSentimentList(dataFrame, 'sentiment')

    machinelearning.PipelineCrossValidation(
        model, original_text, sentiments, sentiments_list)


def KagglePredictLexicon(dataFrame):
    sentiments_list = dataFrame['sentiment'].unique().tolist()
    sentiments_list = [str(i) for i in sentiments_list]

    #dataFrame[KaggleAttributes[0]] = preprocessing.PreProcessingList(dataFrame[KaggleAttributes[0]])

    lexicon.LoadSentilex()
    lexicon.Predict(
        dataFrame, KaggleAttributes[0], KaggleAttributes[1], sentiments_list)


def NaiveBayesClassification(dataFrame):
    model = machinelearning.NaiveBayesClassifier()

    vectorizer = preprocessing.GetVectorizer()

    freq_tweets = vectorizer.fit_transform(dataFrame[KaggleAttributes[0]])

    result = machinelearning.NaiveBayesCrossValidation(
        model, freq_tweets, dataFrame[KaggleAttributes[1]])

    sentiments_list = utils.GetSentimentList(dataFrame, 'sentiment')

    machinelearning.PrintResult(
        dataFrame[KaggleAttributes[1]], result, sentiments_list)


if __name__ == "__main__":
    dataFrame = KaggleDataFrame(constants.KAGGLE_TRAIN_3CLASSES)

    dataFrame[KaggleAttributes[0]] = preprocessing.PreProcessingList(
        dataFrame[KaggleAttributes[0]])

    NaiveBayesClassification(dataFrame)
    #model = machinelearning.SVMClassifier()
    #KaggleCrossValidation(dataFrame, model)
