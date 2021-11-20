import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

from sklearn.feature_extraction.text import CountVectorizer

import re  # regex

nltk.download('stopwords')
nltk.download('rslp')

stop_words = stopwords.words('portuguese')


def PreProcessingList(tweetList):
    tweetList = [PreProcessing(i) for i in tweetList]

    return tweetList


def PreProcessing(tweet, trend=''):
    tweet = RemoveStopWords(tweet, stop_words)
    tweet = CleanAttribute(tweet, trend)
    #tweet = Stemming(tweet)

    # split pra quando tiver mais de um espaço em branco
    return ' '.join(tweet.split())


def CleanAttribute(attribute, trend):
    attribute = re.sub(r"http\S+", "", attribute)
    attribute = re.sub(r'[.,"\'-?:!;]', '', attribute)
    attribute = attribute.strip()

    # Remove trend
    attribute = attribute.replace(trend.lower(), "")

    return attribute


def RemoveStopWords(attribute, stop_words):
    words = [word for word in attribute.split() if not word in stop_words]

    return ' '.join(words)


def Stemming(instancia):
    stemmer = nltk.stem.RSLPStemmer()
    palavras = []
    for w in instancia.split():
        palavras.append(stemmer.stem(w))

    return (" ".join(palavras))


def GetVectorizer():
    tweet_tokenizer = TweetTokenizer()
    vectorizer = CountVectorizer(
        analyzer="word",
        tokenizer=tweet_tokenizer.tokenize,
        ngram_range=(1, 2)
    )

    return vectorizer
