.PHONY: clean clean-py clean-build

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-py - remove Python file artifacts"
	@echo "install - install the library locally"
	@echo "test - run full test suite"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-py

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr .eggs/

clean-py:
	rm -fr .pytest_cache/
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

dev:
	python3 -m pip install pyhmy[dev]

test:
	python3 -m pytest -r s -s tests

install:
	python3 -m pip install -e .

release: clean
	python3 -m build
	twine upload dist/*

sdist: clean
	python3 -m build
	ls -l dist
