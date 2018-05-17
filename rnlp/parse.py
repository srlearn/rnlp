# Copyright (C) 2017-2018 StARLinG Lab
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (at the base of this repository). If not,
# see <http://www.gnu.org/licenses/>

"""
Depencencies: nltk, future: (pip install nltk future)
nltk models: averaged_perceptron_tagger, punkt

   $ python
   >>> import nltk
   >>> nltk.download()
   [navigate to the models tab and download averaged_perceptron_tagger and punkt]
"""

from __future__ import print_function
from builtins import input

from os import listdir
from os import system
from sys import argv

import nltk

def textFile(file):
    '''check if text file'''
    return '.txt' in file

def readCorpus(file):
    '''reads corpus from a directory of txt files or a file'''
    print("reading content from corpus..")
    corpus = []
    if textFile(file):

        answer = input("Single file provided.\n Go with this file? Yes/No: ")

        if answer.lower() == "no":
            exit()
        with open(file) as fp:
            lines = fp.read().splitlines()
            for item in lines:
                corpus += item
    else:
        print("Reading files from directory..")
        dirFiles = listdir(file)
        nFiles = len(dirFiles)
        for f in dirFiles:
            print("reading file "+str(f)+", file "+str(dirFiles.index(f)+1)+"/"+str(nFiles))
            with open(file+"/"+f) as fp:
                fLines = fp.read().splitlines()
                for item in fLines:
                    corpus += item
    return "".join(corpus)

def removePunctuations(sentence):
    '''removes punctuations from a sentence'''
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in sentence:
       if char not in punctuations:
           no_punct = no_punct + char
    return no_punct

def getSentences(corpus):
    '''tokenize the corpus into sentences'''
    sentences = nltk.sent_tokenize(corpus)
    sentences = [removePunctuations(sentence) for sentence in sentences]
    return sentences

def getBlocks(sentences,n):
    '''get blocks of n sentences together'''
    N = len(sentences)
    blocks = []
    for i in range(0,N,n):
        blocks.append(sentences[i:(i+n)])
    return blocks

def checkConsistency():
    '''checks for system errors/conflicts'''
    if "facts.txt" in listdir("."):

        answer = input("facts.txt already exists, delete file or exit program, Delete/Exit?: ")

        if answer.lower() == "exit":
            exit()
        else:
            system("rm -f facts.txt")
    if "blockIDs.txt" in listdir("."):

        answer = input("blockIDs.txt already exists, delete file or exit program, Delete/Exit?: ")

        if answer.lower() == "exit":
            exit()
        else:
            system("rm -f blockIDs.txt")
    if "sentenceIDs.txt" in listdir("."):

        answer = input("sentenceIDs.txt already exists, delete file or exit program, Delete/Exit?: ")

        if answer.lower() == "exit":
            exit()
        else:
            system("rm -f sentenceIDs.txt")
    if "wordIDs.txt" in listdir("."):

        answer = input("wordIDs.txt already exists, delete file or exit program, Delete/Exit?: ")

        if answer.lower() == "exit":
            exit()
        else:
            system("rm -f wordIDs.txt")
    if "bk.txt" in listdir("."):

        answer = input("bk.txt already exists, program will generate new one, OK/Exit?: ")

        if answer.lower() == "exit":
            exit()
        else:
            system("rm -f bk.txt")

def writeBlock(block,blockID):
    '''writes the block to a file with the id'''
    with open("blockIDs.txt","a") as fp:
        fp.write("blockID: "+str(blockID)+"\n")
        sentences = ""
        for sentence in block:
            sentences += sentence+","
        fp.write("block sentences: "+sentences[:-1]+"\n")
        fp.write("\n")

def writeSentenceInBlock(sentence,blockID,sentenceID):
    '''writes the sentence in a block to a file with the id'''
    with open("sentenceIDs.txt","a") as fp:
        fp.write("sentenceID: "+str(blockID)+"_"+str(sentenceID)+"\n")
        fp.write("sentence string: "+sentence+"\n")
        fp.write("\n")

def writeWordFromSentenceInBlock(word,blockID,sentenceID,wordID):
    '''writes the word from a sentence in a block to a file with the id'''
    with open("wordIDs.txt","a") as fp:
        fp.write("wordID: "+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+"\n")
        fp.write("wordString: "+word+"\n")
        fp.write("\n")

def writeFact(predicateString):
    '''writes the fact to facts file'''
    with open("facts.txt","a") as f:
        f.write(predicateString+"\n")

def setParam(parameter,bk,defaultValue):
    '''gets parameter value from user'''
    parameterValue = defaultValue

    answer = input("Enter Custom "+parameter+"?(yes/no). default "+parameter+" is "+parameterValue+": ")

    if answer.lower()=="yes":

        parameterValue = input("Enter " + parameter + ": ")

    bk.write("setParam: " + parameter + "=" + parameterValue + ".\n")

def getTarget():
    '''gets the object of inference from the user(target)'''
    #choice = raw_input("choose target: \n1.sentenceContainsTarget(+SID,+WID)\n2.blockContainsTarget(+BID,+SID)\n3.Both\n4.new target\nEnter choice: ")

    choice = input("choose target: \n1.sentenceContainsTarget(+SID,+WID)\n2.blockContainsTarget(+BID,+SID)\n3.Both\n4.new target\nEnter choice: ")

    if int(choice) == 1:
        return "mode: sentenceContainsTarget(+SID,+WID).\n"
    elif int(choice) == 2:
        return "mode: blockContainsTarget(+BID,+SID).\n"
    elif int(choice) == 3:
        return "mode: sentenceContainsTarget(+SID,+WID).\n"+"mode: blockContainsTarget(+BID,+SID).\n"
    elif int(choice) == 4:
        newPredicate = input("Enter the target predicate with modes: ")
        return newPredicate

def makeIdentifiers(blocks):
    '''make unique identifiers for components of the block and write to file'''
    blockID,sentenceID,wordID = 0,0,0
    blockID = 1
    checkConsistency()
    print("Creating background file..")
    bk = open("bk.txt","a")
    bk.write("useStdLogicVariables: true\n")
    setParam("treeDepth",bk,"3")
    setParam("nodeSize",bk,"3")
    setParam("numOfClauses",bk,"8")
    bk.write("mode: nextSentenceInBlock(+BID,+SID,-SID).\n")
    bk.write("mode: nextSentenceInBlock(+BID,-SID,+SID).\n")
    bk.write("mode: earlySentenceInBlock(+BID,-SID).\n")
    bk.write("mode: midWaySentenceInBlock(+BID,-SID).\n")
    bk.write("mode: lateSentenceInBlock(+BID,-SID).\n")
    bk.write("mode: sentenceInBlock(-SID,+BID).\n")
    bk.write("mode: wordString(+WID,#WSTR).\n")
    bk.write("mode: partOfSpeechTag(+WID,#WPOS).\n")
    bk.write("mode: nextWordInSentence(+SID,+WID,-WID).\n")
    bk.write("mode: earlyWordInSentence(+SID,-WID).\n")
    bk.write("mode: midWayWordInSentence(+SID,-WID).\n")
    bk.write("mode: lateWordInSentence(+SID,-WID).\n")
    bk.write("mode: wordInSentence(-WID,+SID).\n")
    target = getTarget()
    bk.write("mode: "+target)
    bk.close()
    nBlocks = len(blocks)
    for block in blocks:
        print("writing block "+str(blocks.index(block)+1)+"/"+str(nBlocks)+" to blockIDs.txt..")
        writeBlock(block,blockID)
        sentenceID = 1
        nSentences = len(block)
        beginning = nSentences/float(3)
        ending = (2*nSentences)/float(3)
        for sentence in block:
            if sentenceID < nSentences:
                #=====================predicate: nextSentenceInBlock(blockID,sentenceID,sentenceID)======================
                predicateString = "nextSentenceInBlock("+str(blockID)+","+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+"_"+str(sentenceID+1)+")."
                writeFact(predicateString)
            #=====================predicate: earlySentenceInBlock(blockID,sentenceID)===========================
            if sentenceID < beginning:
                predicateString = "earlySentenceInBlock("+str(blockID)+","+str(blockID)+"_"+str(sentenceID)+")."
                writeFact(predicateString)
            #=====================predicate: midWaySentenceInBlock(blockID,sentenceID)==========================
            if sentenceID >= beginning and sentenceID < ending:
                predicateString = "earlySentenceInBlock("+str(blockID)+","+str(blockID)+"_"+str(sentenceID)+")."
                writeFact(predicateString)
            #=====================predicate: lateSentenceInBlock(blockID,sentenceID)============================
            if sentenceID > ending:
                predicateString = "lateSentenceInBlock("+str(blockID)+","+str(blockID)+"_"+str(sentenceID)+")."
                writeFact(predicateString)
            print("writing sentence "+str(sentenceID)+"/"+str(nSentences)+" in block id "+str(blockID)+" to sentenceIDs.txt..")
            #====================predicate: sentenceInBlock(sentenceID,blockID)=====================================
            predicateString = "sentenceInBlock("+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+")."
            writeFact(predicateString)
            writeSentenceInBlock(sentence,blockID,sentenceID)
            sentenceID += 1
            wordID = 1
            tokens = nltk.word_tokenize(sentence)
            nWords = len(tokens)
            beginning = nWords/float(3)
            ending = (2*nWords)/float(3)
            for word in tokens:
                #============predicate: wordString(wordID,#str)==================
                '''
                if word == "you":
                    pos = open("pos.txt","a")
                    word = str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)
                    sentence = str(blockID)+"_"+str(sentenceID)
                    pos.write("sentenceContainsTarget("+sentence+","+word+").\n")
                    pos.close()
                else:
                    neg = open("neg.txt","a")
                    word = str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)
                    sentence = str(blockID)+"_"+str(sentenceID)
                    neg.write("sentenceContainsTarget("+sentence+","+word+").\n")
                    neg.close()
                '''
                predicateString = "wordString("+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+","+"\'"+str(word)+"\')."
                writeFact(predicateString)
                #============predicate: partOfSpeechTag(wordID,#POS)=============
                POS = nltk.pos_tag([word])[0][1]
                predicateString = "partOfSpeech("+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+","+"\""+str(POS)+"\")."
                writeFact(predicateString)
                if wordID < nWords:
                    #====================predicate: nextWordInSentence(sentenceID,wordID,wordID)==========================
                    predicateString = "nextWordInSentence("+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+","+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID+1)+")."
                    writeFact(predicateString)
                #=====================predicate: earlyWordInSentence(sentenceID,wordID)===========================
                if wordID < beginning:
                    predicateString = "earlyWordInSentence("+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+")."
                    writeFact(predicateString)
                #=====================predicate: midWayWordInSentences(sentenceID,wordID)==========================
                if wordID >= beginning and wordID < ending:
                    predicateString = "midWayWordInSentence("+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+")."
                    writeFact(predicateString)
                #=====================predicate: lateWordInSentence(sentenceID,wordID)============================
                if sentenceID > ending:
                    predicateString = "lateSentenceInBlock("+str(blockID)+","+str(blockID)+"_"+str(sentenceID)+")."
                    writeFact(predicateString)
                print("writing word "+str(wordID)+"/"+str(nWords)+" from sentence id "+str(sentenceID)+" in block id "+str(blockID)+" to wordIDs.txt..")
                #====================predicate: wordInSentence(wordID,sentenceID)=====================================
                predicateString = "wordInSentence("+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+","+str(blockID)+"_"+str(sentenceID)+")."
                writeFact(predicateString)
                writeWordFromSentenceInBlock(word,blockID,sentenceID,wordID)
                wordID += 1
        blockID += 1

def main():
    '''main method'''
    n = 2
    if "-blockSize" not in argv:
        print("defaulting to block size "+str(n))
    else:
        n = int(argv[(argv.index("-blockSize"))+1])

    chosenFile = input("Enter the file or folder to read the corpus from: ")

    corpus = readCorpus(chosenFile)
    sentences = getSentences(corpus)
    blocks = getBlocks(sentences,n) #can toggle number of sentences in a block
    makeIdentifiers(blocks)
#main()
