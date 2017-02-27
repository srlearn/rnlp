from os import listdir,system
import nltk

def textFile(file):
    '''check if text file'''
    if ".txt" in file:
        return True
    return False

def readCorpus(file):
    '''reads corpus from a directory of txt files or a file'''
    print "reading content from corpus.."
    corpus = []
    if textFile(file):
        answer = raw_input("single file provided.\n Go with this file? Yes/No: ")
        if answer.lower() == "no":
            exit()
        with open(file) as fp:
            lines = fp.read().splitlines()
            for item in lines:
                corpus += item
    else:
        print "Reading files from directory.."
        dirFiles = listdir(file)
        nFiles = len(dirFiles)
        for f in dirFiles:
            print "reading file "+str(f)+", file "+str(dirFiles.index(f)+1)+"/"+str(nFiles)
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
        answer = raw_input("facts.txt already exists, delete file or exit program, Delete/Exit?: ")
        if answer.lower() == "exit":
            exit()
        else:
            system("rm -f facts.txt")
    if "blockIDs.txt" in listdir("."):
        answer = raw_input("blockIDs.txt already exists, delete file or exit program, Delete/Exit?: ")
        if answer.lower() == "exit":
            exit()
        else:
            system("rm -f blockIDs.txt")
    if "sentenceIDs.txt" in listdir("."):
        answer = raw_input("sentenceIDs.txt already exists, delete file or exit program, Delete/Exit?: ")
        if answer.lower() == "exit":
            exit()
        else:
            system("rm -f sentenceIDs.txt")
    if "wordIDs.txt" in listdir("."):
        answer = raw_input("wordIDs.txt already exists, delete file or exit program, Delete/Exit?: ")
        if answer.lower() == "exit":
            exit()
        else:
            system("rm -f wordIDs.txt")
    
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
    
def makeIdentifiers(blocks):
    '''make unique identifiers for components of the block and write to file'''
    blockID,sentenceID,wordID = 0,0,0
    blockID = 1
    checkConsistency()
    nBlocks = len(blocks)
    for block in blocks:
        print "writing block "+str(blocks.index(block)+1)+"/"+str(nBlocks)+" to blockIDs.txt.."
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
            print "writing sentence "+str(sentenceID)+"/"+str(nSentences)+" in block id "+str(blockID)+" to sentenceIDs.txt.."
            #====================predicate: sentenceInBlock(sentenceID,blockID)=====================================
            predicateString = "sentenceInBlock("+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+")."
            writeFact(predicateString)
            #factPredicates.append(predicateString)
            writeSentenceInBlock(sentence,blockID,sentenceID)
            sentenceID += 1
            wordID = 1
            tokens = nltk.word_tokenize(sentence)
            nWords = len(tokens)
            beginning = nWords/float(3)
            ending = (2*nWords)/float(3)
            for word in tokens:
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
                    #factPredicates.append(predicateString)
                print "writing word "+str(wordID)+"/"+str(nWords)+" from sentence id "+str(sentenceID)+" in block id "+str(blockID)+" to wordIDs.txt.."
                #====================predicate: wordInSentence(wordID,sentenceID)=====================================
                predicateString = "wordInSentence("+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+","+str(blockID)+"_"+str(sentenceID)+")."
                writeFact(predicateString)
                #factPredicates.append(predicateString)
                writeWordFromSentenceInBlock(word,blockID,sentenceID,wordID)
                wordID += 1
        blockID += 1

def main():
    '''main method'''
    file = raw_input("Enter the file or folder to read the corpus from: ")
    corpus = readCorpus(file)
    sentences = getSentences(corpus)
    blocks = getBlocks(sentences,2) #can toggle number of sentences in a block
    makeIdentifiers(blocks)
main()
            
    
        
