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
    pip install -r requirements.txt; \
    )

lint: python-build

python-build:
	( \
    . .venv/bin/activate; \
    pylint -j 4 forge; \
    )

# test: init lint
# 	. venv/bin/activate; \
# 	coverage run -m unittest discover -s test/; \
# 	coverage report -m *.py;

install:
	mkdir -p /usr/local/etc/forge/plugins
	cp -r _internal_plugins/ /usr/local/etc/forge/plugins
	pip3 install -Ur requirements.txt
	cd ../; pip3 install .
