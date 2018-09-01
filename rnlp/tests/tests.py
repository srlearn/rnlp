from rnlptests import *
import unittest

if __name__ == '__main__':
    """
    Testing module for ``rnlp``, to be ran from the base of the repository.

    .. code-block:: bash

                    python rnlp/tests/tests.py

    Verbosity may be explicitly set by passing an integer with the ``-v``
    flag. The value will be passed into the unittest.TextTestRunner, so
    integers higher than 1 will lead to more verbose outputs.

    .. code-block:: bash

                    python rnlp/tests/tests.py -v 2

    Individual modules may be tested with unittest via the command line.

    .. code-block:: bash

                    python -m unittest rnlp/tests/rnlptests/test_parse.py
                    ...
                    --------------------------------------------------
                    Ran 3 tests in 0.008s

                    OK
    """

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        default=1,
                        type=int)
    args = parser.parse_args()

    testsuite = unittest.TestLoader().discover('.')
    runner = unittest.TextTestRunner(verbosity=args.verbose)

    results = runner.run(testsuite)
    if results.failures or results.errors:
        raise(Exception('Encountered errors during runner.run'))
