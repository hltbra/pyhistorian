all: install test

PYTHON=python

install:
	@$(PYTHON) setup.py install

test:
	@echo
	@echo
	@$(PYTHON) src/specs/run_specs.py && echo 'Ran specs succesfully' || echo 'Ran specs with failures'
