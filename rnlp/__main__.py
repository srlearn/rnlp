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
