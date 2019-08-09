"""
Setup file for rnlp
"""

from setuptools import setup, find_packages
from setuptools.command.install import install as _install

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README.md
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


# https://stackoverflow.com/questions/26799894/installing-nltk-data-in-setup-py-script
class Install(_install):
    """
    Overwriting the base class to additionally install nltk packages.
    """

    def run(self):
        _install.do_egg_install(self)

        # Install the additional required nltk packages
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')


setup(
    name='rnlp',
    version='0.3.2',
    license='GPL-v3',

    description='Converts text corpora into a set of relational facts.',
    long_description=long_description,

    url='https://github.com/hayesall/rnlp',

    author='Alexander L. Hayes (@hayesall)',
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
        'Source': 'https://github.com/hayesall/rnlp',
        'Tracker': 'https://github.com/hayesall/rnlp/issues'
    },

    packages=find_packages(exclude=['tests']),

    cmdclass={'install': Install},

    install_requires=[
        'nltk',
        'tqdm',
        'joblib'
    ],

    setup_requires=['nltk']
)
