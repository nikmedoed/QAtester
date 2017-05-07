import os
import pickle
import re

machineDirectory = "D:\\BANKI_QA\\Orignals\\"

def readall(dir):
    files = list(filter(lambda x: ('hdr' in x), os.listdir(dir)))
    result = []
    g = 0
    for i in files:
        f = open(machineDirectory + i, "r")
        id = i.replace(".hdr","").replace("qa","")
        for t in range(17):
            text = f.readline()
        # text = text.decode("cp1251")
        q = re.sub("<NOMORPH><FONT=\"GREY\">Answer: .*", "", re.sub("MRM_snippet = Question: ", "", text))
        a = re.sub(".*<NOMORPH><FONT=\"GREY\">Answer: ", "", text.replace("</FONT></NOMORPH>", ""))
        f.close()
        state = False
        for r in result:
            if r['q'] == q and a == r['a']:
                r['listid'].append(id)
                state = True
        if not state:
            result.append({'groupid': g, 'listid': [id], 'q': q, 'a': a})
            g +=1
    return result

def basewrite(place, base):
    bfile = open(place, "wb")
    pickle.dump(base, bfile)
    bfile.close()

def baseread(place = "dupbase"):
    bfile = open(place, "rb")
    base = pickle.load(bfile)
    bfile.close()
    return base

def basewritetxt(place, base):
    bfile = open(place, "w")
    for i in base:
        bfile.write(str(i['groupid']))
        bfile.write('\n')
        bfile.write('\t'.join(i['listid']))
        bfile.write('\n')
        bfile.write(i['q'])
        bfile.write('\n')
        bfile.write(i['a'])
        bfile.write('\n')
        bfile.write('\n')
    bfile.close()

def main():
    # dupbase = readall(machineDirectory)
    dupbase = baseread("dupbase")
    basewritetxt("dupbase.txt", dupbase)


if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()