.DEFAULT_GOAL := help

.PHONY: clean-tox
clean-tox:		## Remove tox testing artifacts
	@echo "+ $@"
	@rm -rf .tox/

.PHONY: clean-build
clean-build:	## Remove build artifacts
	@echo "+ $@"
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

.PHONY: clean-pyc
clean-pyc:		## Remove Python file artifacts
	@echo "+ $@"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: clean
clean: clean-tox clean-build clean-pyc ## Remove all file artifacts

.PHONY: lint
lint:			## Check code style with flake8
	@echo "+ $@"
	@tox -e flake8

.PHONY: test
test:			## Run tests quickly with the default Python
	@echo "+ $@"
	@tox -e py

.PHONY: test-all
test-all:		## Run tests on every Python version with tox
	@echo "+ $@"
	@tox

.PHONY: coverage
coverage:		## Check code coverage quickly with the default Python
	@echo "+ $@"
	@tox -e cov-report
	@$(BROWSER) htmlcov/index.html

.PHONY: docs
docs:			## Generate README.md
	@echo "TODO"

.PHONY: release
release: clean	## Package and upload release
	@echo "TODO"

.PHONY: sdist
sdist: clean	## Build sdist distribution
	@echo "+ $@"
	@python setup.py sdist
	@ls -l dist

.PHONY: wheel
wheel: clean	## Build bdist_wheel distribution
	@echo "+ $@"
	@python setup.py bdist_wheel
	@ls -l dist

.PHONY: help
help:			## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
