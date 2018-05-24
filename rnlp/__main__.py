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

from .parse import *
from .corpus import readCorpus

import argparse
import logging

# === Metadata === #

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

# === Logging === #

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_handler = logging.FileHandler('rnlp_log.log')
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)
logger.info('Started logger.')

# === Argument Parser === #

logger.info('Started Argument Parser.')
parser = argparse.ArgumentParser(
    description='''Relational-NLP: A library and tool for converting text
                   into a set of relational facts.''',
    epilog='''Copyright (c) 2017-2018 StARLinG Lab.'''
)

file_or_dir = parser.add_mutually_exclusive_group()

parser.add_argument('-b', '--blockSize', type=int, default=2,
    help='Set the block size')
file_or_dir.add_argument('-d', '--directory', type=str,
    help='Read text from all files in a directory.')
file_or_dir.add_argument('-f', '--file', type=str,
    help='Read from text from a file.')

args = parser.parse_args()
logger.info('Argument Parsing Successful.')

# Set block size.
n = args.blockSize
logger.info('blockSize specified as ' + str(n))

# Set the input file(s).
if args.file:
    chosenFile = args.file
elif args.directory:
    chosenFile = args.directory
else:
    message = 'Error. No file or directory was specified.'
    logger.error(message)
    print(message)
    exit(1)

# Read the corpus.
try:
    corpus = readCorpus(chosenFile)
except Exception:
    logger.error('Error while reading corpus.', exc_info=True)
    exit(2)

# Get sentences from the corpus.
try:
    sentences = getSentences(corpus)
except Exception:
    logger.error('Error getting sentences from corpus', exc_info=True)
    exit(2)

# Create blocks from the sentences.
try:
    blocks = getBlocks(sentences, n)
except Exception:
    logger.error('Error while creating blocks', exc_info=True)
    exit(2)

# Make identifiers from the blocks.
try:
    makeIdentifiers(blocks)
except Exception:
    logger.error('Error while making identifiers.', exc_info=True)
    exit(2)

logger.info('Reached bottom of ' + __name__ + '.')
logger.info('Shutting down logger.')
logging.shutdown()
exit(0)
