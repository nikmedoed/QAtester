from tester import *
from Duplicates import baseread

def maketest(quer, softOr, stop, base ):
    type = 0  # 1,2
    res = req(quer, softOr, "True" in stop)
    # print(res)
    # if len(res) > 50000:
    #     size = 2
    # else:
    #     if len(res) > 5000:
    #         size = 1
    #     else:
    #         size = 0
    test = getQA(res)  # получены в ответ id, тексты вопросов и ответов
    file = open(testfldr + "test-" + str(len(quer)) + "-softOR=" + str(softOr) + "-filt=" + \
                stop.replace("\n", "") + " " + quer[0:20] + ".txt", "w")
    file.write(quer + "\n")
    file.write(softOr + "\n")
    file.write(stop + "\n")
    # print (test)

    real = []
    result=[]
    for i in res:
        for j in base:
            if "0"+i in j['listid']:
                if not(j['groupid'] in real):
                    real.append(j['groupid'])
                    result.append(j)
                break

    print("Запрос: ", quer)
    print()
    it = 0
    tofile=[]
    while it != len(result):
        e = result[it]
        c = input("Запрос: " + quer + "\nВопрос: " + e['q'] + "\n" + "Ответ: " + e['a'] + "\n\n" + "(" + \
                  str(result.index(e)+1) + "/" + str(len(result)) + ")" + " Это подходит? (y/n/b): ")
        if c == "b":
            it -= 1
            tofile.pop
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
