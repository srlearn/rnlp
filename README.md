# NLP-Preprocessing
Processes text from a file or set of files into relational facts.

Pre-requisites: nltk version 3.2.1

Usage:
python parseInputCorpus.py -blockSize 'n'

The code will prompt for a file or folder input of text files to convert to relational facts.

The Relationals encoded are:
between block's of size n(i.e. 'n' sentences) and sentences in the blocks.
between sentences and words in the sentences.

The relationships currently encoded are:

1.earlySentenceInBlock - sentence occurs within a third of the block length

2.earlyWordInSentence - word occurs within a third of the sentence length

3.lateSentenceInBlock - sentence occurs after two-thirds of the block length

4.midWayWordInSentence - word occurs between a third and two-thirds of the block length

5.nextSentenceInBlock - sentence that follows a sentence in a block

6.nextWordInSentence - word that follows a word in a sentence in a block

7.sentenceInBlock - sentence occurs in a block

8.wordInSentence - word occurs in a sentence.

9.wordString - the string contained in the word.

More relationships are going to be included soon. such as part-of-speech tagging and named entity recognition
