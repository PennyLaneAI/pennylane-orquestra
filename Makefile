PYTHON3 := $(shell which python3 2>/dev/null)

PYTHON := python3
COVERAGE := --cov=pennylane_orquestra --cov-report term-missing --cov-report=html:coverage_html_report
TESTRUNNER := -m pytest tests --tb=native --no-flaky-report
TESTRUNNERSTEPS := -m pytest steps/test_* --tb=native --no-flaky-report
PLUGIN_TESTRUNNER := pl-device-test --skip-ops --tb=native --no-flaky-report

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  install            to install PennyLane-Orquestra"
	@echo "  wheel              to build the PennyLane-Orquestra wheel"
	@echo "  dist               to package the source distribution"
	@echo "  clean              to delete all temporary, cache, and build files"
	@echo "  clean-docs         to delete all built documentation"
	@echo "  test               to run the unit tests without connecting to Orquestra"
	@echo "  test-e2e           to run the end-to-end tests that connect to Orquestra"
	@echo "  coverage           to generate a coverage report based on the unit tests"

.PHONY: install
install:
ifndef PYTHON3
	@echo "To install PennyLane-Orquestra you need to have Python 3 installed"
endif
	$(PYTHON) setup.py install

.PHONY: wheel
wheel:
	$(PYTHON) setup.py bdist_wheel

.PHONY: dist
dist:
	$(PYTHON) setup.py sdist

.PHONY : clean
clean:
	rm -rf pennylane_orquestra/__pycache__
	rm -rf tests/__pycache__
	rm -rf dist
	rm -rf build
	rm -rf .coverage coverage_html_report/
	rm -rf tmp
	rm -rf *.dat

docs:
	make -C doc html

.PHONY : clean-docs
clean-docs:
	rm -rf doc/code/api
	make -C doc clean

test:
	$(PYTHON) $(TESTRUNNER) -k 'not e2e'

test-e2e:
	$(PYTHON) $(TESTRUNNER) -k 'e2e'

test-steps:
	$(PYTHON) $(TESTRUNNERSTEPS)

coverage:
	@echo "Generating coverage report..."
	$(PYTHON) $(TESTRUNNER) $(COVERAGE) -k 'not e2e'

coverage-steps:
	@echo "Generating coverage report for the steps..."
	$(PYTHON) $(TESTRUNNERSTEPS) --cov=steps --cov-report term-missing --cov-report=html:coverage_html_report
