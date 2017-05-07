from nltk.tokenize import sent_tokenize
import pymorphy2
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import os
from multiprocessing import Process

machineDirectory = "D:\\BANKI_QA\\W2V-i\\W2V-allfiles\\alltxt\\"

def format(text):
    morph = pymorphy2.MorphAnalyzer()
    punc = ["/", "?", "!", ".", ",", " - ", "+", "*", "\"", ":", ";", "(", ")", "—", "«", "»", "…"]
    for i in punc:
        text = text.replace(i, "")

    # sentences = sent_tokenize(text)
    # for i in sentences:
    #     print( word_tokenize(i))
    return list(map(lambda x: morph.parse(x)[0].normal_form.upper(), text.split()))

def tofile (file, text):
    fi = open(file, "w", encoding='utf8')
    text = "\n".join(text)
    # text = text.encode("cp1251")
    # text = text.decode('utf-8')
    fi.write(text)
    fi.close()

def chunks(lst, chunk_size):
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

def driver(list):
    for i in list:
        fi = open(machineDirectory + i, "r")
        tofile("D:\\BANKI_QA\\W2Vo\\NormalizedDocs\\" + i, format(fi.read()))
        print(i)
        fi.close()

def main():
    files = list(filter(lambda x: ('hdr' in x), os.listdir(machineDirectory)))
    files = chunks(files, (len(files)//4) + 1)
    for i in files:
        Process(target=driver, args=([i])).start()

if __name__ == '__main__':
    main()