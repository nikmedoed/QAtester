from tester import *
from Duplicates import baseread
import pickle
from multiprocessing import Process


def maketest(quer, softOr, stop, base):
    res = req(quer, softOr, "True" in stop)
    startlen = len(res)
    result = IdToGroupid(res, base)["all"]
    file = open(testfldr + "test-size=" + str(startlen) + "-normsize=" + str(len(result)) + " - " + str(len(quer)) +
                "-softOR=" + str(softOr) + "-filt=" + \
                stop.replace("\n", "") + " " + quer[0:20] + ".testdata", "wb")

    pickle.dump({'quer': quer, 'soft': softOr, 'stop': stop, 'res': result}, file)
    print(file.name + "\n\n")
    file.close()


def main():
    tests = open("tests.txt", "r", encoding="cp1251")
    base = baseread()
    start = 1
    iter = 0
    for line in tests.readlines():
        iter += 1
        if iter >= start:
            print("test:\n" + line)
            line = line.split("\t")
            Process(target=maketest, args=(line[0], line[1], line[2], base)).start()

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()
