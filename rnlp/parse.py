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
rnlp.parse
----------
"""

from __future__ import print_function
from __future__ import division

try:
   input = raw_input
except NameError:
   pass

# Standard Python Library
import string

# Non-standard Python Library
import nltk
from tqdm import tqdm
from .textprocessing import getSentences
from .textprocessing import getBlocks

def _writeBlock(block,blockID):
    '''writes the block to a file with the id'''
    with open("blockIDs.txt","a") as fp:
        fp.write("blockID: "+str(blockID)+"\n")
        sentences = ""
        for sentence in block:
            sentences += sentence+","
        fp.write("block sentences: "+sentences[:-1]+"\n")
        fp.write("\n")

def _writeSentenceInBlock(sentence,blockID,sentenceID):
    '''writes the sentence in a block to a file with the id'''
    with open("sentenceIDs.txt","a") as fp:
        fp.write("sentenceID: "+str(blockID)+"_"+str(sentenceID)+"\n")
        fp.write("sentence string: "+sentence+"\n")
        fp.write("\n")

def _writeWordFromSentenceInBlock(word,blockID,sentenceID,wordID):
    '''writes the word from a sentence in a block to a file with the id'''
    with open("wordIDs.txt","a") as fp:
        fp.write("wordID: "+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+"\n")
        fp.write("wordString: "+word+"\n")
        fp.write("\n")

def _writeFact(predicateString):
    '''writes the fact to facts file'''
    with open("facts.txt","a") as f:
        f.write(predicateString+"\n")

def _writeBk(target="sentenceContainsTarget(+SID,+WID).", treeDepth="3",
            nodeSize="3", numOfClauses="8"):
    """
    Writes a background file to disk.

    :param target: Target predicate with modes.
    :type target: str.
    :param treeDepth: Depth of the tree.
    :type treeDepth: str.
    :param nodeSize: Maximum size of each node in the tree.
    :type nodeSize: str.
    :param numOfClauses: Number of clauses in total.
    :type numOfClauses: str.
    """

    with open('bk.txt', 'w') as bk:

        bk.write("useStdLogicVariables: true\n")

        bk.write("setParam: treeDepth=" + str(treeDepth) + '.\n')
        bk.write("setParam: nodeSize=" + str(nodeSize) + '.\n')
        bk.write("setParam: numOfClauses=" + str(numOfClauses) + '.\n')

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

        bk.write("mode: " + target + "\n")

    return

def makeIdentifiers(blocks, target="sentenceContainsTarget(+SID,+WID).",
                    treeDepth="3", nodeSize="3", numOfClauses="8"):
    """
    Make unique identifiers for components of the block and write to files.

    :param blocks: Blocks of sentences (likely the output of
                   ``textprocessing.getBlocks``).
    :type blocks: list
    :param target: Target to write to the background file (another option might
                   be ``blockContainsTarget(+BID,+SID).``).
    :type target: str.
    :param treeDepth: Depth of the tree.
    :type treeDepth: str.
    :param nodeSize: Maximum size of each node in the tree.
    :type nodeSize: str.
    :param numOfClauses: Number of clauses in total.
    :type numOfClauses: str.

    .. note:: This is a function that writes *facts*, presently there is no
      way to distinguish between these and positive/negatives examples.

    Example:

    .. code-block:: python

                    from rnlp.textprocessing import getSentences
                    from rnlp.textprocessing import getBlocks
                    from rnlp.parse import makeIdentifiers

                    example = "Hello there. How are you? I am fine."

                    sentences = getSentences(example)
                    # ['Hello there', 'How are you', 'I am fine']

                    blocks = getBlocks(sentences, 2)
                    # with 1: [['Hello there'], ['How are you'], ['I am fine']]
                    # with 2: [['Hello there', 'How are you'], ['I am fine']]
                    # with 3: [['Hello there', 'How are you', 'I am fine']]

                    makeIdentifiers(blocks)
                    # 100%|██████████████████████| 2/2 [00:00<00:00, 18.49it/s]
    """
    blockID, sentenceID, wordID = 1, 0, 0
    #checkConsistency()
    print("Creating background file...")

    _writeBk(target=target, treeDepth=treeDepth,
             nodeSize=nodeSize, numOfClauses=numOfClauses)

    print("Creating identifiers from the blocks...")
    nBlocks = len(blocks)
    for block in tqdm(blocks):

        _writeBlock(block, blockID)

        sentenceID = 1
        nSentences = len(block)
        beginning = nSentences/float(3)
        ending = (2*nSentences)/float(3)

        for sentence in block:

            if sentenceID < nSentences:
                #=====================predicate: nextSentenceInBlock(blockID,sentenceID,sentenceID)======================
                predicateString = "nextSentenceInBlock("+str(blockID)+","+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+"_"+str(sentenceID+1)+")."
                _writeFact(predicateString)
            #=====================predicate: earlySentenceInBlock(blockID,sentenceID)===========================
            if sentenceID < beginning:
                predicateString = "earlySentenceInBlock("+str(blockID)+","+str(blockID)+"_"+str(sentenceID)+")."
                _writeFact(predicateString)
            #=====================predicate: midWaySentenceInBlock(blockID,sentenceID)==========================
            if sentenceID >= beginning and sentenceID < ending:
                predicateString = "earlySentenceInBlock("+str(blockID)+","+str(blockID)+"_"+str(sentenceID)+")."
                _writeFact(predicateString)
            #=====================predicate: lateSentenceInBlock(blockID,sentenceID)============================
            if sentenceID > ending:
                predicateString = "lateSentenceInBlock("+str(blockID)+","+str(blockID)+"_"+str(sentenceID)+")."
                _writeFact(predicateString)
            #print("writing sentence "+str(sentenceID)+"/"+str(nSentences)+" in block id "+str(blockID)+" to sentenceIDs.txt..")
            #====================predicate: sentenceInBlock(sentenceID,blockID)=====================================
            predicateString = "sentenceInBlock("+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+")."
            _writeFact(predicateString)
            _writeSentenceInBlock(sentence,blockID,sentenceID)
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
                _writeFact(predicateString)
                #============predicate: partOfSpeechTag(wordID,#POS)=============
                POS = nltk.pos_tag([word])[0][1]
                predicateString = "partOfSpeech("+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+","+"\""+str(POS)+"\")."
                _writeFact(predicateString)
                if wordID < nWords:
                    #====================predicate: nextWordInSentence(sentenceID,wordID,wordID)==========================
                    predicateString = "nextWordInSentence("+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+","+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID+1)+")."
                    _writeFact(predicateString)
                #=====================predicate: earlyWordInSentence(sentenceID,wordID)===========================
                if wordID < beginning:
                    predicateString = "earlyWordInSentence("+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+")."
                    _writeFact(predicateString)
                #=====================predicate: midWayWordInSentences(sentenceID,wordID)==========================
                if wordID >= beginning and wordID < ending:
                    predicateString = "midWayWordInSentence("+str(blockID)+"_"+str(sentenceID)+","+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+")."
                    _writeFact(predicateString)
                #=====================predicate: lateWordInSentence(sentenceID,wordID)============================
                if sentenceID > ending:
                    predicateString = "lateSentenceInBlock("+str(blockID)+","+str(blockID)+"_"+str(sentenceID)+")."
                    _writeFact(predicateString)
                #print("writing word "+str(wordID)+"/"+str(nWords)+" from sentence id "+str(sentenceID)+" in block id "+str(blockID)+" to wordIDs.txt..")
                #====================predicate: wordInSentence(wordID,sentenceID)=====================================
                predicateString = "wordInSentence("+str(blockID)+"_"+str(sentenceID)+"_"+str(wordID)+","+str(blockID)+"_"+str(sentenceID)+")."
                _writeFact(predicateString)
                _writeWordFromSentenceInBlock(word,blockID,sentenceID,wordID)
                wordID += 1
        blockID += 1
