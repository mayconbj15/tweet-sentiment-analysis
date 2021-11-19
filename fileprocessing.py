import re
from scipy.sparse import data


def ProcessBase(dataFrame, sentiment_field, sentiments_list):
    dataFrame = FilterSentiments(dataFrame, sentiment_field, sentiments_list)
    dataFrame[sentiment_field] = CodeSet(dataFrame, sentiment_field, MakeMapSentimentoToCode(sentiments_list))

    return dataFrame

def PrintMetrics(dataFrame, field):
    print('Distribuição das classes')
    print(dataFrame[field].value_counts())

def PredictVectors(dataFrame, attributes_list):
    return dataFrame[attributes_list[0]], dataFrame[attributes_list[1]]

def FilterSentiments(dataFrame, sentiment_field, sentiments_list):
    return dataFrame[dataFrame[sentiment_field].isin(sentiments_list)]

def CodeSet(dataFrame, sentiment_field, mapping):
    return dataFrame[sentiment_field].map(mapping)

def MakeMapSentimentoToCode(sentiment_list):
    mapp = {}
    for i in range(0, len(sentiment_list)):
        mapp[sentiment_list[i]] = i

    return mapp

