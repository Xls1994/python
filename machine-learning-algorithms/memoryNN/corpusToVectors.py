import numpy as np

def StrToNumpyVector(string):
    return np.asarray([float(elem) for elem in string.split(" ")])

def loadDict(wordVectorFile):
    wordVectors = {}
    with open(wordVectorFile, 'r') as f:
        for line in f:
            cleanLine = line.strip()
            word = cleanLine.split(" ")[0]
            wordVectors[word] = cleanLine[len(word) + 1:]
    return wordVectors
def maxLen(file):
    n = 0
    with open(file, 'r') as f:
        for line in f:
            lineLength = len(line.strip().split(" "))
            if n < lineLength:
                n = lineLength
    return n

def generateInput(wordVectors, corpus, contxtWordsVector, aspectWordsVector, labels, positions, sentLengths, wordDimension):
    aspectTermPlaceHolder= "$T$"
    classNumber = 4
    corpusStream = open(corpus, 'r')
    
    contxtWordsVectorStream = open(contxtWordsVector, 'w')
    aspectWordsVectorStream = open(aspectWordsVector, 'w')
    labelsStream            = open(labels, 'w')
    positionsStream         = open(positions, 'w')
    sentLengths             = open(sentLengths, 'w')

    maxLength = maxLen(corpus)
    n = len(corpusStream.readlines()) / 3
    corpusStream.seek(0)
    for i in range(n):
        sent        = corpusStream.readline().strip()
        aspectTerm  = corpusStream.readline().strip()
        polarity    = int(corpusStream.readline().strip())

        sentVectorStr = ""
        sentWords = sent.split(" ")
        sentenceLength = len(sentWords) - 1
        for word in sentWords:
            if word == aspectTermPlaceHolder:
                continue
            if word in wordVectors:
                sentVectorStr += wordVectors[word] + " "
            else:
                for value in np.random.rand(wordDimension) - 0.5:
                    sentVectorStr += str(value) + " "
        for i in range(sentenceLength,maxLength - 1):
            for value in np.zeros(wordDimension, dtype=float):
                sentVectorStr += str(value) + " "
        
        contxtWordsVectorStream.write(sentVectorStr.strip() + "\n")

        aspectTermWords = aspectTerm.split(" ")
        aspectTermLength = len(aspectTermWords)
        aspectVectorStr = ""
        if aspectTermLength > 1:
            vector = np.zeros(wordDimension)
            for word in aspectTermWords:
                if word in wordVectors:
                    vector += StrToNumpyVector(wordVectors[word])
                else:
                    vector += np.random.rand(wordDimension) - 0.5
            vector = vector / aspectTermLength
            for value in vector:
                aspectVectorStr += str(value) + " "
        else:
            if aspectTerm in wordVectors:
                aspectVectorStr += wordVectors[aspectTerm]
            else:
                for value in np.random.rand(wordDimension) - 0.5:
                    aspectVectorStr += str(value) + " "
        aspectWordsVectorStream.write(aspectVectorStr.strip() + "\n")
        
        oneHot = np.zeros(classNumber, dtype=np.float)
        oneHot[int(polarity)] = 1
        oneHotStr = ""
        for i in oneHot:
            oneHotStr += str(i) + " "
        labelsStream.write(oneHotStr + "\n")

        sentLengths.write(str(len(sent.split(" ")) - 1) + "\n")

        positionsVector = list(np.arange(maxLength) + 1)
        positionsVectorStr = ""
        del positionsVector[sentWords.index(aspectTermPlaceHolder)]
        for position in positionsVector:
            positionsVectorStr += str(position) + " "

        positionsStream.write(positionsVectorStr.strip() + "\n")
        

corpusDir           = '/home/laboratory/memoryCorpus/'
wordVectorDir       = corpusDir + 'en_vectors_50.txt'
corpus              = corpusDir + "laptops_train.xml.seg.addConf"

contxtWordsVector   = corpusDir + 'contxtWords'
aspectWordsVector   = corpusDir + 'aspectWords'
labels              = corpusDir + 'labels'
positions           = corpusDir + 'positions'
sentLengths         = corpusDir + 'sentLengths'
wordDimension       = 50

wordVectors = loadDict(wordVectorDir)
generateInput(wordVectors, corpus, contxtWordsVector, aspectWordsVector, labels, positions, sentLengths, wordDimension)