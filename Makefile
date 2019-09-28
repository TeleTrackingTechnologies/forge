IMAGE_NAME='Forge'
BUILD=1
VERSION=0.1.$(BUILD)

.DEFAULT: help
help:
	@echo "make init"
	@echo "   prepare development environment and create virtualenv"
	@echo "make test"
	@echo "   run lint, pytype and unit tests"
	@echo "make lint"
	@echo "   run lint and pytype only"
	@echo "make clean"
	@echo "   clean compiled files and the virtual environment"

init:
	rm -rf .venv
	virtualenv --python=python3 --always-copy .venv
	( \
    . .venv/bin/activate; \
    pip3 install -r requirements.txt; \
    )

lint: python-build

python-build:
	( \
    . .venv/bin/activate; \
    pylint -j 4 --rcfile=pylintrc forge; \
    )

install:
	( \
	pip3 install -Ur requirements.txt; \
	pip3 install .; \
    )

test:
	python -m unittest discover -s forge -p '*_test.py'