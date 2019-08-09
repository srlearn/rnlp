########
``rnlp``
########

|PyPi|_ |License|_ |Travis|_ |Codecov|_ |ReadTheDocs|_

.. |PyPi| image:: https://img.shields.io/pypi/pyversions/rnlp.svg
  :alt: Python Package Index (PyPi) latest version.
.. _PyPi: https://pypi.org/project/rnlp/

.. |License| image:: https://img.shields.io/github/license/hayesall/rnlp.svg
  :alt: License.
.. _License: https://github.com/hayesall/rnlp/blob/master/LICENSE

.. |Travis| image:: https://travis-ci.org/hayesall/rnlp.svg?branch=master
  :alt: Master branch build status.
.. _Travis: https://travis-ci.org/hayesall/rnlp

.. |Codecov| image:: https://codecov.io/gh/hayesall/rnlp/branch/master/graphs/badge.svg?branch=master
  :alt: Master branch code coverage.
.. _Codecov: https://codecov.io/github/hayesall/rnlp?branch=master

.. |ReadTheDocs| image:: https://readthedocs.org/projects/rnlp/badge/?version=latest
  :alt: Documentation build status and link to documentation.
.. _ReadTheDocs: http://rnlp.readthedocs.io/en/latest/

Relational NLP Preprocessing (**rnlp**): A Python package and tool for converting text into a set of relational facts.

- **Documentation**: https://rnlp.readthedocs.io/en/latest/
- **Questions?**: Contact `Alexander L. Hayes (hayesall) <https://hayesall.com>`_

Installation
------------

Stable builds on PyPi

.. code-block:: bash

		pip install rnlp

Quick-Start
-----------

``rnlp`` can be used either as a command line interface (CLI) tool or as an imported Python Package.

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

The relations created by ``rnlp`` include the following:

* Sentence's Relative Position in Block:

  * ``earlySentenceInBlock``: Sentence occurs within the first third of a block.
  * ``midWaySentenceInBlock``: Sentence occurs between the first third and the last third of a block's length.
  * ``lateSentenceInBlock``: Sentence occurs within the last third of a block's length.

* Word's Relative Position in Sentence:

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
  * ``partOfSpeechTag``: The word's part of speech (as determined by the nltk part-of-speech tagger).

---

Files contain a toy corpus (``example files/``) and an image of a BoostSRL tree for predicting if a word in a sentence is the word "you".

.. image:: https://raw.githubusercontent.com/hayesall/rnlp/master/documentation/img/output.png

The tree says that if the word string contained in word 'b' is "you" then 'b' is the word "you" with a high probability. (This is of course true).
A more interesting inference is the False branch that says that if word 'b' is an early word in sentence 'a' and word 'anon12035' is also an early word in sentence 'a' and if the word string contained in word 'anon12035' is "Thank", then the word 'b' has decent chance of being the word "you". (The model was able to learn that the word "you" often occurs with the word "Thank" in the same sentence when "Thank" appears early in that sentence).
