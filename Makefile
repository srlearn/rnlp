# Copyright © 2019 Alexander L. Hayes

.PHONY : distribution

distribution:
	pip install --upgrade setuptools wheel twine
	rm -rf dist/ rnlp.egg-info/ build/
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*
