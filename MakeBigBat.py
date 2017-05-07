import os
from multiprocessing import Process

machineDirectory = "D:\\BANKI_QA\\W2V-i\\W2V-allfiles\\alltxt\\"
dirres = "D:\\BANKI_QA\\W2Vo\\Vectors\\"

def chunks(lst, chunk_size):
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

def driver(ite, list):
    bat = open("make_vectors_from_docs" + str(ite) + ".bat", "w")
    for i in list:
        # print(i)
        bat.writelines("C:\\Users\\sirne\\Anaconda2\\python.exe D:\\BANKI_QA\\W2Vo\\use_model.py D:\\BANKI_QA\\W2Vo\\" + \
                       "NormalizedDocs\\" + i + " D:\\BANKI_QA\\W2Vo\\" + "Vectors\\" + i + "\n")
        #
        # if it < 8:
        #     bat.writelines("start \"\" C:\\Users\\sirne\\Anaconda2\\python.exe D:\\BANKI_QA\\W2Vo\\use_model.py D:\\BANKI_QA\\W2Vo\\" + \
        #                "NormalizedDocs\\" + i + " D:\\BANKI_QA\\W2Vo\\" + "Vectors\\" + i + "\n")
        #     it += 1
        # else:
        #     bat.writelines("C:\\Users\\sirne\\Anaconda2\\python.exe D:\\BANKI_QA\\W2Vo\\use_model.py D:\\BANKI_QA\\W2Vo\\" + \
        #                "NormalizedDocs\\" + i + " D:\\BANKI_QA\\W2Vo\\" + "Vectors\\" + i + "\n")
        #     it = 0
    bat.writelines("\npause 1")
    bat.close

def main():
    files = list(filter(lambda x: ('hdr' in x), os.listdir(machineDirectory)))
    a = set(files)
    files2 = list(filter(lambda x: ('hdr' in x), os.listdir(dirres)))
    b = set (files2)
    a = a.difference(b)
    l = []
    for i in a:
        l.append(i)
    a = chunks(l, (len(l) // 6) + 1)
    it = 2
    for i in a:
        Process(target=driver, args=(it, i)).start()
        it += 1


if __name__ == '__main__':
    main()