
# -*- coding: utf-8 -*-

# Copyright © 2017-2018 StARLinG Lab
# Copyright © 2019 Alexander L. Hayes
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

import os
import string
import nltk
from tqdm import tqdm

__all__ = ["makeIdentifiers"]

def __getOutputFile(outputDir, fileName):
    if outputDir is None:
        # If no outputDir passed in, set to the current directory
        outputDir = os.getcwd()
    elif not os.path.isdir(outputDir):
        # Ensure it exists
        os.makedirs(outputDir)
    
    return os.path.join(outputDir, fileName)

    
def _writeBlock(block, blockID, outputDir=None):
    """Writes the blocks to a file with blockID."""
    outputFile = __getOutputFile(outputDir, "blockIDS.txt")
    with open(outputFile, "a") as fp:
        fp.write("blockID: " + str(blockID) + "\n")
        sentences = ""
        for sentence in block:
            sentences += sentence+","
        fp.write("block sentences: "+sentences[:-1]+"\n")
        fp.write("\n")


def _writeSentenceInBlock(sentence, blockID, sentenceID, outputDir=None):
    """writes the sentence in a block to a file with the id"""
    outputFile = __getOutputFile(outputDir, "sentenceIDs.txt")
    with open(outputFile, "a") as fp:
        fp.write("sentenceID: "+str(blockID)+"_"+str(sentenceID)+"\n")
        fp.write("sentence string: "+sentence+"\n")
        fp.write("\n")


def _writeWordFromSentenceInBlock(word, blockID, sentenceID, wordID, outputDir=None):
    """writes the word from a sentence in a block to a file with the id"""
    outputFile = __getOutputFile(outputDir, "wordIDs.txt")
    with open(outputFile, "a") as fp:
        fp.write("wordID: " + str(blockID) + "_" + str(sentenceID) + "_" + str(wordID) + "\n")
        fp.write("wordString: " + word + "\n")
        fp.write("\n")


def _writeFact(predicateString, outputDir=None):
    """writes the fact to facts file"""
    outputFile = __getOutputFile(outputDir, "facts.txt")
    with open(outputFile, "a") as f:
        f.write(predicateString+"\n")


def _writeBk(target="sentenceContainsTarget(+SID,+WID).", treeDepth="3",
             nodeSize="3", numOfClauses="8", outputDir=None):
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
    outputFile = __getOutputFile(outputDir, "bk.txt")
    with open(outputFile, "a") as bk:

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
                    treeDepth="3", nodeSize="3", numOfClauses="8", outputDir=None):
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
    :param output: Optional directory to pass in for output
    type output: str.

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
    print("Creating background file...")

    _writeBk(
        target=target,
        treeDepth=treeDepth,
        nodeSize=nodeSize,
        numOfClauses=numOfClauses,
        outputDir=outputDir
    )

    print("Creating identifiers from the blocks...")

    nBlocks = len(blocks)
    for block in tqdm(blocks):

        _writeBlock(block, blockID, outputDir)

        sentenceID = 1
        nSentences = len(block)
        beginning = nSentences/float(3)
        ending = (2*nSentences)/float(3)

        for sentence in block:

            if sentenceID < nSentences:
                # mode: nextSentenceInBlock(blockID, sentenceID, sentenceID).
                ps = "nextSentenceInBlock(" + str(blockID) + "," + \
                     str(blockID) + "_" + str(sentenceID) + "," + \
                     str(blockID) + "_" + str(sentenceID+1) + ")."
                _writeFact(ps, outputDir)

            if sentenceID < beginning:
                # mode: earlySentenceInBlock(blockID, sentenceID).
                ps = "earlySentenceInBlock(" + str(blockID) + "," + \
                     str(blockID) + "_" + str(sentenceID) + ")."
                _writeFact(ps, outputDir)
            elif sentenceID > ending:
                # mode: lateSentenceInBlock(blockID, sentenceID).
                ps = "lateSentenceInBlock(" + str(blockID) + "," + \
                     str(blockID) + "_" + str(sentenceID) + ")."
                _writeFact(ps, outputDir)
            else:
                # mode: midWaySentenceInBlock(blockID, sentenceID).
                ps = "earlySentenceInBlock(" + str(blockID) + "," + \
                     str(blockID) + "_" + str(sentenceID) + ")."
                _writeFact(ps, outputDir)

            # mode: sentenceInBlock(sentenceID, blockID).
            ps = "sentenceInBlock(" + str(blockID) + "_" + str(sentenceID) + \
                 "," + str(blockID) + ")."
            _writeFact(ps, outputDir)
            _writeSentenceInBlock(sentence, blockID, sentenceID, outputDir)

            wordID = 1
            tokens = nltk.word_tokenize(sentence)
            nWords = len(tokens)
            wBeginning = nWords/float(3)
            wEnding = (2*nWords)/float(3)

            for word in tokens:

                # mode: wordString(wordID, #str).
                ps = "wordString(" + str(blockID) + "_" + str(sentenceID) + \
                     "_" + str(wordID) + "," + "'" + str(word) + "')."
                _writeFact(ps, outputDir)

                # mode: partOfSpeechTag(wordID, #POS).
                POS = nltk.pos_tag([word])[0][1]
                ps = "partOfSpeech(" + str(blockID) + "_" + str(sentenceID) + \
                     "_" + str(wordID) + "," + '"' + str(POS) + '").'
                _writeFact(ps, outputDir)

                # mode: nextWordInSentence(sentenceID, wordID, wordID).
                if wordID < nWords:
                    ps = "nextWordInSentence(" + str(blockID) + "_" + \
                         str(sentenceID) + "," + str(blockID) + "_" + \
                         str(sentenceID) + "_" + str(wordID) + "," + \
                         str(blockID) + "_" + str(sentenceID) + "_" + \
                         str(wordID+1) + ")."
                    _writeFact(ps, outputDir)

                if wordID < wBeginning:
                    # mode: earlyWordInSentence(sentenceID, wordID).
                    ps = "earlyWordInSentence(" + str(blockID) + "_" + \
                         str(sentenceID) + "," + str(blockID) + "_" + \
                         str(sentenceID) + "_" + str(wordID) + ")."
                    _writeFact(ps, outputDir)
                elif wordID > wEnding:
                    # mode: lateWordInSentence(sentenceID< wordID).
                    ps = "lateWordInSentence(" + str(blockID) + "_" + \
                         str(sentenceID) + "," + str(blockID) + "_" + \
                         str(sentenceID) + "_" + str(wordID) + ")."
                    _writeFact(ps, outputDir)
                else:
                    # mode: midWayWordInSentence(sentenceID, wordID).
                    ps = "midWayWordInSentence(" + str(blockID) + "_" + \
                         str(sentenceID) + "," + str(blockID) + "_" + \
                         str(sentenceID) + "_" + str(wordID) + ")."
                    _writeFact(ps, outputDir)

                # mode: wordInSentence(wordID, sentenceID).
                ps = "wordInSentence(" + str(blockID) + "_" + \
                     str(sentenceID) + "_" + str(wordID) + "," + \
                     str(blockID) + "_" + str(sentenceID) + ")."
                _writeFact(ps, outputDir)
                _writeWordFromSentenceInBlock(word, blockID, sentenceID, wordID, outputDir)
                wordID += 1
            sentenceID += 1
        blockID += 1
