import pickle
import os
import datetime

testdir = "tests\\"

def maketest(testdata):
    bfile = open(testdir + testdata, "rb")
    testset = pickle.load(bfile)
    bfile.close()
    quer = testset['quer']
    softOr = testset['soft']
    stop = testset['stop']
    result = testset['res']
    # print (test)
    print("Запрос: ", quer)
    print()

    it = 0
    tofile = []
    tempname = "temp\\temp-" + str(len(result)) + " - " + \
               str(datetime.datetime.now()).replace(":", "-") + ".txt"
    tempfile = open(tempname, "w")
    tempfile.close()

    while it < len(result):
        e = result[it]
        c = input("\n\nЗапрос: \t" + quer + " (необходимо определить, отвечает ли на него пара вопрос-ответ)\nВопрос: \t" + e['q'] + "\n" + "Ответ: \t" + e['a'] + "\n\n" + "(" + \
                  str(result.index(e)+1) + "/" + str(len(result)) + ")" + " Это подходит? (y/n/b): ")
        tempfile = open(tempname, "a")
        tempfile.write(str(it + 1) + "\t" + str(e['groupid']) + "\t" + str(c) + "\n")
        tempfile.close()
        if "set" in c:
            s = c.split(" ")[1:]
            for iter in s:
                ite = int(iter)
                k = result[ite - 1]
                tofile.append(str(k['groupid']))
                it = ite
        else:
            if "goto" in c:
                it = int(c.split(" ")[1])-1
            else:
                if c == "b":
                    it -= 1
                    if len(tofile) > 0:
                        tofile.pop()
                else:
                    if c == 'y':
                        tofile.append(str(e['groupid']))
                        print("\t\tДобавлено")
                    else:
                        if c == "break":
                            break
                        print("\t\tОтклонено")
                    it += 1
    file = open(testdir + testdata.replace("testdata", "txt"), "w")
    file.write(quer + "\n")
    file.write(softOr + "\n")
    file.write(stop + "\n\n")
    file.write("\n".join(tofile))
    file.close()


def main():
    tests = list(filter(lambda x: ('.testdata' in x), os.listdir(testdir)))
    # base = baseread()
    for line in tests:
        print("test:\n" + line)
        c = input("C этим тестом работаем? (y/n): ")
        if c == "y":
            maketest(line) #, base)
            os.remove(testdir + line)
        print("\n\n")

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()
