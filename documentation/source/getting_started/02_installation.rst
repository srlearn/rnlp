============
Installation
============

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
