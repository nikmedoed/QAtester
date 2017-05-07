from tester import *

def main():
    met = 0
    quer = "кредит наличными"
    type = 0 #1,2
    if met == 0:
        res = req(quer)
    else:
        res = GETQuery(quer)
    if len(res)>50000:
        size = 2
    else:
        if len(res)>5000:
            size = 1
        else:
            size = 0
    test = getQA(res) #получены в ответ id, тексты вопросов и ответов
    file = open(testfldr + "test-" + ["small", "norm", "big"][size] + "-" + ["easy", "med", "hard"][type] + "-" + \
                ["text", "query"][met] + " " + quer[0:20] + ".txt", "w")
    file.write(["text", "query"][met] + "\n")
    file.write(quer + "\n\n")
    # print (test)

    result = reverseRepeater(test)
    it = 0
    while it != len(result):
        e = result[it]
        c = input(e['q'] + "\n" + e['a'] + "\n\n" + "(" + str(result.index(e)) + "/" + str(len(result)) + ")" + " Это подходит? (y/n/b): ")
        if c == "b":
            it -= 1
        else:
            if c == 'y':
                for id in e['id']:
                    file.write(id+"\n")
                file.write("\n")
            it += 1

    file.close()

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    main()
