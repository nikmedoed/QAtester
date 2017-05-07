import os
import zipfile
import re
import random
from math import log2
import datetime
import rarfile
from SearchEngine import *
from Duplicates import baseread

machineDirectory = "D:\\BANKI_QA\\Orignals\\"
testfldr = "tests\\"


def IdToGroupid (res, base):
    real = []
    result = []
    for i in res:
        for j in base:
            if "0" + i in j['listid']:
                if not (j['groupid'] in real):
                    real.append(j['groupid'])
                    result.append(j)
                    break
    return {'id': real, "all": result}


def getQA(test): # по списку id возвращает список словарей с вопросами и ответами
    # files = list(filter(lambda x: x.startswith('qa') and ('hdr' in x), os.listdir(machineDirectory)))
    # print(files)
    id = []
    for i in test:
        fil = "qa0"+str(i)+".hdr"
        # print(fil)
        try:
            f = open(machineDirectory + fil, "r")
            for t in range(17):
                text = f.readline()
            # text = text.decode("cp1251")
            id.append({'id': i, 'q': re.sub("<NOMORPH><FONT=\"GREY\">Answer: .*", "", re.sub("MRM_snippet = Question: ", "", text)),
                          'a': re.sub(".*<NOMORPH><FONT=\"GREY\">Answer: ", "", text.replace("</FONT></NOMORPH>", ""))})
            f.close()
            # print (fil, "Ok")
        except Exception:
            print (fil, "skipped")
    return id


def reverseRepeater(test): # объединяет дубликаты в группы, т.е. остается список id, вопрос и ответ для них
    result = []
    while len(test)>0:
        elem = test.pop(0)
        result.append({'id': [elem['id']], 'q': elem['q'], 'a': elem['a']})
        i = 0
        while i < len(test):
            if elem['q'] == test[i]['q']:
                result[len(result)-1]['id'].append(test[i]['id'])
                del test[i]
            else:
                i += 1
    return result


def getTest(res, ALL, truRes):
    TP = 0
    DCG5 = 0
    DCG10 = 0
    DCG20 = 0
    DCG50 = 0
    DCG = 0
    APres5 = 0
    APres10 = 0
    APres20 = 0
    APres50 = 0
    APres = 0
    Cont = 0
    IDCG = 0
    nDCG5 = 0
    nDCG10 = 0
    nDCG20 = 0
    nDCG50 = 0
    FalsePos = []
    for i in range(1, len(res)):
        IDCG += 1.0 / log2(i + 1)
        if res[i - 1] in truRes:
            TP += 1
            if Cont == 0:
                MRRpart = 1.0 / i
            Cont += 1
            forap = Cont / i
            fordcg = 1.0 / log2(1 + i)
            if i <= 5:
                DCG5 += fordcg
                APres5 += forap
            if 5 < i <= 10:
                DCG10 += fordcg
                APres10 += forap
            if 10 < i <= 20:
                DCG20 += fordcg
                APres20 += forap
            if 20 < i <= 50:
                DCG50 += fordcg
                APres50 += forap
            DCG += fordcg
            APres += forap
        else:
            FalsePos.append(res[i - 1])
        if i == 5:
            nDCG5 = DCG5 / IDCG
        if i == 10:
            nDCG10 = (DCG10 + DCG5) / IDCG
        if i == 20:
            nDCG20 = (DCG20 + DCG10 + DCG5) / IDCG
        if i == 50:
            nDCG50 = (DCG50 + DCG20 + DCG10 + DCG5) / IDCG
    nDCG = DCG / IDCG
    APres50 = (APres50 + APres5 + APres10 + APres20) / 50
    APres20 = (APres5 + APres10 + APres20) / 20
    APres10 = (APres5 + APres10) / 10
    APres5 /= 5
    if len(res) > 0:
        APres /= len(res)
        Precision = TP * 1.0 / len(res)
    else:
        APres = 0
        Precision = 0
    if len(truRes) > 0:
        Recall = TP * 1.0 / len(truRes)
    else:
        Recall = 0
    Accuracy = (TP + ALL - len(res) + TP - len(truRes)) / ALL
    Error = (len(res) - TP + len(truRes) - TP) / ALL
    if Precision == 0 or Recall == 0:
        Fmeasure = 0
    else:
        Fmeasure = 2.0 / ((1.0 / Precision) + (1.0 / Recall))
    return [TP, Precision, Recall, Accuracy, Error, Fmeasure, APres5, APres10, APres20, APres50, APres,
            nDCG5, nDCG10, nDCG20, nDCG50, nDCG, MRRpart]

def main():
    base = baseread()
    resfile = "Results\\" + str(datetime.datetime.now()).replace(":", "-") + ".txt"
    file = open(resfile,"w")
    file.write("Test name\tTruePositive\tPrecision\tRecall\tAccuracy\tError\tF-measure\tAPres@5\t" +
               "APres@10\tAPres@20\tAPres@50\tAveragePres\tnDCG@5\tnDCG@10\tnDCG@20\tnDCG@50\t" +
               "nDCG\tMRR\n")
    globalSres = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    coco = 0
    for test in os.listdir(testfldr):
        coco += 1
        ALL = len(base) #Todo научиться находить общее число документов при особых запросах
        ftest = open(testfldr+test)
        quer = ftest.readline().replace("\n", "")
        softOR =  ftest.readline().replace("\n", "")
        stopFilter = "True" in ftest.readline()
        ftest.readline()
        truRes = []
        for line in ftest.readlines():
            truRes.append(line.strip())

        # тест search
        resul = IdToGroupid (req(quer, softOR, stopFilter), base)
        # resul состоит из двух элементов 'id' и 'all'
        res = resul['id']
        searchTest = getTest(res, ALL, truRes)
        for se in range(0, len(searchTest)-1):
            globalSres[se] += searchTest[se]

        file.write(test + "\t")  # testname
        file.write('\t'.join(searchTest)+"\n")
    if coco > 0:
        for i in range(0, len(globalSres) - 1):
            globalSres[i] /= coco
    else:
        for i in range(0, len(globalSres) - 1):
            globalSres[i] = 0
    file.write("\nGlobal") #testname
    file.write('\t'.join(globalSres) + "\n")
    file.close()
    print ("Results in " + resfile)

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()