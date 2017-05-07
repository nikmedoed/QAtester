import os
import pickle
import re


def main():
    files = list(filter(lambda x: ('hdr' in x), os.listdir(machineDirectory)))
    base ={}

    nfile = open ("base.txt","w")
    for i in files:
        z = zipfile.ZipFile(machineDirectory+i)
        for fil in z.namelist():
            file = z.open(fil,"r")
            id = (file.readline()).decode("cp1251").strip().replace("MRM_id = ", "")
            realid =  re.sub("MRM_.*_id = ", "", (file.readline()).decode("cp1251").strip())
            base.update({id: realid})
            nfile.write(str(id)+"\t"+str(realid)+"\n")
        z.close()
    bfile = open("base", "wb")
    pickle.dump(base,bfile)
    bfile.close()
    nfile.close()

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()