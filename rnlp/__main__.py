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
Main script for rnlp.

.. code-block:: bash

    $ python -m rnlp --help
"""

import argparse
import logging

from .parse import makeIdentifiers
from .textprocessing import getSentences
from .textprocessing import getBlocks
from .corpus import readCorpus

from ._meta import __license__, __version__, __copyright__

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

LOG_HANDLER = logging.FileHandler("rnlp_log.log")
LOG_HANDLER.setLevel(logging.INFO)
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(LOG_HANDLER)
LOGGER.info("Started logger.")

LOGGER.info("Started Argument Parser.")
PARSER = argparse.ArgumentParser(
    description="rnlp (v{0}): Convert text into relational facts.".format(__version__),
    epilog="This program is free software under the {0}. {1}".format(
        __license__, __copyright__
    ),
)

FILE_OR_DIR = PARSER.add_mutually_exclusive_group()

PARSER.add_argument("-b", "--blockSize", type=int, default=2, help="Set the block size")
FILE_OR_DIR.add_argument(
    "-d", "--directory", type=str, help="Read all .txt files in directory"
)
FILE_OR_DIR.add_argument("-f", "--file", type=str, help="Read from one .txt file")

ARGS = PARSER.parse_args()
LOGGER.info("Argument Parsing Successful.")

N_BLOCKS = ARGS.blockSize
LOGGER.info("blockSize specified as %s", N_BLOCKS)

if ARGS.file:
    CHOSEN_FILE = ARGS.file
elif ARGS.directory:
    CHOSEN_FILE = ARGS.directory
else:
    ERROR_MESSAGE = "Error. No file or directory was specified."
    LOGGER.error(ERROR_MESSAGE)
    print(ERROR_MESSAGE)
    exit(1)

CORPUS = readCorpus(CHOSEN_FILE)
SENTENCES = getSentences(CORPUS)
BLOCKS = getBlocks(SENTENCES, N_BLOCKS)
makeIdentifiers(BLOCKS)

LOGGER.info("Reached bottom of %s.", __name__)
LOGGER.info("Shutting down logger.")
logging.shutdown()
exit(0)
