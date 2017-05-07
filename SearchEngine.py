import http.client
import urllib.parse
import json
import pickle

serva = "localhost:2085"
format = "json"

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