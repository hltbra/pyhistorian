all: install test

PYTHON=python

clean:
	rm -rf dist build *egg-info

install: clean
	@$(PYTHON) setup.py install

test:
	@echo
	@echo
	@$(PYTHON) specs/run_specs.py && echo 'Ran specs succesfully' || echo 'Ran specs with failures'
