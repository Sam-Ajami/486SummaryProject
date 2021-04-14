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
    #print("\n\n")
    inQuote=False
    sentences = []
    beginning=0
    tokenized = tokenizeText(file.replace("”", "\"").replace("“", "\"").replace("‘", "'").replace("’", "'"))
    sentence = ""
    for token in tokenized:
        token=token
        if(isAPunk(token) and not (token=="\"" or token=="'" or token=="”" or token=="“" or token=="‘" or token=="’")):
            sentence+=token
        else:
            sentence+=" "+token

        if((token=="\"" or token=="”" or token=="“") and not inQuote):
            inQuote=True
        elif((token=="\"" or token=="”" or token=="“") and inQuote):
            inQuote=False #
        if(isDelineator(token) and not inQuote):
            if(file[beginning:index+1]!="\n\n" and file[beginning:index+1]!="\n"):
                sentence=sentence.replace("”", "\"")
                sentence=sentence.replace("“", "\"")
                sentence=sentence.replace("‘", "'")
                sentence=sentence.replace("’", "'")
                sentences.append(sentence.lower())
                #print(sentence.lower(),end="\n\n")
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
        if(index==18):
            print("here dummy")
        averager+=1
        f = open(entry, "r", encoding="utf8")
        g = open(ourSummaries[index], "r", encoding="utf8")
        a=f.read()
        b=g.read()
        relevantSummary=splitIntoSentences(a)
        relevantSummarySum=""
        for sentences in relevantSummary:
            relevantSummarySum+=sentences
        ourSummary=splitIntoSentences(b)
        numOfRelevantSentences = len(relevantSummary)   #A
        numOfReturnedSentences = len(ourSummary)        #B
        numOfRelevantReturnedSentences = 0              #C
        for sentences in ourSummary:   
            if relevantSummarySum.find(sentences)>-1:
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
print("\tRecall: "+str(recSum/averager))
print("\tPrecision: "+str(preSum/averager))
