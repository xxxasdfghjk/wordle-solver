import copy
import bisect

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
state = [{} for i in range(WORD_LENGTH)]
ANSWER_WORD = "green"
expected_info_ams = [{} for i in range(WORD_LENGTH)]
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
    for j in range(WORD_LENGTH):
        for i in ALPHABET:
            state[j].update({i:NO_INFO})
    for j in range(WORD_LENGTH):
        for i in ALPHABET:
            expected_info_ams[j].update({i:NO_INFO})
    load_words()
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

def update_state(result,state,submit_word):
    global ans_candidate
    if(ANSWER_WORD == submit_word):
        return True
    for i in range(WORD_LENGTH):
        if(result[i] == NO_EXIST):
            for k in range(WORD_LENGTH):
                state[k][submit_word[i]] = NO_EXIST
                ans_candidate = exclude_words_from_char_exist(ans_candidate, submit_word[i])
        elif(result[i] == CONF):
            state[i][submit_word[i]] = CONF
            ans_candidate = exclude_words_from_char_not_exist(ans_candidate, submit_word[i],i)
        else:
            for k in range(WORD_LENGTH):
                if(k == i):
                    state[k][submit_word[i]] = NO_EXIST
                    ans_candidate = exclude_words_from_char_exist(ans_candidate, submit_word[i],i)
                elif(state[k][submit_word[i]] == NO_INFO):
                    state[k][submit_word[i]] = EXIST
            ans_candidate = exclude_words_from_char_not_exist(ans_candidate, submit_word[i])
    return False

def choose_word(expected_info_ams):
    if(len(ans_candidate) == 1):
        return ans_candidate[0]
    res_words = ""
    res_points = -1
    ranking_num = 10
    ranking = [500 for i in range(ranking_num)]
    ranking_words = ["" for i in range(ranking_num)]
    candi = []
    for i in words_list:
        index = 0
        points = 0
        used = ""
        for j in i:
            if not j in used:
                points = points + expected_info_ams[index][j]
                if(state[index][j] != NO_EXIST):
                    used = used + j
            index = index + 1
        ind = bisect.bisect(ranking,-points)
        if(ind < ranking_num):
            ranking[ind] = -points
            ranking_words[ind] = i
        if(res_points < points):
            res_points = points
            res_words = i
            candi = [res_words]
        elif(points != 0 and res_points == points):
            candi.append(i)
    if(len(candi) > 1):
        ind = exists_list(ans_candidate,candi)
        if(ind != -1):
            return ans_candidate[ind]
        else:
            return candi[0]
    return res_words
            
def exists_list(origin_list,target_list):
    ind = 0
    for i in origin_list:
        for j in target_list:
            if(i == j):
                return ind
        ind = ind+1
    return -1



def count_word_exist_char(ans_candidate,char):
    count = 0
    for i in ans_candidate:
        if(char in i):
            count = count + 1
    return count

def count_word_exist_str(ans_candidate,st):
    count = 0
    l = len(st)
    for i in ans_candidate:
        cnt = 0
        for t in st:
            if not t in i:
                break
            cnt = cnt + 1
            if cnt == l:
                count = count + 1
                break
    return count

def count_word_has_pos_char(ans_candidate,char,pos):
    count = 0
    for i in ans_candidate:
        if(i[pos] == char):
            count = count + 1
    return count

def cos_ruijido(lis):
    length = len(lis)
    sum = 0
    for i in lis:
        sum = sum + i
    norm = 0
    for i in lis:
        norm = norm + i*i
    norm = (norm *length )** (0.5)
    return sum/norm

def calculate_ams_benefit(state,index,char):
    NO_EXIST_VALUE = 0
    CONF_VALUE = 0.00000001
    if(state[index][char] == NO_EXIST):
        return NO_EXIST_VALUE
    elif(state[index][char] == NO_INFO):
        word_has_char = count_word_exist_char(ans_candidate,char)
        word_has_pos_char = count_word_has_pos_char(ans_candidate,char,index)
        word_has_no_char = len(ans_candidate) - word_has_char
        if(word_has_char == 0):
            return 0
        ruijido = cos_ruijido([word_has_pos_char,word_has_char,word_has_no_char])
        return ruijido
    elif(state[index][char] == CONF):
        return CONF_VALUE
    elif(state[index][char] == EXIST):
        word_has_char = len(ans_candidate)
        word_has_pos_char = count_word_has_pos_char(ans_candidate,char,index)
        if(word_has_char == 0 or word_has_pos_char == 0):
            return 0
        ruijido = cos_ruijido([word_has_char/2.0,word_has_pos_char])
        return ruijido

def solver(word,deb=0):
    global ANSWER_WORD
    ANSWER_WORD= word
    init()
    global expected_info_ams
    COUNT = 0
    while True:
        COUNT = COUNT + 1
        if(COUNT == 100):
            return 100
        for i in range(WORD_LENGTH):
            for j in ALPHABET:
                expected_info_ams[i][j] = calculate_ams_benefit(state,i,j)
        submit_word = choose_word(expected_info_ams)
        result = wordle(submit_word)
        print(submit_word,len(ans_candidate))
        is_end = update_state(result,state,submit_word)
        if(len(ans_candidate) < 11 and deb==1):
            if(is_end == True):
                print([submit_word])
            else:
                print(ans_candidate)
        if(is_end == True):
            print("== Success!! ==")
            print("Answer : "+submit_word + " "+"Try Count : "+str(COUNT))
            print("===============")
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

all_test()