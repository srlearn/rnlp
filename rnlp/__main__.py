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

from parse import *

import argparse

__author__ = 'Kaushik Roy (@kkroy36)'
__copyright__ = 'Copyright (c) 2017-2018 StARLinG Lab'
__license__ = 'GPL-v3'

__version__ = '0.1.0'
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

parser = argparse.ArgumentParser(
    description='''Relational-NLP: A library and tool for converting text
                   into a set of relational facts.''',
    epilog='''Copyright (c) 2017-2018 StARLinG Lab.'''
)

parser.add_argument('-b', '--blockSize', type=int,
    help='Set the block size')
parser.add_argument('-f', '--file', type=str, default=2,
    help='Read from file.')

args = parser.parse_args()

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

main()
