===========
Quick Start
===========

Relations
---------

The relations created by ``rnlp`` include the following:

  * Sentence’s Relative Position in Block:

    * ``earlySentenceInBlock``: Sentence occurs within the first third of a block’s length.
    * ``midWaySentenceInBlock``: Sentence occurs between the first and last third of a block’s length.
    * ``lateSentenceInBlock``: Sentence occurs within the last third of a block’s length.

  * Word’s Relative Position in Sentence:

    * ``earlyWordInSentence``: Word occurs within the first third of a sentence.
    * ``midWayWordInSentence``: Word occurs between a third and two-thirds of a sentence.
    * ``lateWordInSentence``: Word occurs within the last third of a sentence.

  * Relative Position Between Items:

    * ``nextWordInSentence``: Pointer from a word to its neighbor.
    * ``nextSentenceInBlock``: Pointer from a sentence to its neighbor.

  * Existential Semantics:

    * ``sentenceInBlock``: Sentence occurs in a particular block.
    * ``wordInSentence``: Word occurs in a particular sentence.

  * Low-Level Information about words:

    * ``wordString``: A string representation of a word.
    * ``partOfSpeechTag``: The word’s part of speech.

From text to Relational Facts
-----------------------------

Consider the example file ``example_files/doi.txt``, the U.S. Declaration of Independence:

.. code-block:: text

    In Congress, July 4, 1776. The unanimous Declaration of the thirteen united
    States of America, When in the Course of human events, it becomes necessary
    for one people to dissolve the political bands which have connected them
    with another, and to assume among the powers of the earth, the separate and
    equal station to which the Laws of Nature and of Nature's God entitle them,
    a decent respect to the opinions of mankind requires that they should
    declare the causes which impel them to the separation.
    ...
    ...

``rnlp`` can be used either as a commandline tool or as an imported Python Package.

**Commandline**

.. code-block:: bash

  $ python -m rnlp -f example_files/doi.txt
  Reading corpus from file(s)...
  Creating background file...
  100%|████████| 18/18 [00:00<00:00, 38it/s]

**Imported**

.. code-block:: python

  from rnlp.corpus import declaration
  import rnlp

  doi = declaration()
  rnlp.converter(doi)


.. code-block:: prolog

    nextSentenceInBlock(1,1_1,1_2).
    earlySentenceInBlock(1,1_1).
    sentenceInBlock(1_1,1).
    wordString(1_1_1,'In').
    partOfSpeech(1_1_1,"IN").
    nextWordInSentence(1_1,1_1_1,1_1_2).
    earlyWordInSentence(1_1,1_1_1).
    wordInSentence(1_1_1,1_1).
    wordString(1_1_2,'Congress').
    partOfSpeech(1_1_2,"NNP").
    ...
    ...
