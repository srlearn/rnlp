"""
Setup file for rnlp
"""

from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install as _install

from codecs import open
from os import path

# Get __version__, __license__ and others from _meta.py
with open(path.join("rnlp", "_meta.py")) as f:
    exec(f.read())

here = path.abspath(path.dirname(__file__))

# Get the long description from the README.md
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
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

        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download("averaged_perceptron_tagger")


setup(
    name="rnlp",
    version=__version__,
    license=__license__,
    description="Converts text corpora into a set of relational facts.",
    long_description=long_description,
    url="https://github.com/hayesall/rnlp",
    author=__author__,
    author_email=__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="nlp",
    project_urls={
        "Source": "https://github.com/hayesall/rnlp",
        "Tracker": "https://github.com/hayesall/rnlp/issues",
    },
    packages=find_packages(exclude=["tests"]),
    cmdclass={"install": Install},
    install_requires=["nltk", "tqdm", "joblib"],
    setup_requires=["nltk"],
)
