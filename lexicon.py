from os import pipe

import machinelearning


dic_word_polarity = {}

lexicon = 'LIWC'

positive_list = ['126']
negative_list = ['127']

LIWC_FILE_PATH = 'files\lexicons\LIWC2007.txt'


def LoadSentilex():
    print('LOADING SENTILEX')
    sentilexpt = open('files\lexicons\SentiLex-flex-PT02.txt',
                      'r', encoding='UTF-8')
    global dic_word_polarity

    for i in sentilexpt.readlines():
        pos_ponto = i.find('.')
        palavra = (i[:pos_ponto]).split(',')[0]

        pol = i[pos_ponto+1:len(i)].split(';')[3]
        polaridade = pol[7:]

        # if polaridade != '1' and polaridade != '0' and polaridade != '-1':
        #    raise Exception('ERROR')

        #dic_palavra_polaridade[palavra] = polaridade
        AddWordAndPolarity(palavra, polaridade)

    lexicon = 'Sentilex'


def LoadLIWC():
    liwc = open(LIWC_FILE_PATH, 'r', encoding='UTF-8')
    lines = liwc.readlines()
    global dic_word_polarity

    for line in lines[0:64]:
        line_split = line.replace('\n', '').split('\t')
        dic_word_polarity[line_split[0]] = line_split[1]

    for line in lines[66:]:
        word_line = line.replace('\n', '').split('\t')
        word = word_line[0]
        word_attributes = word_line[1: len(word_line)]

        dic_word_polarity[word] = word_attributes


def AddWordAndPolarity(palavra, polaridade):
    global dic_word_polarity
    lista_palavras = dic_word_polarity.get(palavra[0])

    if lista_palavras == None:
        dic_word_polarity[palavra[0]] = [{palavra, polaridade}]
    else:
        lista_palavras.append({palavra, polaridade})
        dic_word_polarity[palavra[0]] = lista_palavras


def ScoreSentiment(phrase):
    if lexicon == 'LIWC':
        return ScoreSentimentLIWC(phrase)
    else:
        return ScoreSentimentSentilex(phrase)


def ScoreSentimentSentilex(frase):
    frase = frase.lower()
    l_sentimento = []

    for p in frase.split():
        l_sentimento.append(int(dic_word_polarity.get(p, 0)))

    score = sum(l_sentimento)
    if score > 0:
        return 1
    elif score < 0:
        return -1
    else:
        return 0


def ScoreSentimentLIWC(phrase):
    sentiment = 0
    for p in phrase.split():
        p = p.lower()
        word_attributes = dic_word_polarity.get(p)
        if word_attributes != None:
            for word_attribute in word_attributes:
                if word_attribute in positive_list:
                    sentiment += 1
                elif word_attribute in negative_list:
                    sentiment -= 1

    if sentiment > 0:
        return 1
    elif sentiment < 0:
        return 0
    else:
        return 2


def Predict(dataFrame, field_sentiment, field_text, sentiments_list):
    actual_values = []
    for phrase in dataFrame[field_sentiment]:
        actual_values.append(ScoreSentiment(phrase))

    expected_values = dataFrame[field_text].tolist()

    machinelearning.PrintResult(
        expected_values, actual_values, sentiments_list)


if __name__ == "__main__":
    # LoadSentilex()
    LoadLIWC()

    print(ScoreSentimentSentilex('Eu estou triste'))

    print('end')
