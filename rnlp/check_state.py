_err = (
    """
    >>> import nltk
    >>> nltk.download('punkt')
    >>> nltk.download('stopwords')
    >>> nltk.download('averaged_perceptron_tagger')

    Visit https://rnlp.readthedocs.io/en/latest/getting_started/02_installation.html
    for more information.
    """
)


def _ensure_nltk_installed():
    """
    Determine if `nltk` is installed.

    :raises: Exception if `nltk` is not installed.
    """
    try:
        import nltk
    except ModuleNotFoundError:
        raise Exception(
            "Unable to `import nltk` because it is not in the current environment."
            " Run `pip install nltk`, and then the following in an interpreter:\n"
            + _err
        ) from  None


def _find_nltk_module(module_name):
    """
    Determine whether a certain `nltk` module is installed.

    :param module_name: Name of a module within nltk
    :type module name: str.

    :raises: Exception if the module cannot be found
    """
    import nltk
    try:
        nltk.data.find(module_name)
    except LookupError as e:
        raise Exception(
            "Unable to find module '" + module_name + "'. Please run the following:\n"
            + _err
        ) from None


def ensure_nltk_setup():
    """Function to ensure required packages are installed."""
    _ensure_nltk_installed()
    nltk_modules = ("tokenizers/punkt", "corpora/stopwords", "taggers/averaged_perceptron_tagger")
    for nltk_module in nltk_modules:
        _find_nltk_module(nltk_module)
