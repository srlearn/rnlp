"""
Setup file for rnlp
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README.md
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# rnlp needs a few additional nltk packages to function properly.
import nltk
nltk.download('punkt')
nltk.download('stopwords')
#nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Import the package and assign metadata as appropriate
import rnlp

setup(
    name='rnlp',
    version=rnlp.__version__,
    license=rnlp.__license__,

    description='Converts text corpora into a set of relational facts.',
    long_description=long_description,

    url='https://github.com/starling-lab/rnlp',

    author='Alexander L. Hayes (@batflyer)',
    author_email='alexander@batflyer.net',

    classifiers=[
        # Development Information
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Intended primarily for research use
        'Intended Audience :: Science/Research',

        # Tested Operating Systems
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',

        # Supported Python Versions.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

    keywords='nlp',

    project_urls={
        'Source': 'https://github.com/starling-lab/rnlp',
        'Tracker': 'https://github.com/starling-lab/rnlp/issues'
    },

    packages=find_packages(exclude=['tests'])
)
