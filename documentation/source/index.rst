.. rnlp documentation master file, created by
   sphinx-quickstart on Thu May 17 10:12:50 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

``rnlp``
========

  *Relational NLP Preprocessing*: A Python package and tool for converting text
  into a set of relational facts.

  :Authors:
    Kaushik Roy (`@kkroy36 <https://github.com/kkroy36/>`_), Alexander L. Hayes (`@batflyer <https://github.com/batflyer/>`_)

  :Index: :ref:`genindex`
  :Modules: :ref:`modindex`
  :Source: `GitHub <https://github.com/starling-lab/rnlp>`_
  :Bugtracker: `GitHub Issues <https://github.com/starling-lab/rnlp/issues/>`_

  .. image:: https://img.shields.io/pypi/pyversions/rnlp.svg?style=flat-square
  .. image:: https://img.shields.io/pypi/v/rnlp.svg?style=flat-square
  .. image:: https://img.shields.io/pypi/l/rnlp.svg?style=flat-square
  .. image:: https://img.shields.io/readthedocs/rnlp/stable.svg?flat-square
	   :target: http://rnlp.readthedocs.io/en/stable/

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Installation
------------

Stable builds on PyPi

.. code-block:: bash

		pip install rnlp

Development builds on GitHub

.. code-block:: bash

		pip install git+git://github.com/starling-lab/rnlp.git

Some modules in nltk need to be available:

.. code-block:: bash
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        
Quick-Start
-----------

``rnlp`` can be used either as a CLI tool or as an imported Python Package.

+---------------------------------------------+--------------------------------------+
| **CLI**                                     | **Imported**                         |
+---------------------------------------------+--------------------------------------+
|.. code-block:: bash                         |.. code-block:: python                |
|                                             |                                      |
|  $ python -m rnlp -f example_files/doi.txt  |  from rnlp.corpus import declaration |
|  Reading corpus from file(s)...             |  import rnlp                         |
|  Creating background file...                |                                      |
|  100%|████████| 18/18 [00:00<00:00, 38it/s] |  doi = declaration()                 |
|                                             |  rnlp.converter(doi)                 |
+---------------------------------------------+--------------------------------------+

Text will be converted into relational facts, relations encoded are:

- between blocks of size 'n' (i.e. 2 sentences) in the blocks.

- between block's of size n (i.e. 'n' sentences) and sentences in the blocks.

- between sentences and words in the sentences.

---

The relationships currently encoded are:

1. earlySentenceInBlock - sentence occurs within a third of the block length

2. earlyWordInSentence - word occurs within a third of the sentence length

3. lateSentenceInBlock - sentence occurs after two-thirds of the block length

4. midWayWordInSentence - word occurs between a third and two-thirds of the block length

5. nextSentenceInBlock - sentence that follows a sentence in a block

6. nextWordInSentence - word that follows a word in a sentence in a block

7. sentenceInBlock - sentence occurs in a block

8. wordInSentence - word occurs in a sentence.

9. wordString - the string contained in the word.

10. partOfSpeech - the part of speech of the word.

---

Files contain a toy corpus (``files/``) and an image of a BoostSRL tree for predicting if a word in a sentence is the word "you".

.. image:: https://raw.githubusercontent.com/starling-lab/rnlp/master/documentation/img/output.png

The tree says that if the word string contained in word 'b' is "you" then 'b' is the word "you". (This is of course true).
A more interesting inference is the False branch that says that if word 'b' is an early word in sentence 'a' and word 'anon12035' is also an early word in sentence 'a' and if the word string contained in word 'anon12035' is "Thank", then the word 'b' has decent change of being the word "you". (The model was able to learn that the word "you" often occurs with the word "Thank" in the same sentence when "Thank" appears early in that sentence).

 .. _`@kkroy36`: https://github.com/kkroy36/
 .. _`@batflyer`: https://github.com/batflyer/
