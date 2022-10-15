import random

ans_candidate = []
words_list = []

CONF = -1
EXIST = -2
NO_EXIST = -3
NO_INFO = -4

WORD_LENGTH = 5
ANSWER_WORD = "green"

def load_words():
    global words_list
    global ans_candidate
    with open("./wordlist_all","r") as wd:
        while True:
            word = wd.readline().rstrip("\n")
            if len(word) == 0:
                break
            words_list.append(word)
    with open("./wordlist_hidden","r") as wd:
        while True:
            word = wd.readline().rstrip("\n")
            if len(word) == 0:
                break
            ans_candidate.append(word)


def init():
    load_words()
    ANSWER_WORD = "wrist"

def wordle(submit_word):
    res = {}
    st = ""
    for i in range(WORD_LENGTH):
        if ANSWER_WORD[i] == submit_word[i]:
            res.update({i:CONF})
            st = st + "2"
        elif submit_word[i] in ANSWER_WORD:
            res.update({i:EXIST})
            st = st + "1"
        else:
            st = st + "0"
            res.update({i:NO_EXIST})    
    return st

def isexistwords(st):
    return st in words_list


def quest():
    global ANSWER_WORD
    init()
    ANSWER_WORD = ans_candidate[random.randrange(0,len(ans_candidate))]
    COUNT = 0
    while True:
        COUNT = COUNT + 1
        while True:
            print(str(COUNT)+" try input :")
            submit_word = input()
            if isexistwords(submit_word):
                break
            print("non exist word : ")
        result = wordle(submit_word)
        print(result)
        is_end = submit_word == ANSWER_WORD
        if(is_end == True):
            print("== Success!! ==")
            print("Answer : "+submit_word + " "+"Try Count : "+str(COUNT))
            print("===============")
            return COUNT
quest()
