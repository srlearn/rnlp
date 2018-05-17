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
==============

A set of functions for normalizing text, with options for stemming,
stopping, removing punctuation, etc.

Document Hierarchy
==================

A corpora is a collection of documents.
A document is a collection of chapters.
A chapter is a collection of paragraphs.
A paragraph is a collection of sentences.
A sentence is a collection of words.
A word is a collection of letters.

The depth of reasoning probably depends on the domain you are working on.
"""

from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *

import string

_punctuation = string.punctuation
_stemmer = PorterStemmer()
_stopwords = stopwords.word('english')

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

    
