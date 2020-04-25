IMAGE_NAME='Forge'
VERSION=0.0.1

.DEFAULT: help
help:
	@echo "make init"
	@echo "   prepare development environment and create virtualenv"
	@echo "make test"
	@echo "   run lint, pytype and unit tests"
	@echo "make lint"
	@echo "   run lint and pytype only"
	@echo "make build"
	@echo "   run lint, test, and build package"
	@echo "make clean"
	@echo "   clean compiled files and the virtual environment"
	@echo "\n"
	@echo "For Development:"
	@echo "make install"
	@echo "   installs package from source"

init:
	rm -rf .venv
	pip3 install virtualenv
	virtualenv --python=python3 --always-copy .venv
	( \
    . .venv/bin/activate; \
    pip3 install -r requirements.txt; \
    )

lint:
	( \
    . .venv/bin/activate; \
    pylint -j 4 --rcfile=pylintrc forge; \
    )

build:
	( \
	pip3 install --upgrade setuptools wheel; \
	python3 setup.py sdist bdist_wheel; \
	)

install: build
	( \
	pip3 install dist/forge-${VERSION}-py3-none-any.whl; \
    )

test:
	python -m unittest discover -s forge -p '*_test.py'

clean:
	rm -rf forge.egg-info/ build/ dist/ .venv/

type-check:
	pytype *.py forge/*.py