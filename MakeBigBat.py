import os

machineDirectory = "D:\\BANKI_QA\\W2V-i\\W2V-allfiles\\alltxt\\"

def main():
    files = list(filter(lambda x: ('hdr' in x), os.listdir(machineDirectory)))
    bat = open("make_vectors_from_docs.bat", "w")
    for i in files:
        # print(i)
        bat.writelines("start "" C:\\Users\\sirne\\Anaconda2\\python.exe D:\\BANKI_QA\\W2Vo\\use_model.py D:\\BANKI_QA\\W2Vo\\" + \
                       "NormalizedDocs\\" + i + " D:\\BANKI_QA\\W2Vo\\" + "Vectors\\" + i + "\n")

    bat.writelines("\npause 1")
    bat.close()

if __name__ == '__main__':
    main()