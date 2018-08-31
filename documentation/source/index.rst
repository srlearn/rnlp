.. rnlp documentation master file, created by
   sphinx-quickstart on Thu May 17 10:12:50 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

``rnlp``
========

  *Relational NLP Preprocessing*: A Python package and tool for converting text
  into a set of relational facts.


  :Source Code: `GitHub <https://github.com/starling-lab/rnlp>`_
  :Bugtracker: `GitHub Issues <https://github.com/starling-lab/rnlp/issues/>`_

  .. image:: https://img.shields.io/pypi/pyversions/rnlp.svg?style=flat-square
  .. image:: https://img.shields.io/pypi/v/rnlp.svg?style=flat-square
  .. image:: https://img.shields.io/pypi/l/rnlp.svg?style=flat-square

Overview
--------

.. figure:: _static/gif/commandline.gif

  The U.S. Declaration of Independence is available in the corpus submodule for demonstration. Here it is converted to a set of facts using the imported Python package.

``rnlp`` is intended to be a general-purpose tool for converting text into relational facts for use with relational reasoning systems (such as `BoostSRL <https://starling.utdallas.edu/software/boostsrl/>`_).

Text is converted into relational facts, built around the basic building blocks of *Words*, *Sentences*, and *Blocks*.

*Words* are individual units of text, such as the words you are currently reading. *Sentences* are a collection of words, often separated by punctuation. *Blocks* are a collection of sentences.

.. toctree::
   :maxdepth: 1
   :caption: Getting Started:

   getting_started/01_environment
   getting_started/02_installation
   getting_started/03_quickstart

.. toctree::
   :maxdepth: 1
   :caption: API Reference:

   api/rnlp
   api/rnlp.parse
   api/rnlp.textprocessing
   api/rnlp.corpus
