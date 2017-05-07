import http.client
import urllib.parse
import json
import os
import zipfile
import re
import random
from math import log2
import datetime
import rarfile

import pickle


serva = "localhost:2085"
format = "json"
machineDirectory = "D:\\BANKI_QA\\Orignals\\"
testfldr = "tests\\"

#byClaters = True
#byClaters = False

def updateID(test):
    base=[]
    bfile = open("base", "rb")
    base = pickle.load(bfile)
    bfile.close()
    return list(map(lambda x: base[x], test))

def GETQuery(q):
    conn = http.client.HTTPConnection(serva)
    conn.request("GET", q)
    data1 = json.loads(conn.getresponse().read())
    ids = []
    for x in data1['rows']:
        ids.append(str(x['id']))
    conn.close()
    return updateID(ids)


def req(reque, softOR = 0, stopw = False):
    docShow = "1000000"
    stext = urllib.parse.quote(reque)
    #print(stext + "\n")
    #("&show_by_clust=1" if byClaters else "") + "&clust_doc_cnt=3&clust_doc_ft=3&clust_doc_order=1" + \
    query = "/?doccnt=" + docShow + ("&reqext_stopword=1" if stopw else "") + "&soft_or_coef=" + str(softOR) + \
                "&zone=0&class_id=-1&show=json&informer=100&min_wt=0&reqext=1&req_params=1&hl_one_feat=1&descr=1" + \
                "&save_query=1&calc_rank_type=0&snip_size=350&use_query_val=270433453622&reqtext=" +stext + \
                "&report_doccnt=500&report_win=150&report_sent=3&report_frag=1000&report_max_shift=10000" +\
                "&report_min_wt=0.01&report_hl=1&report_clust=1&report_rq_non_clst=1&report_cls_type=1&report_cls=" +\
                "&report_cls_data=&thes_rep_doc_cnt=10&thes_rep_ext=1&report_type=1&report_order=1&thes_rep_dop_doc_sent_cnt=2&rep_dop_reqtext=&clust_report_doc_ft=3&clust_report_max_cnt=100&clust_report_doc_in_clust_max_cnt=4&clust_report_n_first_sent=0&clust_report_doc_min_rank=0&clust_report_doc_in_clust_min_cnt=1&clust_doc_order=0&clust_report_cls_type=1&clust_report_cls=event.%D0%B8%D0%BD%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2%D0%B0&clust_report_cls_data=&clust_report_src_ranks=&orderby=0&backUrl=%2F&tree_checked_list=&thes_rep_conc_id=-1"
    # print (query)
    return GETQuery(query)


def getQA(test):
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

def reverseRepeater(test):
    result = []
    while len(test)>0:
        elem = test.pop(0)
        result.append({'id': [elem['id']], 'q': elem['q'], 'a': elem['a']})
        i = 0
        while i < len(test):
            if elem['a'] == test[i]['a']:
                result[len(result)-1]['id'].append(test[i]['id'])
                del test[i]
            else:
                i += 1
    return result


# print(getQA(test))

def main():
    gP=0
    gR=0
    gF=0
    gA = 0
    gE = 0
    gnDCG=0
    gAP=0
    MRR=0
    gnDCG5 = 0
    gnDCG10 = 0
    gnDCG20 = 0
    gnDCG50 = 0
    gAPres5 = 0
    gAPres10 = 0
    gAPres20 = 0
    gAPres50 = 0
    coco=0
    resfile = "Results\\" + str(datetime.datetime.now()).replace(":", "-") + ".txt"
    file = open(resfile,"w")
    file.write("Test name\tPrecision\tRecall\tF-measure\tAccuracy\tError\tAverage Precision (AP)\tAP@5\tAP@10\tAP@20\tAP@50\tnDCG\tnDCG@5\tnDCG@10\tnDCG@20\tnDCG@50\n")
    for test in os.listdir(testfldr):
        TP=0
        coco += 1
        ALL = 541588 #Todo научиться находить общее число документов при особых запросах
        # Todo удалить повторы
        f = open(testfldr+test)
        res = req(f.readline().replace("\n", ""), f.readline().replace("\n", ""), "True" in f.readline() ) # req, softOR, стоп-слова
        f.readline()
        # if "text" in f.readline():
        #     res = req(f.readline())
        #     f.readline()
        # else:
        #     res = GETQuery(f.readline())
        #     f.readline()
        truRes = []
        for line in f.readlines():
            temp =line.strip()
            if temp in res:
                TP += 1
            truRes.append(temp)
        Precision = TP*1.0 / len(res)
        Recall = TP*1.0/ len(truRes)
        Accuracy = (TP+ALL-len(res)+TP-len(truRes))/ALL
        Error = (len(res)-TP+len(truRes)-TP)/ALL
        Fmeasure = 2.0/((1.0/Precision)+(1.0/Recall))
        #получаем res и truRes надо отправить на оценку
        DCG5=0
        DCG10=0
        DCG20=0
        DCG50=0
        DCG=0
        APres5=0
        APres10=0
        APres20=0
        APres50=0
        APres=0
        Cont=0
        IDCG=0
        nDCG5 = 0
        nDCG10 = 0
        nDCG20 = 0
        nDCG50 = 0
        for i in range(1,len(res)):
            IDCG += 1.0/log2(i+1)
            if res[i-1] in truRes:
                if Cont == 0:
                    MRR += 1.0/i
                Cont += 1
                forap = Cont/i
                fordcg = 1.0/log2(1+i)
                if i <= 5:
                    DCG5 += fordcg
                    APres5 += forap
                if i<=10:
                    DCG10 += fordcg
                    APres10 += forap
                if i<=20:
                    DCG20 += fordcg
                    APres20 += forap
                if i<=50:
                    DCG50 += fordcg
                    APres50 += forap
                DCG += fordcg
                APres += forap
            if i == 5:
                nDCG5 = DCG5 / IDCG
            if i == 10:
                nDCG10 = DCG10 / IDCG
            if i == 20:
                nDCG20 = DCG20 / IDCG
            if i == 50:
                nDCG50 = DCG50 / IDCG
        nDCG = DCG / IDCG
        APres5 /= 5
        APres10 /= 10
        APres20 /= 20
        APres50 /= 50
        APres /= len(res)

        gP += Precision
        gR += Recall
        gA += Accuracy
        gE += Error
        gF += Fmeasure
        gnDCG += nDCG
        gAP += APres
        gnDCG5 += nDCG5
        gnDCG10 += nDCG10
        gnDCG20 += nDCG20
        gnDCG50 += nDCG50
        gAPres5 += APres5
        gAPres10 += APres10
        gAPres20 += APres20
        gAPres50 += APres50
        file.write('\t'.join(map(str,[test, Precision, Recall, Fmeasure, Accuracy, Error, APres, APres5, APres10, APres20, APres50, nDCG, nDCG5, nDCG10, nDCG20, nDCG50]))+"\n")
    gP /= coco
    gR /= coco
    gA /= coco
    gE /= coco
    gF /= coco
    gnDCG /= coco
    gAP /= coco
    MRR /= coco
    gnDCG5 /= coco
    gnDCG10 /= coco
    gnDCG20 /= coco
    gnDCG50 /= coco
    gAPres5 /= coco
    gAPres10 /= coco
    gAPres20 /= coco
    gAPres50 /= coco
    file.write("\nGlobal\n")

    file.write('\t'.join( map(str,["ALL", gP, gR, gF, gA, gE, gAP, gAPres5, gAPres10, gAPres20, gAPres50, gnDCG, gnDCG5, gnDCG10, gnDCG20, gnDCG50])) + "\n")
    file.write("MRR:" + str(MRR))
    file.close()
    print ("Results in " + resfile)

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()