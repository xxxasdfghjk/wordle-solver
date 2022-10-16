import copy
from WordleStatus import CharStatus


class WordleSolver:

    answerCandidate = []
    wordsList = []
    WORD_LENGTH = 5
    ALPHABET = [chr(i) for i in range(ord('a'), ord('z')+1)]
    expectedInfoAms = [{} for i in range(WORD_LENGTH)]

    def __init__(self, allWordsFilePath, hiddenWordsFilePath, wordLength):
        self.WORD_LENGTH = wordLength
        with open(allWordsFilePath, "r") as wd:
            while True:
                word = wd.readline().rstrip("\n")
                if len(word) == 0:
                    break
                self.wordsList.append(word)
        with open(hiddenWordsFilePath, "r") as wd:
            while True:
                word = wd.readline().rstrip("\n")
                if len(word) == 0:
                    break
                self.answerCandidate.append(word)

    def outputResult(self, submitWord, answerWord):
        res = {}
        word = ""
        for i in range(self.WORD_LENGTH):
            if answerWord[i] == submitWord[i]:
                word = word + "2"
                res.update({i: CharStatus.CONF})
            elif submitWord[i] in answerWord:
                word = word + "1"
                res.update({i: CharStatus.EXIST})
            else:
                word = word + "0"
                res.update({i: CharStatus.NO_EXIST})
        return res, word

    def isExistsWord(self, word):
        return word in self.wordsList

    def quest(self, answerWord):
        if not answerWord in self.answerCandidate:
            raise Exception()
        count = 0
        while True:
            count = count + 1
            while True:
                print(str(count)+" try input :")
                submitWord = input()
                if self.isExistsWord(submitWord):
                    break
                print("non exist word : ")
            _, st = self.outputResult(submitWord, answerWord)
            isEnd = submitWord == answerWord
            if (isEnd == True):
                print("== Success!! ==")
                print("Answer : "+submitWord + " "+"Try Count : "+str(count))
                print("===============")
                return count
            print(st)

    def excludeWordsFromCharExist(self, wordList, char, pos=-1):
        if (pos != -1):
            return list(filter(lambda word: not char == word[pos], wordList))
        else:
            return list(filter(lambda word: not char in word, wordList))

    def excludeWordsFromCharNotExist(self, wordList, char, pos=-1):
        if (pos != -1):
            return list(filter(lambda word: char == word[pos], wordList))
        else:
            return list(filter(lambda word: char in word, wordList))

    def wordle(self, submitWord, answerWord):
        res = {}
        for i in range(self.WORD_LENGTH):
            if submitWord[i] == answerWord[i]:
                res.update({i: CharStatus.CONF})
            elif submitWord[i] in answerWord:
                res.update({i: CharStatus.EXIST})
            else:
                res.update({i: CharStatus.NO_EXIST})
        return res

    def updateStatus(self, result, state, submitWord, ansCandidate, answerWord):
        if (answerWord == submitWord):
            return (True, ansCandidate, state)
        for i in range(self.WORD_LENGTH):
            if (result[i] == CharStatus.NO_EXIST):
                for k in range(self.WORD_LENGTH):
                    state[k][submitWord[i]] = CharStatus.NO_EXIST
                    ansCandidate = self.excludeWordsFromCharExist(
                        ansCandidate, submitWord[i])
            elif (result[i] == CharStatus.CONF):
                state[i][submitWord[i]] = CharStatus.CONF
                ansCandidate = self.excludeWordsFromCharNotExist(
                    ansCandidate, submitWord[i], i)
            else:
                for k in range(self.WORD_LENGTH):
                    if (k == i):
                        state[k][submitWord[i]] = CharStatus.NO_EXIST
                        ansCandidate = self.excludeWordsFromCharExist(
                            ansCandidate, submitWord[i], i)
                    elif (state[k][submitWord[i]] == CharStatus.NO_INFO):
                        state[k][submitWord[i]] = CharStatus.EXIST
                ansCandidate = self.excludeWordsFromCharNotExist(
                    ansCandidate, submitWord[i])
        return (False, ansCandidate, state)

    def chooseWord(self, expectedInfoAms, ansCandidate, wordsList, state):
        if (len(ansCandidate) == 1):
            return ansCandidate[0]
        resWords = ""
        resPoints = -1
        for i in wordsList:
            index = 0
            points = 0
            used = ""
            for j in i:
                if not j in used:
                    points = points + expectedInfoAms[index][j]
                    if (state[index][j] != CharStatus.NO_EXIST):
                        used = used + j
                index = index + 1
            if (resPoints < points):
                resPoints = points
                resWords = i
        return resWords

    def countWordExistChar(self, ansCandidate, char):
        count = 0
        for i in ansCandidate:
            if (char in i):
                count = count + 1
        return count

    def countWordHasPosChar(self, ansCandidate, char, pos):
        count = 0
        for i in ansCandidate:
            if (i[pos] == char):
                count = count + 1
        return count

    def calcCosineSimilarity(self, lis):
        length = len(lis)
        sum = 0
        for i in lis:
            sum = sum + i
        norm = 0
        for i in lis:
            norm = norm + i*i
        norm = (norm * length) ** (0.5)
        return sum/norm

    def calculateAmsBenefit(self, state, index, char, ansCandidate):
        NO_EXIST_VALUE = 0
        CONF_VALUE = 0.00000001
        if (state[index][char] == CharStatus.NO_EXIST):
            return NO_EXIST_VALUE
        elif (state[index][char] == CharStatus.NO_INFO):
            wordHasChar = self.countWordExistChar(ansCandidate, char)
            wordHasPosChar = self.countWordHasPosChar(
                ansCandidate, char, index)
            wordHasNoChar = len(ansCandidate) - wordHasChar
            if (wordHasChar == 0):
                return 0
            ruijido = self.calcCosineSimilarity(
                [wordHasPosChar, wordHasChar, wordHasNoChar])
            return ruijido
        elif (state[index][char] == CharStatus.CONF):
            return CONF_VALUE
        elif (state[index][char] == CharStatus.EXIST):
            wordHasChar = len(ansCandidate)
            wordHasPosChar = self.countWordHasPosChar(
                ansCandidate, char, index)
            if (wordHasChar == 0 or wordHasPosChar == 0):
                return 0
            ruijido = self.calcCosineSimilarity(
                [wordHasChar/2.0, wordHasPosChar])
            return ruijido

    def solver(self, answerWord, printLog=True):
        currentAnswerCandidate = copy.deepcopy(self.answerCandidate)
        submitted = []
        expectedInfoAms = [{} for i in range(self.WORD_LENGTH)]
        state = [{} for i in range(self.WORD_LENGTH)]
        for j in range(self.WORD_LENGTH):
            for i in self.ALPHABET:
                state[j].update({i: CharStatus.NO_INFO})
        for j in range(self.WORD_LENGTH):
            for i in self.ALPHABET:
                expectedInfoAms[j].update({i: CharStatus.NO_INFO})
        while True:
            for i in range(self.WORD_LENGTH):
                for j in self.ALPHABET:
                    expectedInfoAms[i][j] = self.calculateAmsBenefit(
                        state, i, j, currentAnswerCandidate)
            submitWord = self.chooseWord(
                expectedInfoAms, currentAnswerCandidate, self.wordsList, state)
            submitted.append(submitWord)
            result = self.wordle(submitWord, answerWord)
            isEnd, currentAnswerCandidate, state = self.updateStatus(
                result, state, submitWord, currentAnswerCandidate, answerWord)
            if (isEnd == True):
                if (printLog):
                    print("== Success!! ==")
                    print("Answer : "+submitWord + " " +
                          "Try Count : "+str(len(submitted)))
                    print("===============")
                return submitted

    def allTest(self, isFileOutput=False, printLog=False,):
        test = self.answerCandidate
        for i in test:
            tryWords = self.solver(i, printLog=False)
            print(','.join(tryWords))

    def isFormatted(self, st):
        for i in st:
            if i not in "012":
                return False
        return len(st) == self.WORD_LENGTH

    def wordleInput(self):
        res = {}
        print("Input wordle result 5 digits (black : 0 , yellow : 1 , green : 2)  : ")
        while True:
            st = input()
            if (self.isFormatted(st)):
                break
            else:
                print("not formatted , please retype : ")
                continue

        for i in range(self.WORD_LENGTH):
            if st[i] == "2":
                res.update({i: CharStatus.CONF})
            elif st[i] == "1":
                res.update({i: CharStatus.EXIST})
            else:
                res.update({i: CharStatus.NO_EXIST})
        return res

    def talk(self, deb=0):
        currentAnswerCandidate = copy.deepcopy(self.answerCandidate)
        COUNT = 0
        expectedInfoAms = [{} for i in range(self.WORD_LENGTH)]
        state = [{} for i in range(self.WORD_LENGTH)]
        for j in range(self.WORD_LENGTH):
            for i in self.ALPHABET:
                state[j].update({i: CharStatus.NO_INFO})
        for j in range(self.WORD_LENGTH):
            for i in self.ALPHABET:
                expectedInfoAms[j].update({i: CharStatus.NO_INFO})
        while True:
            COUNT = COUNT + 1
            for i in range(self.WORD_LENGTH):
                for j in self.ALPHABET:
                    expectedInfoAms[i][j] = self.calculateAmsBenefit(
                        state, i, j, currentAnswerCandidate)
            submitWord = self.chooseWord(
                expectedInfoAms, currentAnswerCandidate, self.wordsList, state)
            print("please submit this word : " + submitWord)
            result = self.wordleInput()
            isEnd, currentAnswerCandidate, state = self.updateStatus(
                result, state, submitWord, currentAnswerCandidate, "!!!!!!!!!")
            if (len(currentAnswerCandidate) == 0):
                print("NO ANSWER EXISTS")
            if (isEnd == True):
                print("== Success!! ==")
                print("Answer : "+submitWord + " "+"Try Count : "+str(COUNT))
                print("===============")
                return COUNT
