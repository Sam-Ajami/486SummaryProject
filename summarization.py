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
    if(words == "." or words == "!" or words == "?" or words == "\n"):
        return True
    else:
        return False

def splitIntoSentences(file):
    inQuote = False
    sentences = []
    beginning = 0
    for index, words in enumerate(file):
        if(words == "\"" and not inQuote):
            inQuote = True
        elif(words == "\"" and inQuote):
            inQuote = False #
        if(isDelineator(words) and not inQuote):
            if(file[beginning:index+1] != "\n\n" and file[beginning:index+1]!= "\n"):
                sentences.append(file[beginning:index+1].replace("\n", ""))
                beginning=index+1
            
    return sentences

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

#Attach to each sentence, a set of its terms.
#Remove stop words from each of these sets.
#Associate words with their grammatical coun-terparts (stemming) for each of these sets.


#Attach to each sentence the sum of their words’ points, divided by the length of the sentence