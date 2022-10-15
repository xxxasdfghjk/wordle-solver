import copy

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
    return False

def choose_word(expected_info_ams):
    if(len(ans_candidate) == 1):
        return ans_candidate[0]
    res_words = ""
    res_points = 0
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
        """
        for k in range(0,len(used)):
            for l in range(k+1,len(used)):
                x_and_y = count_word_exist_str(ans_candidate,used[k]+used[l])
                x = count_word_exist_str(ans_candidate,used[k])
                y = count_word_exist_str(ans_candidate,used[l])
                x_or_y = x+y-x_and_y
                not_x_not_y = len(ans_candidate) - x_or_y
                not_x_y = y - x_and_y
                x_not_y = x - x_and_y
                norm = ((x_not_y*x_not_y + not_x_y*not_x_y + x_and_y*x_and_y + not_x_not_y*not_x_not_y) ** (0.5))*(2)

                res_points = res_points + cos_ruijido([x_not_y,not_x_y,x_and_y,not_x_not_y])/10
        """

        if(res_points <= points):
            res_points = points
            res_words = i
    return res_words
            


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
    CONF_VALUE = 0
    if(state[index][char] == NO_EXIST):
        return NO_EXIST_VALUE
    elif(state[index][char] == NO_INFO):
        word_has_char = count_word_exist_char(ans_candidate,char)
        word_has_pos_char = count_word_has_pos_char(ans_candidate,char,index)
        word_has_no_char = len(ans_candidate) - word_has_char
        if(word_has_no_char == 0 or word_has_no_char == 0):
            return 0
        ruijido = cos_ruijido([word_has_char,word_has_no_char])
        return ruijido*ruijido
        #return word_has_char+word_has_no_char/((2*(word_has_char*word_has_char+word_has_no_char+word_has_no_char))**(1/2))+(word_has_pos_char/(len(ans_candidate)*5))
    elif(state[index][char] == CONF):
        return CONF_VALUE
    elif(state[index][char] == EXIST):
        word_has_char = len(ans_candidate)/2
        word_has_pos_char = count_word_has_pos_char(ans_candidate,char,index)
        if(word_has_char == 0 or word_has_pos_char == 0):
            return 0
        ruijido = cos_ruijido([word_has_char,word_has_pos_char])
        return ruijido*ruijido
        #((word_has_char+word_has_pos_char)/((2*(word_has_char*word_has_char+word_has_pos_char*word_has_pos_char)**(0.5))))/4

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
        if(len(ans_candidate) < 11 and deb==1):
            print(ans_candidate)
            print(state)
        is_end = update_state(result,state,submit_word)
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


#killer_case = ['amber', 'avert', 'break', 'breed', 'caper', 'catch', 'creak', 'cruel', 'daunt', 'eaten', 'freak', 'gaunt', 'hatch', 'hound', 'hyper', 'jaunt', 'might', 'paper', 'pound', 'stead', 'under', 'vaunt', 'wider', 'wight']
#iller_case = ['daunt', 'freak', 'gamer', 'gaunt', 'gazer', 'happy', 'hatch', 'haunt', 'impel', 'jaunt', 'maker', 'paint', 'taker', 'vaunt', 'wafer', 'wager']
killer_case = ['amber', 'avert', 'blush', 'breed', 'caper', 'catch', 'daunt', 'freak', 'gaunt', 'hatch', 'hound', 'hyper', 'jaunt', 'mover', 'paper', 'plush', 'taker', 'under', 'vaunt', 'wider', 'wight']
for i in killer_case:
    solver(i,1)
