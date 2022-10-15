import copy
import statistics

def exclude_words_from_char_exist(word_list, char,pos = -1):
    index = pos
    new_list = []
    if(pos != -1):
        for i in word_list:
            if i[index] != char:
                new_list.append(i)
    else:
        for i in word_list:
            if not (char in i):
                new_list.append(i)
    return new_list

def exclude_words_from_char_not_exist(word_list, char,pos = -1):
    index = pos
    new_list = []
    if(pos != -1):
        for i in word_list:
            if i[index] == char:
                new_list.append(i)
    else:
        for i in word_list:
            if (char in i):
                new_list.append(i)
    return new_list

no_use_char =[]
char_status = []
ans_candidate = []
words_list = []

CONF = -1
EXIST = -2
NO_EXIST = -3
NO_INFO = -4

WORD_LENGTH = 5
ALPHABET = [chr(i) for i in range(ord('a'), ord('z')+1)]
word_box = [i for i in range(WORD_LENGTH)]
ANSWER_WORD = "green"
expected_info_ams = {}
WORDS_LIST = []
ANS_CANDIDATE = []
IS_LOADED = 0
def load_words():
    global words_list
    global ans_candidate
    global IS_LOADED
    if(IS_LOADED == 1):
        words_list = copy.copy(WORDS_LIST)
        ans_candidate = copy.copy(ANS_CANDIDATE)
        return

    with open("./wordlist_all","r") as wd:
        while True:
            word = wd.readline().rstrip("\n")
            if len(word) == 0:
                break
            words_list.append(word)
            WORDS_LIST.append(word)
    with open("./wordlist_hidden","r") as wd:
        while True:
            word = wd.readline().rstrip("\n")
            if len(word) == 0:
                break
            ans_candidate.append(word)
            ANS_CANDIDATE.append(word)
    IS_LOADED = 1


def init():
    load_words()    
    for i in ans_candidate:
            expected_info_ams.update({i:0})
    ANSWER_WORD = "wrist"

def wordle(submit_word):
    res = {}
    for i in range(WORD_LENGTH):
        if ANSWER_WORD[i] == submit_word[i]:
            res.update({i:CONF})
        elif submit_word[i] in ANSWER_WORD:
            res.update({i:EXIST})
        else:
            res.update({i:NO_EXIST})
    return res

def update_state(result,submit_word):
    global ans_candidate
    if(ANSWER_WORD == submit_word):
        return True
    for i in range(WORD_LENGTH):
        if(result[i] == NO_EXIST):
            for k in range(WORD_LENGTH):
                ans_candidate = exclude_words_from_char_exist(ans_candidate, submit_word[i])
        elif(result[i] == CONF):
            ans_candidate = exclude_words_from_char_not_exist(ans_candidate, submit_word[i],i)
        else:
            for k in range(WORD_LENGTH):
                    ans_candidate = exclude_words_from_char_exist(ans_candidate, submit_word[i],i)
    return False

def choose_word(expected_info_ams):
    if(len(ans_candidate) == 1):
        return ans_candidate[0]
    res_words = ""
    res_points = 99999999
    for i in words_list:
        points = expected_info_ams[i]
        if(res_points >= points):
            res_points = points
            res_words = i
    return res_words
            


def count_word_exist_char(ans_candidate,char):
    count = 0
    for i in ans_candidate:
        if(char in i):
            count = count + 1
    return count

def count_word_has_pos_char(ans_candidate,char,pos):
    count = 0
    for i in ans_candidate:
        if(i[pos] == char):
            count = count + 1
    return count

def diff_character(original,target):
    st_code = 0
    index = 0
    for i in original:
        
        
        if i in target[index]:
            st_code = st_code * 10 + 0
        else:
            st_code = st_code * 10 + 1
        index = index + 1
    return st_code

def calculate_ams_benefit(choose_word):
    dic = {}
    for candi_word in ans_candidate:
        code = diff_character(choose_word,candi_word)
        dic[code] = dic.get(code,0) + 1
    mi = 999999
    ma = -1
    lis = []
    for k in dic.keys():
        lis.append(dic[k])
        ma = max(dic[k],ma)
        mi = min(dic[k],mi)
    return ma - mi

def solver(word):
    global ANSWER_WORD
    ANSWER_WORD= word
    init()
    global expected_info_ams
    COUNT = 0
    while True:
        COUNT = COUNT + 1
        if(COUNT == 100):
            return 100
        for j in words_list:
            expected_info_ams[j] = calculate_ams_benefit(j)
        submit_word = choose_word(expected_info_ams)
        result = wordle(submit_word)
        print(submit_word,expected_info_ams[j],len(ans_candidate))
        is_end = update_state(result,submit_word)
        if(is_end == True):
            print("== Success!! ==")
            print("Answer : "+submit_word + " "+"Try Count : "+str(COUNT))
            return COUNT

def all_test():
    test = []
    with open("./wordlist_hidden","r") as wd:
        while True:
            word = wd.readline().rstrip("\n")
            if len(word) == 0:
                break
            test.append(word)
    lis = []
    for i in test:
        if (solver(i) > 6):
            lis.append(i)
            print(i)
    print(lis)

#all_test()

#killer_case = ['amber', 'avert', 'break', 'breed', 'caper', 'catch', 'creak', 'cruel', 'daunt', 'eaten', 'freak', 'gaunt', 'hatch', 'hound', 'hyper', 'jaunt', 'might', 'paper', 'pound', 'stead', 'under', 'vaunt', 'wider', 'wight']
#killer_case = ['angel', 'baker', 'bobby', 'booby', 'catch', 'cider', 'croak', 'daunt', 'freak', 'gamer', 'gaunt', 'gazer', 'happy', 'hatch', 'haunt', 'impel', 'jaunt', 'maker', 'paint', 'taker', 'vaunt', 'wafer', 'wager']
killer_case = ['amber', 'avert', 'blush', 'breed', 'caper', 'catch', 'daunt', 'freak', 'gaunt', 'hatch', 'hound', 'hyper', 'jaunt', 'mover', 'paper', 'plush', 'taker', 'under', 'vaunt', 'wider', 'wight']
for i in killer_case:
    solver(i)
