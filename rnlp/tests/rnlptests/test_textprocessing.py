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

import sys
import unittest

sys.path.append('./')

from rnlp import textprocessing

class removePunctuationTest(unittest.TestCase):
    """
    removePunctuation uses strip() to remove characters at the end.
    """

    def test_removePunctuation_1(self):
        sent = '.?:'
        self.assertEqual(textprocessing._removePunctuation(sent), '')

    def test_removePunctuation_2(self):
        sent = 'helloself.'
        self.assertEqual(textprocessing._removePunctuation(sent), 'helloself')

    def test_removePunctuation_3(self):
        sent = 'Hi.There'
        self.assertEqual(textprocessing._removePunctuation(sent), 'HiThere')

    def test_removePunctuation_4(self):
        import string
        sent = string.punctuation
        self.assertEqual(textprocessing._removePunctuation(sent), '')

    def test_removePunctuation_5(self):
        sent = '(def add1 (lambda (n)) + n 1)'
        self.assertEqual(textprocessing._removePunctuation(sent),
                         'def add1 lambda n  n 1')

class removeStopwordsTest(unittest.TestCase):

    def test_removeStopwords_1(self):
        sent = 'and then there were none'.split()
        self.assertEqual(textprocessing._removeStopwords(sent),
                         ['none'])

    def test_removeStopwords_2(self):
        sent = 'no stopwords here'.split()
        self.assertEqual(textprocessing._removeStopwords(sent),
                         ['stopwords'])

    def test_removeStopwords_3(self):
        from nltk.corpus import stopwords
        sent = stopwords.words('english')
        self.assertEqual(textprocessing._removeStopwords(sent), [])

    def test_removeStopwords_4(self):
        sent = 'finally'.split()
        self.assertEqual(textprocessing._removeStopwords(sent), ['finally'])

class getSentencesTest(unittest.TestCase):

    def test_getSentences_1(self):
        sents = 'Hi there. Hello there. Bye now.'
        self.assertEqual(textprocessing.getSentences(sents),
                         ['Hi there', 'Hello there', 'Bye now'])

    def test_getSentences_2(self):
        sents = 'We hold these truths to be self evident.'
        self.assertEqual(textprocessing.getSentences(sents),
                         ['We hold these truths to be self evident'])

    def test_getSentences_3(self):
        sents = 'One. Two three. Three. Four'
        self.assertEqual(textprocessing.getSentences(sents),
                         ['One', 'Two three', 'Three', 'Four'])

class getBlocks(unittest.TestCase):

    def test_getBlocks_1(self):
        sents = textprocessing.getSentences('Hello. How are you? I am fine.')
        self.assertEqual(textprocessing.getBlocks(sents, 1),
                [['Hello'], ['How are you'], ['I am fine']])
        self.assertEqual(textprocessing.getBlocks(sents, 2),
                [['Hello', 'How are you'], ['I am fine']])
        self.assertEqual(textprocessing.getBlocks(sents, 3),
                [['Hello', 'How are you', 'I am fine']])

    def test_getBlocks_2(self):
        sents = textprocessing.getSentences("""How do you document real life?
        When real life's getting more like fiction each day? Headlines,
        breadlines blow my mind, and now this deadline.""")
        self.assertEqual(textprocessing.getBlocks(sents, 1),
        [['How do you document real life'],
        ["When real lifes getting more like fiction each day"],
        ["Headlines\n        breadlines blow my mind and now this deadline"]])

    def test_getBlocks_3(self):
        sents = textprocessing.getSentences(
            "RENT. How do you write a song when the chords sound wrong?")
        self.assertEqual(textprocessing.getBlocks(sents, 1),
            [['RENT'], ['How do you write a song when the chords sound wrong']])
        self.assertEqual(textprocessing.getBlocks(sents, 2),
            [['RENT', 'How do you write a song when the chords sound wrong']])
