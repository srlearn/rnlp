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

from ...textprocessing import getSentences
from ...textprocessing import getBlocks
from ...parse import makeIdentifiers

import os
import sys
import unittest


class makeIdentifiersTest(unittest.TestCase):
    """
    makeIdentifiers is not elegant to test in practice (since it does a
    large amount of i/o).
    """

    def Reset(self):
        """
        Removes files created by ``parse.makeIdentifiers``, since the current
        version appends to the end of the files each time the function runs.
        """

        # TODO: Integrate this with the setup/teardown methods from unittest

        file_set = ['bk.txt',
                    'facts.txt',
                    'wordIDs.txt',
                    'sentenceIDs.txt',
                    'blockIDs.txt']
        for f in file_set:
            if os.path.isfile(f):
                os.remove(f)

    def EqualFileContents(self, fileName, expectedContents):
        """
        Open ``fileName`` and return true if the list ``expectedContents``
        match the contents of the file.
        """

        with open(fileName) as f:
            actualContents = f.read().splitlines()

        return actualContents == expectedContents

    def test_makeIdentifiers_1(self):

        # Reset state to ensure files do not exist.
        self.Reset()

        example = "Hello there. How are you?"
        sentences = getSentences(example)
        blocks = getBlocks(sentences, 1)

        # Assert that the expected lists are created from the example.
        self.assertEqual(sentences, ['Hello there', 'How are you'])
        self.assertEqual(blocks, [['Hello there'], ['How are you']])
        makeIdentifiers(blocks)

        wordIDs = ['wordID: 1_1_1', 'wordString: Hello', '',
                   'wordID: 1_1_2', 'wordString: there', '',
                   'wordID: 2_1_1', 'wordString: How', '',
                   'wordID: 2_1_2', 'wordString: are', '',
                   'wordID: 2_1_3', 'wordString: you', '']
        sentIDs = ['sentenceID: 1_1', 'sentence string: Hello there', '',
                   'sentenceID: 2_1', 'sentence string: How are you', '']
        blocIDs = ['blockID: 1', 'block sentences: Hello there', '',
                   'blockID: 2', 'block sentences: How are you', '']
        facts = ['lateSentenceInBlock(1,1_1).', 'sentenceInBlock(1_1,1).',
                 "wordString(1_1_1,'Hello').", 'partOfSpeech(1_1_1,"NN").',
                 'nextWordInSentence(1_1,1_1_1,1_1_2).',
                 'midWayWordInSentence(1_1,1_1_1).',
                 'wordInSentence(1_1_1,1_1).', "wordString(1_1_2,'there').",
                 'partOfSpeech(1_1_2,"RB").', 'lateWordInSentence(1_1,1_1_2).',
                 'wordInSentence(1_1_2,1_1).', 'lateSentenceInBlock(2,2_1).',
                 'sentenceInBlock(2_1,2).', "wordString(2_1_1,'How').",
                 'partOfSpeech(2_1_1,"WRB").',
                 'nextWordInSentence(2_1,2_1_1,2_1_2).',
                 'midWayWordInSentence(2_1,2_1_1).',
                 'wordInSentence(2_1_1,2_1).', "wordString(2_1_2,'are').",
                 'partOfSpeech(2_1_2,"VBP").',
                 'nextWordInSentence(2_1,2_1_2,2_1_3).',
                 'midWayWordInSentence(2_1,2_1_2).',
                 'wordInSentence(2_1_2,2_1).', "wordString(2_1_3,'you').",
                 'partOfSpeech(2_1_3,"PRP").',
                 'lateWordInSentence(2_1,2_1_3).',
                 'wordInSentence(2_1_3,2_1).']
        bk = ['useStdLogicVariables: true', 'setParam: treeDepth=3.',
              'setParam: nodeSize=3.', 'setParam: numOfClauses=8.',
              'mode: nextSentenceInBlock(+BID,+SID,-SID).',
              'mode: nextSentenceInBlock(+BID,-SID,+SID).',
              'mode: earlySentenceInBlock(+BID,-SID).',
              'mode: midWaySentenceInBlock(+BID,-SID).',
              'mode: lateSentenceInBlock(+BID,-SID).',
              'mode: sentenceInBlock(-SID,+BID).',
              'mode: wordString(+WID,#WSTR).',
              'mode: partOfSpeechTag(+WID,#WPOS).',
              'mode: nextWordInSentence(+SID,+WID,-WID).',
              'mode: earlyWordInSentence(+SID,-WID).',
              'mode: midWayWordInSentence(+SID,-WID).',
              'mode: lateWordInSentence(+SID,-WID).',
              'mode: wordInSentence(-WID,+SID).',
              'mode: sentenceContainsTarget(+SID,+WID).']

        # Assert that the created files match expectations.
        self.assertTrue(self.EqualFileContents('wordIDs.txt', wordIDs))
        self.assertTrue(self.EqualFileContents('sentenceIDs.txt', sentIDs))
        self.assertTrue(self.EqualFileContents('blockIDs.txt', blocIDs))
        self.assertTrue(self.EqualFileContents('facts.txt', facts))
        self.assertTrue(self.EqualFileContents('bk.txt', bk))

    def test_makeIdentifiers_2(self):

        self.Reset()

        example = "A B. C D. E F."
        sentences = getSentences(example)
        blocks = getBlocks(sentences, 1)

        self.assertEqual(sentences, ['A B', 'C D E F'])
        self.assertEqual(blocks, [['A B'], ['C D E F']])
        makeIdentifiers(blocks)

        wordIDs = ['wordID: 1_1_1', 'wordString: A', '', 'wordID: 1_1_2',
                   'wordString: B', '', 'wordID: 2_1_1', 'wordString: C', '',
                   'wordID: 2_1_2', 'wordString: D', '', 'wordID: 2_1_3',
                   'wordString: E', '', 'wordID: 2_1_4', 'wordString: F', '']
        sentIDs = ['sentenceID: 1_1', 'sentence string: A B', '',
                   'sentenceID: 2_1', 'sentence string: C D E F', '']
        blocIDs = ['blockID: 1', 'block sentences: A B', '', 'blockID: 2',
                   'block sentences: C D E F', '']
        facts = ['lateSentenceInBlock(1,1_1).', 'sentenceInBlock(1_1,1).',
                 "wordString(1_1_1,'A').", 'partOfSpeech(1_1_1,"DT").',
                 'nextWordInSentence(1_1,1_1_1,1_1_2).',
                 'midWayWordInSentence(1_1,1_1_1).',
                 'wordInSentence(1_1_1,1_1).', "wordString(1_1_2,'B').",
                 'partOfSpeech(1_1_2,"NN").', 'lateWordInSentence(1_1,1_1_2).',
                 'wordInSentence(1_1_2,1_1).', 'lateSentenceInBlock(2,2_1).',
                 'sentenceInBlock(2_1,2).', "wordString(2_1_1,'C').",
                 'partOfSpeech(2_1_1,"SYM").',
                 'nextWordInSentence(2_1,2_1_1,2_1_2).',
                 'earlyWordInSentence(2_1,2_1_1).',
                 'wordInSentence(2_1_1,2_1).', "wordString(2_1_2,'D').",
                 'partOfSpeech(2_1_2,"NN").',
                 'nextWordInSentence(2_1,2_1_2,2_1_3).',
                 'midWayWordInSentence(2_1,2_1_2).',
                 'wordInSentence(2_1_2,2_1).', "wordString(2_1_3,'E').",
                 'partOfSpeech(2_1_3,"NN").',
                 'nextWordInSentence(2_1,2_1_3,2_1_4).',
                 'lateWordInSentence(2_1,2_1_3).',
                 'wordInSentence(2_1_3,2_1).', "wordString(2_1_4,'F').",
                 'partOfSpeech(2_1_4,"NN").', 'lateWordInSentence(2_1,2_1_4).',
                 'wordInSentence(2_1_4,2_1).']
        bk = ['useStdLogicVariables: true', 'setParam: treeDepth=3.',
              'setParam: nodeSize=3.', 'setParam: numOfClauses=8.',
              'mode: nextSentenceInBlock(+BID,+SID,-SID).',
              'mode: nextSentenceInBlock(+BID,-SID,+SID).',
              'mode: earlySentenceInBlock(+BID,-SID).',
              'mode: midWaySentenceInBlock(+BID,-SID).',
              'mode: lateSentenceInBlock(+BID,-SID).',
              'mode: sentenceInBlock(-SID,+BID).',
              'mode: wordString(+WID,#WSTR).',
              'mode: partOfSpeechTag(+WID,#WPOS).',
              'mode: nextWordInSentence(+SID,+WID,-WID).',
              'mode: earlyWordInSentence(+SID,-WID).',
              'mode: midWayWordInSentence(+SID,-WID).',
              'mode: lateWordInSentence(+SID,-WID).',
              'mode: wordInSentence(-WID,+SID).',
              'mode: sentenceContainsTarget(+SID,+WID).']

        self.assertTrue(self.EqualFileContents('wordIDs.txt', wordIDs))
        self.assertTrue(self.EqualFileContents('sentenceIDs.txt', sentIDs))
        self.assertTrue(self.EqualFileContents('blockIDs.txt', blocIDs))
        self.assertTrue(self.EqualFileContents('facts.txt', facts))
        self.assertTrue(self.EqualFileContents('bk.txt', bk))
