import sys
import re
import os
import re
import string
import copy
import math
from itertools import groupby
from operator import itemgetter
from stemmer import PorterStemmer
from preprocess import removeSGML,tokenizeText,removeStopwords,stemWords,removePunks

class ourSentence:
    def __init__(self, sentence, listOfTerms):
        self.sentence = sentence
        self.listOfTerms = listOfTerms
    sentence=""         #theSentence   
    listOfTerms=[]     #list of terms in document
    score = 0           #score
    #newSentence = ourSentence(sentenceString, ["hello", "world"]])
    #listOfSentences=[]
    #
    #listOfSentences[6].score = score


def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key.name) ] 
    return sorted(l, key = alphanum_key)

def isDelineator(words):
    if(words == "." or words == "!" or words == "?" or words == "\n"):
        return True
    else:
        return False

def splitIntoSentences(file):
    inQuote = False
    sentences = []
    beginning=0
    tokenized = tokenizeText(file)
    sentence = ""
    for token in tokenized:
        if(isAPunk(token)):
            sentence+=token
        else:
            sentence+=" "+token

        if(token=="\"" and not inQuote):
            inQuote=True
        elif(token=="\"" and inQuote):
            inQuote=False #
        if(isDelineator(token) and not inQuote):
            if(file[beginning:index+1]!="\n\n" and file[beginning:index+1]!="\n"):
                sentences.append(sentence)
                print(sentence)
                sentence = ""
    '''
    for index, words in enumerate(file):
        if(words == "\"" and not inQuote):
            inQuote = True
        elif(words == "\"" and inQuote):
            inQuote = False #
        if(isDelineator(words) and not inQuote):
            if(file[beginning:index+1] != "\n\n" and file[beginning:index+1]!= "\n"):
                sentences.append(file[beginning:index+1].replace("\n", ""))
                beginning=index+1
    '''
            
    return sentences

# createSentenceObjects - Attach a set of terms to each sentence.
# Input:  list of sentences as strings
# Output: list of ourSentence objects
def createSentenceObjects(sentences):
    sentenceObjects = []
    # get stopwords
    s = open("stopwords", "r")
    stopwords = s.read().split()
    # iterate through the list of sentences
    for sentence in sentences:
        # Tokenize sentence
        tokens = tokenizeText(sentence)
        # Remove stopwords from sentence tokens
        tokens = removeStopwords(tokens, stopwords)
        # Stem the tokens of the sentence
        stemmed = stemWords(tokens)
        # Create ourSentence object and append to list of ourSentence objects
        sentenceObjects.append(ourSentence(sentence, stemmed))
    # Return the list of ourSentence objects
    return sentenceObjects


#input dictionary of term frequencies
#output dictionary of term scores
def getScoreDictionary(termFrequencies):
    termFrequencyTuples=[]
    termScoreDict={}
    #turn dictionary into list of tuples and sort from most to least common
    for words in termFrequencies:
        termFrequencyTuples.append((words,termFrequencies[words]))
    termFrequencyTuples.sort(key=lambda tup: tup[1],reverse=True)
    print(termFrequencyTuples)

    #Translate frequency into rank
    rank = 1
    frequency = -1
    for index, tuples in enumerate(termFrequencyTuples):
        #If this is the first term in the list, make its rank 1 and set the starting max frequency
        if(frequency==-1):
            frequency = tuples[1]
            termFrequencyTuples[index] = (termFrequencyTuples[index][0], rank)
            #If we encounter a new freqeuncy, increment the rank and make that the rank of this term
        elif(tuples[1]!=frequency):
            frequency = tuples[1]
            rank += 1
            termFrequencyTuples[index] = (termFrequencyTuples[index][0], rank)
            #if we don't encounter a new rank, this term has the same rank as the previous example
        elif(tuples[1]==frequency):
            termFrequencyTuples[index] = (termFrequencyTuples[index][0], rank)

    #print ranks for resting purposes
    print(termFrequencyTuples)

    #get maxRank
    maxRank=termFrequencyTuples[-1][1]
    print(maxRank)  

    #Convert ranks into scores and place it into a dictionary
    for index, tuples in enumerate(termFrequencyTuples):
        termScoreDict[termFrequencyTuples[index][0]]= maxRank - termFrequencyTuples[index][1] + 1

    #return the dictionary
    return termScoreDict

def getTermFreqs(sentenceObjList): #Erin's function :)
    word_freqs = {}
    for sentence in sentenceObjList:
        for word in sentence.listOfTerms
            if word in word_freqs:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1
    return word_freqs


'''
Attach to each sentence the sum of their words’ points, divided by the length of the sentence (Lauren) 
Loop through the sentences and loop through the words in the sentence and add up all the scores of the words from the dictionary. 
Divide by length of sentence to normalize
'''
#Lauren's Function
getSentences(listOfSentenceObjects,termScores): 
    OurSentence = {}
    wordSum = 0.0

    for sentence in listOfSentenceObjects:
        for word in sentence:
            wordSum += termScores[word]
        OurSentence[sentence] = float(wordSum/float(len(sentence)))

    return OurSentence

'''
file = "string"
listOfSentences = splitIntoSentences(file)

listOfSentenceObjects=DominicFunction(listOfSentences) #return List of OurSentence
termFrequency=ErinFunction(listOfSentenceObjects) #term dictionary term:frequency
termScores=SamFunction(termFrequency)               #term dictionary term:score
listOfSentenceObjects=LaurenFunction(listOfSentenceObjects,termScores)  #List of OurSentence, with scores filled in 
sort(listOfSentenceObjects)
'''

print("\n")
#sys.argv[1]
with os.scandir(sys.argv[1]) as entries:
    entries=natural_sort(entries)
    for index,entry in enumerate(entries):
        f = open(entry, "r")
        a=f.read()
        sentences = splitIntoSentences(a)
        print(sentences)
        for sentence in sentences:
            print(sentence)
            print("split")
        #for elements in re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',a):
        #    print(elements)
        #    print("split")

