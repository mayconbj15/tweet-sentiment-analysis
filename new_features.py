import json
import preprocessing


def GroupWords(texts):
    group = {}

    for text in texts:
        text = preprocessing.PreProcessing(text)
        for word in text.split(' '):
            quant = group.get(word)
            if quant == None:
                group[word] = 1
            else:
                group[word] = quant + 1

    return group


def SortFunc(group):
    g1 = dict(sorted(group.items(), key=lambda item: item[1], reverse=True))

    return g1


def SortWords(dataList):
    group = GroupWords(dataList)
    group = SortFunc(group)


def LoadJson(filePath):
    f = open(filePath,)
    data = json.load(f)
    f.close()

    return data


if __name__ == "__main__":
    texts = []

    data = LoadJson('data.json')

    for i in data['data']:
        texts.append(i['text'])

    group = GroupWords(texts)
    group = SortFunc(group)

    print('end')
