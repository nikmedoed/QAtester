from tester import *
from Duplicates import baseread


def maketest(quer, softOr, stop, base):
    res = req(quer, softOr, "True" in stop)
    file = open(testfldr + "test-" + str(len(quer)) + "-softOR=" + str(softOr) + "-filt=" + \
                stop.replace("\n", "") + " " + quer[0:20] + ".txt", "w")
    file.write(quer + "\n")
    file.write(softOr + "\n")
    file.write(stop + "\n")
    # print (test)
    result = IdToGroupid(res, base)["all"]
    print("Запрос: ", quer)
    print()
    it = 0
    tofile = []
    while it != len(result):
        e = result[it]
        c = input("Запрос: " + quer + "\nВопрос: " + e['q'] + "\n" + "Ответ: " + e['a'] + "\n\n" + "(" + \
                  str(result.index(e)+1) + "/" + str(len(result)) + ")" + " Это подходит? (y/n/b): ")
        if c == "b":
            it -= 1
            tofile.pop()
        else:
            if c == 'y':
                tofile.append(e['groupid'])
                print("Добавлено")
            it += 1
    file.write("\n".join(e['groupid']))
    file.close()


def main():
    tests = open("tests.txt", "r", encoding="cp1251")
    base = baseread()
    start = 0
    iter = 0
    for line in tests.readlines():
        iter += 1
        if iter >= start:
            line = line.split("\t")
            maketest(line[0], line[1], line[2], base)

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()
