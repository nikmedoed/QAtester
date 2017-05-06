import os
import zipfile
import pickle
import re

machineDirectory = "D:\\BANKI_QA\\Orignals\\"
resdir = "D:\\BANKI_QA\\W2V-allconcat-filt\\alltxt\\"

def main():
    files = list(filter(lambda x: ('hdr' in x), os.listdir(machineDirectory)))
    nfile = open("alltxt.txt", "w")
    n = 0
    c = 0
    for i in files:
        try:
            f = open(machineDirectory + i, "r")
            # nfile = open(resdir + i, "w")
            for t in range(17):
                text = f.readline()
            # text = text.decode("cp1251")
            nfile.write(re.sub("<NOMORPH><FONT=\"GREY\">Answer: .*", "", re.sub("MRM_snippet = Question: ", "", text)) + "\n")
            nfile.write(re.sub(".*<NOMORPH><FONT=\"GREY\">Answer: ", "", text.replace("</FONT></NOMORPH>", "")) + "\n\n")
            c += 2
            if c >= 50000:
                nfile.close()
                n += 1
                nfile = open("alltxt" + str(n) + ".txt", "w")
                c = 0
            # nfile.close()
            f.close()
            # print (i, "Ok")
        except Exception:
            print(i, "skipped")

    nfile.close()
#
if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()
