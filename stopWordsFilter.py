from nltk.corpus import stopwords


def main():
    stopwords_rus = set(stopwords.words('russian'))
    print (stopwords_rus)


if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()
