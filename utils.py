import re
import matplotlib.pyplot as plt


def GetSentimentList(dataFrame, sentiment_field):
    sentiments_list = dataFrame[sentiment_field].unique().tolist()
    sentiments_list = [str(i) for i in sentiments_list]

    return sentiments_list


def PlotDf(df, sentiment_field):
    values = df[sentiment_field].value_counts()
    sentiment_list = GetSentimentList(df, sentiment_field)

    data = {}
    for sentiment in sentiment_list:
        data[ToSentimento(sentiment)] = values[int(sentiment)]

    courses = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    plt.bar(courses, values, color='maroon',
            width=0.4)

    plt.xlabel("Classe (Sentimentos)")
    plt.title("Distribuição das classes")
    plt.show()


def ToSentimento(sentiment):
    if sentiment == '1':
        return 'Positivo'
    if sentiment == '0':
        return 'Negativo'
    if sentiment == '2':
        return 'Neutro'
