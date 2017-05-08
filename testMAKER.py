from tester import *
from Duplicates import baseread


def maketest(quer, softOr, stop, base):
    res = req(quer, softOr, "True" in stop)
    startlen = len(res)
    result = IdToGroupid(res, base)["all"]
    file = open(testfldr + "test-size=" + str(startlen) + "-normsize=" + str(len(result)) + " - " + str(len(quer)) +
                "-softOR=" + str(softOr) + "-filt=" + \
                stop.replace("\n", "") + " " + quer[0:20] + ".txt", "w")
    file.write(quer + "\n")
    file.write(softOr + "\n")
    file.write(stop + "\n")
    # print (test)
    print("Запрос: ", quer)
    print()
    it = 0
    tofile = []
    tempfile = open("temp\\temp-" + str(startlen) + " - " + str(len(result)) + " - " +
                     str(datetime.datetime.now()).replace(":", "-") + ".txt", "w")
    while it < len(result):
        e = result[it]
        c = input("\n\nЗапрос: \t" + quer + " (необходимо определить, отвечает ли на него пара вопрос-ответ)\nВопрос: \t" + e['q'] + "\n" + "Ответ: \t" + e['a'] + "\n\n" + "(" + \
                  str(result.index(e)+1) + "/" + str(len(result)) + ")" + " Это подходит? (y/n/b): ")
        tempfile.write(str(it) + "\t" + str(e['groupid']) + "\t" + str(c) + "\n")
        if "set" in c:
            s = c.split(" ")[1:]
            for iter in s:
                ite = int(iter)
                k = result[ite]
                tofile.append(str(k['groupid']))
                it = ite + 1
        else:
            if "goto" in c:
                it = int(c.split(" ")[1])
            else:
                if c == "b":
                    it -= 1
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
    tempfile.close()
    file.write("\n".join(tofile))
    file.close()


def main():
    tests = open("tests.txt", "r", encoding="cp1251")
    base = baseread()
    start = 1
    iter = 0
    for line in tests.readlines():
        iter += 1
        if iter >= start:
            print("test:\n" + line + "\n\n")
            line = line.split("\t")
            maketest(line[0], line[1], line[2], base)

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()
