all: install test

PYTHON=python

install:
	@$(PYTHON) setup.py install

test:
	@echo
	@echo
	@$(PYTHON) src/tests/run_tests.py && echo 'Ran tests succesfully' || echo 'Ran tests with failures'
