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
textprocessing
--------------

A set of functions for normalizing text, with options for stemming,
stopping, removing punctuation, etc.

Document Hierarchy
------------------

A corpora is a collection of documents.
A document is a collection of chapters.
A chapter is a collection of paragraphs.
A paragraph is a collection of sentences.
A sentence is a collection of words.
A word is a collection of letters...

The depth of reasoning probably depends on the domain you are working on.
"""

from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *

import string

_punctuation = string.punctuation
_stemmer = PorterStemmer()
_stopwords = stopwords.words('english')

def __removePunctuation(text_string):
    """
    Removes punctuation symbols from a string.

    :param text_string: A string.
    :type text_string: str.

    :returns: The input ``text_string`` with punctuation symbols removed.
    :rtype: str.

    >>> from rnlp.textprocessing import __removePunctuation
    >>> example = 'Hello, World!'
    >>> __removePunctuation(example)
    'Hello World'
    """
    return text_string.strip(_punctuation)

def __removeStopwords(text_list):
    """
    Removes stopwords contained in a list of words.

    :param text_string: A list of strings.
    :type text_string: list.

    :returns: The input ``text_list`` with stopwords removed.
    :rtype: list
    """

    output_list = []

    for word in text_list:
        if word.lower() not in _stopwords:
            output_list.append(word)

    return output_list

def getBlocks(sentences, n):
    """
    Get blocks of n sentences together.

    :param sentences: List of strings where  each string is a sentence.
    :type sentences: list
    :param n: Maximum blocksize for sentences, i.e. a block will be composed of
              ``n`` sentences.
    :type n: int.

    :returns: Blocks of n sentences.
    :rtype: list-of-lists

    .. code-block:: python

                    import rnlp

                    example = "Hello there. How are you? I am fine."

                    sentences = rnlp.getSentences(example)
                    # ['Hello there', 'How are you', 'I am fine']

                    blocks = rnlp.getBlocks(sentences, 2)
                    # with 1: [['Hello there'], ['How are you'], ['I am fine']]
                    # with 2: [['Hello there', 'How are you'], ['I am fine']]
                    # with 3: [['Hello there', 'How are you', 'I am fine']]
    """
    blocks = []
    for i in range(0, len(sentences), n):
        blocks.append(sentences[i:(i+n)])
    return blocks

def getSentences(text_string):
    """
    Tokenizes the corpus into sentences, removing punctuation as it does so.

    :param text_string: A string.
    :type text_string: str.

    :returns: A list of string sentences with punctuation removed.
    :rtype: list

    .. code-block:: python

                    import rnlp

                    example = "Hello there. How are you? I am fine."
                    sentences = rnlp.getSentences(example)
                    # ['Hello there', 'How are you', 'I am fine']
    """
    return [__removePunctuation(s) for s in sent_tokenize(text_string)]
