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

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key.name) ] 
    return sorted(l, key = alphanum_key)
    
def isDelineator(words):
    if(words=="." or words=="!" or words=="?" or words=="\n"):
        return True
    else:
        return False

def isAPunk (word):
    if (word.lower() in string.punctuation) or word.lower()=="”" or word.lower()=="“" or word.lower()=="‘" or word.lower()=="’":
        return True
    else:
        return False

def splitIntoSentences(file):
    inQuote=False
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
        if(words=="\"" and not inQuote):
            inQuote=True
        elif(words=="\"" and inQuote):
            inQuote=False #
        if(isDelineator(words) and not inQuote):
            if(file[beginning:index+1]!="\n\n" and file[beginning:index+1]!="\n"):
                sentences.append(file[beginning:index+1].replace("\n", ""))
                beginning=index+1
    '''
            
    return sentences

preSum=0
recSum=0
averager=0

with os.scandir(sys.argv[1]) as summaries, os.scandir(sys.argv[2]) as ourSummaries:
    summaries=natural_sort(summaries)
    ourSummaries=natural_sort(ourSummaries)
    for index,entry in enumerate(summaries):
        averager+=1
        f = open(entry, "r")
        g = open(ourSummaries[index], "r")
        a=f.read()
        b=g.read()
        relevantSummary=splitIntoSentences(a)
        ourSummary=splitIntoSentences(b)
        numOfRelevantSentences = len(relevantSummary)   #A
        numOfReturnedSentences = len(ourSummary)        #B
        numOfRelevantReturnedSentences = 0              #C
        for sentences in ourSummary:
            if sentences in relevantSummary:
                numOfRelevantReturnedSentences+=1
        
        print("Article "+str(index+1))
        print("Length of our Summary: "+str(numOfReturnedSentences))
        print("Length of the Correct Summary: "+str(numOfRelevantSentences))
        print("Number of Relevant Sentences in our Summary: "+str(numOfRelevantReturnedSentences))
        print("Recall: "+str(numOfRelevantReturnedSentences/numOfRelevantSentences))    #C/A
        print("Precision: "+str(numOfRelevantReturnedSentences/numOfReturnedSentences)) #C/B
        print("============================")
        
        preSum+=numOfRelevantReturnedSentences/numOfReturnedSentences
        recSum+=numOfRelevantReturnedSentences/numOfRelevantSentences
    
print("Macro-Average: ")
print("\tPrecision: "+str(preSum/averager))
print("\tRecall: "+str(recSum/averager))
