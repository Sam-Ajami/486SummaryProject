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
from preprocess import removeSGML,tokenizeText,removeStopwords,stemWords,removePunks,isAPunk


#this object stores all relevant information about our sentences
class ourSentence:
    def __init__(self, sentence, listOfTerms, index):
        self.sentence = sentence
        self.listOfTerms = listOfTerms
        self.index = index
    sentence=""         #theSentence   
    listOfTerms=[]     #list of terms in document
    score = 0           #score
    index = -1
    #newSentence = ourSentence(sentenceString, ["hello", "world"]])
    #listOfSentences=[]
    #
    #listOfSentences[6].score = score

#used to sort list of file names in order to organize our summaries by our articles
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key.name) ] 
    return sorted(l, key = alphanum_key)

#determines if a token is a delineator for the purposes of an object
def isDelineator(words):
    if(words == "." or words == "!" or words == "?" or words == "\n"):
        return True
    else:
        return False

#defunct function
def isQuoteEnding(token, lastToken):
    if(token == "”" and lastToken == "."):
        return True
    else:
        return False

#Function to split articles into a list of sentences
#input: string representing an entire document
#output: list of strings representing the sentences in that document
def splitIntoSentences(file):
    #to determine if we're in a quote and thus shouldn't end a sentence yet
    inQuote = False
    #list to return 
    sentences = []
    #store the beginning of the current sentence
    beginning=0
    #split sentence into tokens
    tokenized = tokenizeText(file)
    #store current sentence
    sentence = ""
    #store last token
    lastToken = ""
    #process each token in document
    for token in tokenized:
        #if the token is a new line and the sentence is empty, just skip this
        if(token=="\n" and sentence==""):
            lastToken=token
            continue
        elif (token=="\n"):
            #if the token is a new line and the sentence isnt empty, append the sentence and continue
            sentences.append(sentence)
            #print(sentence)
            sentence = ""
            lastToken=token
            continue
        
        #if the token is a punctuation (except quote marks), just attach it to the end of the current sentence. Otherwise, attach it with a space
        if(isAPunk(token) and not (token=="\"" or token=="'" or token=="”" or token=="“" or token=="‘" or token=="’")):
            sentence+=token
        else:
            sentence+=" "+token

        #if we encounter a quote mark, switch between  inQuote = true or false
        if((token=="\"" or token=="”" or token=="“") and not inQuote):
            inQuote=True
        elif((token=="\"" or token=="”" or token=="“") and inQuote):
            inQuote=False #''
        #if we reach a sentence delineator and we're not in a quote,  
        if((isDelineator(token)) and not inQuote):
            #check if the sentence up till now is just newlines
            if(file[beginning:index+1]!="\n\n" and file[beginning:index+1]!="\n"):
                #otherwise, append the new sentence, reset, and continue
                sentences.append(sentence)
                #print(sentence)
                sentence = ""
        #keep track of last Token
        lastToken=token
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
    for index, sentence in enumerate(sentences):
        # Tokenize sentence
        tokens = tokenizeText(sentence)
        # Remove stopwords from sentence tokens
        tokens = removeStopwords(tokens, stopwords)
        # Stem the tokens of the sentence
        stemmed = stemWords(tokens)
        # Remove punctuations 
        stemmed = removePunks(stemmed)
        # Create ourSentence object and append to list of ourSentence objects
        sentenceObjects.append(ourSentence(sentence, stemmed, index))
    # Return the list of ourSentence objects
    return sentenceObjects


#gets scores from dictionary of term frequencies
#input dictionary of term frequencies
#output dictionary of term scores
def getScoreDictionary(termFrequencies):
    termFrequencyTuples=[]
    termScoreDict={}
    #turn dictionary into list of tuples and sort from most to least common
    for words in termFrequencies:
        termFrequencyTuples.append((words,termFrequencies[words]))
    termFrequencyTuples.sort(key=lambda tup: tup[1],reverse=True)
    #print(termFrequencyTuples)

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
    #print(termFrequencyTuples)

    #get maxRank
    maxRank=termFrequencyTuples[-1][1]
    #print(maxRank)  

    #Convert ranks into scores and place it into a dictionary
    for index, tuples in enumerate(termFrequencyTuples):
        #print(termFrequencyTuples[index][0],end=" ")
        #print(maxRank - termFrequencyTuples[index][1] + 1)
        termScoreDict[termFrequencyTuples[index][0]]= maxRank - termFrequencyTuples[index][1] + 1

    #return the dictionary
    return termScoreDict

#gets term frequencies from list of sentence objects
#input: list of sentence objects
#output: dictionary of term frequencies
def getTermFreqs(sentenceObjList): 

    word_freqs = {}
    #for each sentence in list of sentence objects
    for sentence in sentenceObjList:
        #process the term list
        for word in sentence.listOfTerms:
            #For each term in each term list
            #if we've seen the term before, increment the frequency, otherwise set it to 1
            if word in word_freqs:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1
    return word_freqs

#Calculates sentence scores
#input: list of sentence objects, dictionary of term scores
#output: dictionary of sentence objects with scores filled in
def getSentenceScores(listOfSentenceObjects,termScores): 
    OurSentence = {}
    wordSum = 0.0
    #for each sentence in the list of sentence object
    for sentence in listOfSentenceObjects:
        #go through the term list
        #for each term in the term in list
        for word in sentence.listOfTerms:
            #add the score of that term to the total
            wordSum += termScores[word]
        #divide the score the length of the sentence and add it to the score part of the sentence object
        OurSentence[sentence] = float(wordSum/float(len(sentence.listOfTerms)))
        wordSum = 0.0

    return OurSentence

'''
file = "string"
listOfSentences = splitIntoSentences(file)

listOfSentenceObjects=createSentenceObjects(listOfSentences) #return List of OurSentence
termFrequency=getTermFreqs(listOfSentenceObjects) #term dictionary term:frequency
termScores=getScoreDictionary(termFrequency)               #term dictionary term:score
listOfSentenceObjects=getSentenceScores(listOfSentenceObjects,termScores)  #List of OurSentence, with scores filled in 
sort(listOfSentenceObjects)
'''

print("\n")
#sys.argv[1]
#go through the articles from command line
with os.scandir(sys.argv[1]) as entries:
    #sort them 
    entries=natural_sort(entries)
    #for each article
    for index,entry in enumerate(entries):
        #print the name of the summary file
        print("ourSummaries/ourSummary"+str(index+1)+".txt")
        #try to remove the summary file if it already exists
        try:
            os.remove("ourSummaries/ourSummary"+str(index+1)+".txt")
        except:
            print("Wait What")
        #os.remove("ourSummaries/ourSummary"+str(index+1)+".txt")
        #open a new summary file for this article
        w = open("ourSummaries/ourSummary"+str(index+1)+".txt", "a")

        #open and read the article
        f = open(entry, "r", encoding="utf8")
        a=f.read()
        #print(a)
        #split the article into a list of sentences
        listOfSentences = splitIntoSentences(a)

        #turn list of sentences into list of sentence objects
        listOfSentenceObjects=createSentenceObjects(listOfSentences) #return List of OurSentence
        #calculate length of summary
        numSentences = len(listOfSentenceObjects)
        numSentences = math.ceil(numSentences*.30)
        #get dictionary of term frequencies
        termFrequency=getTermFreqs(listOfSentenceObjects) #term dictionary term:frequency
        #get dictionary of term scores
        termScores=getScoreDictionary(termFrequency)               #term dictionary term:score
        #fill list of sentence objects with their calculated scores
        listOfSentenceObjects=getSentenceScores(listOfSentenceObjects,termScores)  #List of OurSentence, with scores filled in 

        # turn list of sentence objects into list of sentence object, score tuples
        newList = list(listOfSentenceObjects.items())
        #sort by scores
        newList.sort(key=lambda tup: tup[1],reverse=True)
        summary=[]
        
        #go through list of sentences and add them to the summary, stopping once you reach the calculated length
        for index, sentences in enumerate(newList):
            #print(sentences[0].sentence,end=", ")
            #print(sentences[1])
            summary.append((sentences[0],sentences[0].index))
            #print(type(sentences))
            #print(type(sentences[0]))
            #print(type(sentences[1]))
            if(index==numSentences):
                break
        #sort by chronological order
        summary.sort(key=lambda tup: tup[1])
        #iterate through list of sentences and print them in the output file. 
        for sentences in summary:
            #print(sentences[0].sentence)
            #Words discounts punctuation
            if(sentences[0].sentence[0]==" "):
                w.write(sentences[0].sentence[1:])
            else:
                w.write(sentences[0].sentence)
            w.write('\n\n')

        
        #for elements in re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',a):
        #    print(elements)
        #    print("split")

