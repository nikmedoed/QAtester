from nltk.corpus import stopwords
from normalizeWords import format

def stopWfilter(text):
    stopwords_rus = list(map(lambda x: x.upper(), stopwords.words('russian')))
    form = format(text)
    res = []
    for i in form:
        if not i in stopwords_rus:
            res.append(i)
    return " ".join(res)

def main():
    print(stopWfilter("Ехал Грека через реку видит грека в река рак, я бы плюнул на все это но хочу все-таки сделать отдуши"))
    print(format("Ехал Грека через реку видит грека в река рак, я бы плюнул на все это но хочу все-таки сделать отдуши"))
    print(format(" ".join(stopWfilter("Ехал Грека через реку видит грека в река рак, я бы плюнул на все это но хочу все-таки сделать отдуши"))))

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()
