import preprocessing


def GroupWords(texts):
    group = {}

    for text in texts:
        text = preprocessing.PreProcessing(text)
        for word in text.split(' '):
            quant = group.get(word)
            if quant == None:
                if word != '':
                    group[word] = 1
            else:
                if word != '':
                    group[word] = quant + 1

    return SortFunc(group)


def SortFunc(group):
    g1 = dict(sorted(group.items(), key=lambda item: item[1], reverse=True))

    return g1
