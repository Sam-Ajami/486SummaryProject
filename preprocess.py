import sys
import re
import os
import string
from itertools import groupby
from operator import itemgetter
from stemmer import PorterStemmer


def removeSGML(input):
    return re.sub('<[^>]+>', '', input)

def tokenizeText(tokenInput):
    #do standard python split, and find exceptions
    split = tokenInput.split()
    #split=re.findall(r'\S+|\n',tokenInput)
    #print(split)

    for index,words in enumerate(split):
        #print(words+str(index))
        #print("VVVVSTARTVVVV")
        #print(words)
        #input('Continue?')

        #get first and last character for checking for punctuation 
        firstChar=words[0]
        lastChar=words[-1]

        if((len(words)==1) and words in string.punctuation):
            #print("found punctuation!")
            #del split[index]
            #index-=1
            continue

        if((len(words)==1) or words == "'s"):
            #print("found one character word or 's!")
            continue

        #Contraction breakdown - Single Character breakdowns
        leave = True
        while(leave and (len(words)>2) and ((words[-2]=="'") or (words[-2]=="’"))):
            
            if(words[-1]=="s"):                 #'s -> 's 
                leave = False                   #It's too hard to tell when a 's is possesive of contractive, all are treated as possessive 
                split[index]=words[:-2]
                split.insert(index+1, "'s")
            elif (words[-1]=="d"):              #'d -> had
                leave = False
                split[index]=words[:-2]
                split.insert(index+1, "had")
            elif (words[-1]=="m"):              #'m -> am
                leave = False
                split[index]=words[:-2]
                split.insert(index+1, "am")
            elif (words[-1]=="t"):              #n't -> not
                leave = False
                split[index]=words[:-3]
                split.insert(index+1, "not")
            #reset word and check if we should loop again
            words=split[index]
            if (leave):
                leave = False
            else:
                leave = True

        #Contraction breakdown - double Character breakdowns
        while(leave and (len(words)>3) and ((words[-3]=="'") or (words[-2]=="’"))):
            #print("found contraction! B!")
            if(words[-2]=="l"):                 #'ll -> will
                leave = False
                split[index]=words[:-3]
                split.insert(index+1, "will")
            elif(words[-2]=="v"):                 #'ve -> have
                leave = False
                split[index]=words[:-3]
                split.insert(index+1, "have")
            elif(words[-2]=="r"):                 #'re -> are
                leave = False
                split[index]=words[:-3]
                split.insert(index+1, "are")
            #reset word and check if we should loop again
            words=split[index]
            if (leave):
                leave = False
            else:
                leave = True
        #clean punctuation off the end of the word
        while((len(words)>1) 
            and ((lastChar=="." and words.count(".")<2) #saves acronyms by skipping any word with multiple period
            or (lastChar=="," and words.count(",")<2)   #saves numbers by skipping any word with multiple comma
            or (lastChar=="’")
            or (lastChar=="‘")
            or (lastChar=="”")
            or (lastChar=="“")
            or ((lastChar in string.punctuation) and not ((lastChar==",") or (lastChar=="."))))):
            #print("found last character is punctuation!")
            split[index]=words[:-1]
            words=split[index]
            split.insert(index+1, lastChar)
            if(len(words)>0):
                lastChar=words[-1]
            #print(words+str(index))

        #clean punctuation off the front of the word
        while((len(words)>1) 
            and(((firstChar in string.punctuation) and not (firstChar=="."))
            or (firstChar=="’")
            or (firstChar=="‘")
            or (firstChar=="”")
            or (firstChar=="“"))):
            #print("found first character is punctuation!")
            split[index]=words[1:]
            words=split[index]
            split.insert(index, firstChar)
            index-=1
            if(len(words)>0):
                firstChar=words[0]
            #print(words+str(index))
        #print("Initial Word: " +words)
        #print("Final Word: " + split[index])
        #print("^^^^STOP^^^^")
            
    #print(split)
    return split

def inStopWords (word, stopwords):
    if word.lower() in stopwords:
        return True
    else:
        return False

def removeStopwords(input,stopwords):
    
    returnPut = [x for x in input if not inStopWords(x,stopwords)]
    return returnPut


def isAPunk (word):
    if (word.lower() in string.punctuation) or word.lower()=="”" or word.lower()=="“" or word.lower()=="‘" or word.lower()=="’":
        return True
    else:
        return False

def removePunks(input):
    
    returnPut = [x for x in input if not isAPunk(x)]
    return returnPut

def stemWords(input):
    stem = PorterStemmer()
    for index,entries in enumerate(input):
        input[index]=stem.stem(entries,0,len(entries)-1)
    return input


def main():
    #print(stemWords("natural"))
    #print(stemWords("nature"))
    totalList = []

    s = open("stopwords", "r")
    stopwords = s.read().split()

    with os.scandir(sys.argv[1]) as entries:
        for index,entry in enumerate(entries):
            f = open(entry, "r")
            #print(removeSGML(f.read()))
            #print("Processing File "+str(index))
            removed = removeSGML(f.read())
            tokenized = tokenizeText(removed)
            #print(tokenized)
            stopWordFree = removeStopwords(tokenized,stopwords)
            #print(stopWordFree)
            stemmed = stemWords(stopWordFree)
            totalList=totalList+stemmed

    try:
        os.remove("preprocess.output")
    except:
        pass
    w = open("preprocess.output", "a")

    #Words discounts punctuation
    w.write("Words ")
    w.write(str(len(removePunks(totalList)))+'\n')

    #Vocabulary does not
    new_set = set(totalList)
    w.write("Vocabulary ")
    w.write(str(len(new_set))+'\n')

    #get count of each word in dictionary
    w.write("Top 50 words\n")
    new_set = set(removePunks(totalList))
    res = dict.fromkeys(new_set, 0) 
        
    for key,value in res.items():
        #print("Processing "+key)
        res[key]=totalList.count(key)

    #print(res)
    newTotalList = [(k, v) for k, v in res.items()] 
    #print(type(newTotalList))
    #print(newTotalList)

    #special sorting of typles
    newTotalList.sort(key=itemgetter(1),reverse=True)

    #print(type(newTotalList))
    #print(newTotalList)
    counter = 0
    for items in newTotalList:
        #print(items[0]+" "+str(items[1]))
        w.write(items[0]+" "+str(items[1])+"\n")
        counter+=1
        if(counter==50):
            break
    w.close()

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()