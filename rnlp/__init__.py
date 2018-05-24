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
rnlp
====

``pip install rnlp``

**Relational-NLP Preprocessing** (rnlp) is a Python package for converting text
corpus into a set of relational facts.

Designed for use with BoostSRL (https://github.com/starling-lab/BoostSRL).

Motivation
==========

There is no doubt that natural language processing (nlp) is a difficult task,
but recent work has kindled interest in modeling the context or relations
between words and their meanings in high-dimensional spaces.

The intent of this package is to help with building systems which explicitly
model words as a series of entities, relations, and attributes on those
relations.

If words are entities, then their position in a certain document is as relation
between the word and a document entity, their context is a set of relations
between the word entity and the other words it appears near, their attributes
may be the part of speech, etc.

Examples
========

.. code-block:: python

                import rnlp
                import rnlp.corpus

                # Get a document from the built-in corpus
                declaration = rnlp.corpus.declaration()

                # Convert the document into a set of relational facts
                predicates = rnlp.parse(declaration)
"""

__author__ = 'Kaushik Roy (@kkroy36)'
__copyright__ = 'Copyright (c) 2017-2018 StARLinG Lab'
__license__ = 'GPL-v3'

__version__ = '0.2.1'
__status__ = 'Beta'
__maintainer__ = 'Alexander L. Hayes (@batflyer)'
__email__ = 'alexander.hayes@utdallas.edu'

__credits__ = [
    'Kaushik Roy (@kkroy36)',
    'Alexander L. Hayes (@batflyer)',
    'Sriraam Natarajan (@boost-starai)',
    'Gautam Kunapuli (@gkunapuli)',
    'Dileep Viswanathan',
    'Rahul Pasunuri'
]

from . import parse

from .textprocessing import getBlocks
from .textprocessing import getSentences

def converter(input_string, block_size=2):
    """
    The cli tool as a built-in function.

    :param input_string: A string that should be converted to a set of facts.
    :type input_string: str.
    :param blocks_size: Optional block size of sentences (Default: 2).
    :type block_size: int.
    """

    sentences = textprocessing.getSentences(input_string)
    blocks = textprocessing.getBlocks(sentences, block_size)
    parse.makeIdentifiers(blocks)
