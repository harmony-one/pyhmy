CURRENT_SIGN_SETTING := $(shell git config commit.gpgSign)

.PHONY: clean-pyc clean-build

clean: clean-build clean-py

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-py:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '.pytest_cache' -exec rm -rf {} +

test:
	py.test tests

install:
	pip install -e .

release: clean
	python3 -m incremental.update pyhmy --rc
	python setup.py sdist bdist_wheel
	twine upload dist/*

sdist: clean
ifdef VERSION  # Argument for incremental, reference: https://pypi.org/project/incremental/ .
	python3 -m incremental.update pyhmy --$(VERSION)
else
	python3 -m incremental.update pyhmy --dev
endif
	python3 setup.py sdist bdist_wheel
	ls -l dist