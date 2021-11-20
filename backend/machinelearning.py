from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import ComplementNB, MultinomialNB

from sklearn.pipeline import Pipeline

from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

from sklearn.feature_extraction.text import CountVectorizer

from sklearn import neural_network
from sklearn import svm

from nltk.tokenize import TweetTokenizer

import time

import pickle

import preprocessing
import constants

trained = False


def NaiveBayesPipeline():
    return Pipeline([
        ('counts', preprocessing.GetVectorizer()),
        ('classifier', MultinomialNB())
    ])


def NaiveBayesClassifier():
    return MultinomialNB()


def SVMClassifier():
    return Pipeline([
        ('counts', preprocessing.GetVectorizer()),
        ('classifier', svm.SVC())
    ])


def NeuralNetwork():
    print('LOADING NEURAL NETWORK')
    return Pipeline([
        ('counts', CountVectorizer()),
        ('classifier', neural_network.MLPClassifier(
            hidden_layer_sizes=(3,),
            learning_rate_init=0.2,  # ok
            momentum=0.3,
            max_iter=400
        ))
    ])

    # neural_network.MLPClassifier
    # random_state=1,
    # learning_rate_init=0.05,
    # learning_rate='adaptive',
    # activation='logistic',
    # hidden_layer_sizes=3


def SaveModel(model, filePath):
    pickle.dump(model, open(filePath, 'wb'))


def LoadModel(filePath):
    model = pickle.load(open(filePath, 'rb'))

    return model


def PipelineCrossValidation(pipeline, tweets, classes, sentiments_list):
    start_time = time.time()

    print('PREDICTING')
    result = cross_val_predict(pipeline, tweets, classes, cv=10)

    end_time = time.time()
    print('Time (miliseconds): ', (end_time - start_time)*1000)

    PrintResult(classes, result, sentiments_list)

    SaveModel(pipeline, constants.MODEL_BASE_PATH + 'MLPClassifierTest.sav')

# Return a list of predicted values


def NaiveBayesCrossValidation(model, freq_tweets, classes):
    start_time = time.time()

    print('CROSS VAL PREDICTING')
    result = cross_val_predict(model, freq_tweets, classes, cv=10)

    end_time = time.time()
    print('Time (miliseconds): ', (end_time - start_time)*1000)

    return result


def PredictExpected(model, actual, expected, sentiments_list):
    start_time = time.time()

    result = PredictList(model, actual)
    end_time = time.time()
    print('Time (miliseconds): ', (end_time - start_time)*1000)

    PrintResult(expected, result, sentiments_list)


def TrainModel(model, tweets, classes):
    print("Train Model")
    model.fit(tweets, classes)

    return model


def PredictList(model, tweets, trend=''):
    print('PREDICTING')
    start_time = time.time()
    tweets = [preprocessing.PreProcessing(i, trend) for i in tweets]

    end_time = time.time()
    print('Time (miliseconds): ', (end_time - start_time)*1000)

    return model.predict(tweets)


def PrintResult(expected_values, predict_values, sentiments_list):
    matrix = confusion_matrix(expected_values, predict_values)
    print("Matrix de confusão das classes",
          " ".join(sentiments_list), '\n', matrix, "\n")

    print(classification_report(expected_values,
                                predict_values, target_names=sentiments_list))

    print('Acurácia do modelo: {}'.format(
        accuracy_score(expected_values, predict_values)))
