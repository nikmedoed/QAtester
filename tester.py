import os
import zipfile
import re
import random
from math import log2
import datetime
import rarfile
from SearchEngine import *
from Duplicates import baseread
import timeit
from W2Vdriver import *
from stopWordsFilter import stopWfilter
import math

machineDirectory = "D:\\BANKI_QA\\Orignals\\"
testfldr = "tests\\" # + "Гот2\\"


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
    MRRpart = 0
    FalsePos = []
    for k in range(0, len(res)):
        i = k + 1
        IDCG += 1.0 / log2(i + 1)
        if res[k] in truRes:
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
            FalsePos.append(res[k])
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
    namesf = "soft0,7 mlen+0,5mlen"
    resfile = "Results\\" + str(datetime.datetime.now()).replace(":", "-") + namesf + ".txt"
    file = open(resfile, "w")
    file.write("Test name\tType\ttimeMin\tReqCou\tGrCou\tMax TP\tsoftOR\tStWdsFlt\tTruePositive\tPrecision\tRecall\tAccuracy\tError\tF-measure\tAPres@5\t" +
               "APres@10\tAPres@20\tAPres@50\tAveragePres\tnDCG@5\tnDCG@10\tnDCG@20\tnDCG@50\t" +
               "nDCG\tMRR\n")
    file.close()
    globalSres = [0] * 17
    globalSresA = [0] * 17
    globalSresWa = [0] * 17
    globalSresWm = [0] * 17
    globalSresWaS = [0] * 17
    globalSresWa10 = [0] * 17
    globalSresWaM = [0] * 17
    metods = 6
    coco = 0
    mTP = 0
    allfiles = list(filter(lambda x: ('.txt' in x), os.listdir(testfldr))) #[0:4]
    allfiles.reverse()
    allfiles = allfiles[0:25]
    gtime = timeit.default_timer()
    for test in allfiles:
        if "AT" in test:
            flag = "AT: "
        else:
            flag = ""
        a = timeit.default_timer()
        coco += 1
        ALL = len(base) #При необходимости научиться находить общее число документов при особых запросах, где попали не все
        print()
        ftest = open(testfldr+test, "r", encoding="cp1251")
        print("Number: ", str(allfiles.index(test) + 1) + "/" + str(len(allfiles)))
        print("test", test)
        quer = ftest.readline().replace("\n", "")
        softOR = ftest.readline().replace("\n", "")
        stopFilter = "True" in ftest.readline()
        ftest.readline()
        print(quer)
        print("softOr = ", softOR, "\nstopFilter = ", stopFilter)
        truRes = []
        for line in ftest.readlines():
            truRes.append(int(line.strip()))
        trc = len(truRes)
        mTP += trc

        # тест инфопоиска
        greq = req(quer, softOR, stopFilter)
        resul = IdToGroupid(greq, base)
        # resul состоит из двух элементов 'id' и 'all'
        res = resul['id']
        mlen = len(res)
        rc = len(greq)
        gc = len(res)
        print("- True results - count:", trc)
        print("- Search answers - count:", rc)
        print("- Search answers - Grouped count:", gc)

        b = timeit.default_timer()
        print("search metric test")
        searchTest = getTest(res, ALL, truRes)
        print(searchTest)
        for se in range(0, len(searchTest)):
            globalSres[se] += searchTest[se]
            globalSresA[se] += searchTest[se]
        min = round((timeit.default_timer() - a) / 60, 2)
        file = open(resfile, "a")
        file.write('\t'.join(list(map(str, [flag + quer, "InfoSearch", min, rc, gc, trc, softOR, stopFilter]))) + "\t")
        file.write('\t'.join(list(map(lambda x: str(round(x, 4)), searchTest)))+"\n")
        file.close()
        print("search test - OK")
        print("time (min): ", min, "\n")

        softOR = "0,7"
        greq = req(quer, softOR, stopFilter)
        resul = IdToGroupid(greq, base) #resul состоит из двух элементов 'id' и 'all'
        malen = math.trunc(mlen * 1.5)
        res = resul['id']
        res = res[0:malen]
        rc = len(greq)
        gc = len(res)
        c = timeit.default_timer()
        print("Search + W2V(avg) metric test")
        hDic = gIDtoID(resul['id'], base)
        W2Vquer = W2Vreq(quer)
        h = timeit.default_timer()
        res = W2VmakeTest(W2Vquer, hDic.keys(), met1)
        res = list(map(hDic.get, res['list']))[0:mlen]
        searchTest = getTest(res, ALL, truRes)
        print(searchTest)
        for se in range(0, len(searchTest)):
            globalSres[se] += searchTest[se]
            globalSresWa[se] += searchTest[se]
        min = round((b - a + timeit.default_timer() - c) / 60, 2)
        file = open(resfile, "a")
        file.write('\t'.join(list(map(str, [flag + quer, "InfoSearch&W2V(avg)", min, rc, gc, trc, softOR, stopFilter]))) + "\t")
        file.write('\t'.join(list(map(lambda x: str(round(x, 4)), searchTest)))+"\n")
        file.close()
        print("Search + W2V test - OK")
        print("time (min): ", min, "\n")

        j = timeit.default_timer()
        print("Search + W2V(avg10) metric test")
        res = W2VmakeTest(W2Vquer, hDic.keys(), met3)
        res = list(map(hDic.get, res['list']))[0:mlen]
        searchTest = getTest(res, ALL, truRes)
        print(searchTest)
        for se in range(0, len(searchTest)):
            globalSres[se] += searchTest[se]
            globalSresWa10[se] += searchTest[se]
        min = round((b - a + h - c + timeit.default_timer() - j) / 60, 2)
        file = open(resfile, "a")
        file.write('\t'.join(list(map(str, [flag + quer, "InfoSearch&W2V(avg10)", min, rc, gc, trc, softOR, stopFilter]))) + "\t")
        file.write('\t'.join(list(map(lambda x: str(round(x, 4)), searchTest)))+"\n")
        file.close()
        print("Search + W2V test - OK")
        print("time (min): ", min, "\n")

        d = timeit.default_timer()
        print("Search + W2V(max) metric test")
        res = W2VmakeTest(W2Vquer, hDic.keys(), met2)
        res = list(map(hDic.get, res['list']))[0:mlen]
        searchTest = getTest(res, ALL, truRes)
        print(searchTest)
        for se in range(0, len(searchTest)):
            globalSres[se] += searchTest[se]
            globalSresWm[se] += searchTest[se]
        min = round((b - a + h - c + timeit.default_timer() - d) / 60, 2)
        file = open(resfile, "a")
        file.write('\t'.join(list(map(str, [flag + quer, "InfoSearch&W2V(max)", min, rc, gc, trc, softOR, stopFilter]))) + "\t")
        file.write('\t'.join(list(map(lambda x: str(round(x, 4)), searchTest)))+"\n")
        file.close()
        print("Search + W2V test - OK")
        print("time (min): ", min, "\n")


        e = timeit.default_timer()
        print("Search + W2V(stopW+avg) metric test")
        W2Vquer = W2Vreq(stopWfilter(quer))
        px = timeit.default_timer()
        res = W2VmakeTest(W2Vquer, hDic.keys(), met1)
        res = list(map(hDic.get, res['list']))[0:mlen]
        searchTest = getTest(res, ALL, truRes)
        print(searchTest)
        for se in range(0, len(searchTest)):
            globalSres[se] += searchTest[se]
            globalSresWaS[se] += searchTest[se]
        min = round((b - a + h - c + timeit.default_timer() - e) / 60, 2)
        file = open(resfile, "a")
        file.write('\t'.join(list(map(str, [flag + quer, "InfoSearch&W2V(stopW+avg)", min, rc, gc, trc, softOR, stopFilter]))) + "\t")
        file.write('\t'.join(list(map(lambda x: str(round(x, 4)), searchTest)))+"\n")
        file.close()
        print("Search + W2V test - OK")
        print("time (min): ", min, "\n")


        pz = timeit.default_timer()
        print("Search + W2V(stopW+max) metric test")
        res = W2VmakeTest(W2Vquer, hDic.keys(), met2)
        res = list(map(hDic.get, res['list']))[0:mlen]
        searchTest = getTest(res, ALL, truRes)
        print(searchTest)
        for se in range(0, len(searchTest)):
            globalSres[se] += searchTest[se]
            globalSresWaM[se] += searchTest[se]
        min = round((b - a + h - c + pz - e + timeit.default_timer() - pz) / 60, 2)
        file = open(resfile, "a")
        file.write('\t'.join(list(map(str, [flag + quer, "InfoSearch&W2V(stopW+max)", min, rc, gc, trc, softOR, stopFilter]))) + "\t")
        file.write('\t'.join(list(map(lambda x: str(round(x, 4)), searchTest)))+"\n\n")
        file.close()
        print("Search + W2V test - OK")
        print("time (min): ", min, "\n")

    if coco > 0:
        for i in range(0, len(globalSres)):
            globalSres[i] /= coco * metods
            globalSresA[i] /= coco
            globalSresWa[i] /= coco
            globalSresWm[i] /= coco
            globalSresWaS[i] /= coco
            globalSresWa10[i] /= coco
            globalSresWaM[i] /= coco

    file = open(resfile, "a")
    file.write('\t'.join(list(map(str, ["\nGlobal", "", "", "", "", round(mTP/(coco* metods), 4) if coco > 0 else 0, "", ""]))) + "\t")
    file.write('\t'.join(list(map(lambda x: str(round(x, 4)), globalSres))) + "\n")
    file.write('\t'.join(list(map(str, ["Global", "InfoSearch", "", "", "", "", "", ""]))) + "\t")
    file.write('\t'.join(list(map(lambda x: str(round(x, 4)), globalSresA))) + "\n")
    file.write('\t'.join(list(map(str, ["Global", "InfoSearch&W2V(avg)", "", "", "", "", "", ""]))) + "\t")
    file.write('\t'.join(list(map(lambda x: str(round(x, 4)), globalSresWa))) + "\n")
    file.write('\t'.join(list(map(str, ["Global", "InfoSearch&W2V(avg10)", "", "", "", "", "", ""]))) + "\t")
    file.write('\t'.join(list(map(lambda x: str(round(x, 4)), globalSresWa10))) + "\n")
    file.write('\t'.join(list(map(str, ["Global", "InfoSearch&W2V(max)", "", "", "", "", "", ""]))) + "\t")
    file.write('\t'.join(list(map(lambda x: str(round(x, 4)), globalSresWm))) + "\n")
    file.write('\t'.join(list(map(str, ["Global", "InfoSearch&W2V(stopW+avg)", "", "", "", "", "", ""]))) + "\t")
    file.write('\t'.join(list(map(lambda x: str(round(x, 4)), globalSresWaS))) + "\n")
    file.write('\t'.join(list(map(str, ["Global", "InfoSearch&W2V(stopW+max)", "", "", "", "", "", ""]))) + "\t")
    file.write('\t'.join(list(map(lambda x: str(round(x, 4)), globalSresWaM))) + "\n")
    file.close()
    print("\nResults in " + resfile)
    print("Time: ", round((timeit.default_timer() - gtime) / 60, 2))

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()