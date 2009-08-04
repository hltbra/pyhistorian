all: install test

install:
	@python setup.py install

test:
	@echo
	@echo
	@python src/tests/run_tests.py && echo 'Ran tests succesfully'
