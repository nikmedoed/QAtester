import os
import pickle
from normalizeWords import *
import subprocess
import datetime
import shlex
import time
from math import sqrt
import timeit
from Duplicates import baseread

vectors = "D:\\BANKI_QA\\W2Vo\\Vectors\\"
W2Vdirectory = "D:\\BANKI_QA\\W2Vo\\"

# чтение документа с векторами - перевод во внутренее представление
def readDoc(path):
    f = open (path, "r", encoding="utf8")
    result = []
    temp = []
    w = True
    for line in f.readlines():
        line = line.replace("\n", "")
        if w:
            word = line
            w = False
        else:
            if len(line) < 2:
                if len(temp) > 0:
                    result.append({'w': word, 'vec': temp})
                    temp = []
                w = True
            else:
                if not "NOT" in line:
                    t = list(map(float, line.replace("[", "").replace("]", "").split()))
                    temp.extend(t)
    return result

#выполняет запрос (текстовый) и возвращает список вектором по нему
def W2Vreq (req):
    file = str(datetime.datetime.now()).replace(":", "-") + "-" + str(len(req)) + ".txt"
    file = file.replace(" ", "_")
    tofile(W2Vdirectory + "requests\\" + file, format(req))
    cmd = "C:\\Users\\sirne\\Anaconda2\\python.exe " + W2Vdirectory + "use_model.py " + \
          W2Vdirectory + "requests\\" + file + " " + W2Vdirectory + "Out\\" + file
    # bt = W2Vdirectory + file.replace("txt", "bat")
    # bat = open(bt, "w")
    # bat.write(cmd)
    # bat.close()
    # print(bt)
    proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    proc.wait()
    res = readDoc(W2Vdirectory + "Out\\" + file)
    # os.remove(vectors + line)
    return res

# загружает из бинарного файла вектор для документа
def getVec(file):
    bfile = open(file, "rb")
    base = pickle.load(bfile)
    bfile.close()
    return base

#перевод текстовых файлов с векторами в бинарники
def refiles():
    files = list(filter(lambda x: ('.hdr' in x), os.listdir(vectors)))
    print (len(files))
    # time.sleep(30 * 60)
    for line in files:
        data = readDoc(vectors + line)
        dump = open(vectors + line.replace(".hdr", ""), "wb")
        pickle.dump(data, dump)
        dump.close()
        os.remove(vectors + line)

#вычисление косинусного расстояния между векторами
def Rcos (a, b):
    c = len(a)
    d = len(b)
    x = 0
    y = 0
    z = 0
    if c != d:
        print("Oh, NO!")
    else:
        for i in range(0, c):
            x += a[i] * b[i]
            y += a[i] * a[i]
            z += b[i] * b[i]
        y = sqrt(y)
        z = sqrt(z)
        x = x / (y * z)
    return x

# сортирует словарь по значению
def sortDic(dic):
    res = list(sorted(dic.values()))
    res.reverse()
    result = {}
    resulten = []
    for i in range(0, len(res)):
        el = res[i]
        for j in dic:
            if dic.get(j) == el:
                result.update({i: j})
                resulten.append(j)
                dic.pop(j)
                break
    return {"dic": result, 'list': resulten}

# получает список веторов из запроса и список векторов из документа
def getResults(req, base):
    res = []
    tres = []
    for i in req:
        temp = []
        for j in base:
            temp.append(Rcos(i['vec'], j['vec']))
        # res.append(i['w'])
        tres.append(max(temp))
    return tres


def gIDtoID (gid, b):
    dic = {}
    for i in gid:
        f = "qa" + b[i]['listid'][0]
        dic.update({f: i})
    return dic

# переводит список файлов в словарь имя - данные
def readW2Vbase(files=[]):
    if files == []:
        b = baseread()
        for i in b:
            files.append("qa" + i['listid'][0])
        # files = os.listdir(vectors)
    res = {}
    for i in files:
        res.update({i: getVec(vectors + i)})
    return res

# files - это закаченные в память данные из файлов
def W2VmakeTestComp(req, files = []):
    rese = {}
    for a in files:
        base = files.get(a)
        rese.update({a: sum(getResults(req, base))})  # получили суммарное значение по одному документу
    t = sortDic(rese)
    return t

# получает вектор запроса и список имен файлов
def W2VmakeTest(req, ans):
    if ans == []:
        b = baseread()
        for i in b:
            ans.append("qa" + i['listid'][0])
    rese = {}
    for a in ans:
        base = getVec(vectors + a)
        rese.update({a: sum(getResults(req, base))})  # получили суммарное значение по одному документу
    t = sortDic(rese)
    return t

# попытка перегнать все вектора в большой файл
def tryVecToFile():
    b = baseread()
    base = []
    for i in b:
        base.append("qa" + i['listid'][0])
    base = readW2Vbase(base)
    bfile = open("vectorbase", "wb")
    pickle.dump(base, bfile)
    bfile.close()

def main():
    req = W2Vreq("Что делать, если потерял карту")
    ans = os.listdir(vectors)[0:40]
    a = timeit.default_timer()
    print(W2VmakeTest(req, ans))
    print("time", timeit.default_timer()-a)


if __name__ == '__main__':
    main()