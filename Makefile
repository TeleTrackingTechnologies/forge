IMAGE_NAME='Forge'
PYTHON=python


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
	virtualenv --python=$(PYTHON) --always-copy .venv
	( \
    . .venv/bin/activate; \
    pip3 install -r requirements.txt; \
    pip3 install -e .; \
    )

dev: init
	( \
    . .venv/bin/activate; \
    pip3 install -r dev-requirements.txt; \
	pip3 install mypy==0.790; \
    )


lint: dev
	( \
    . .venv/bin/activate; \
    $(PYTHON) -m pylint -j 4 -r y forge; \
    )

type-check:
	( \
    . .venv/bin/activate; \
    $(PYTHON) -m mypy forge; \
    )

build:
	( \
	. .venv/bin/activate; \
	pip3 install --upgrade setuptools wheel; \
	$(PYTHON) setup.py sdist bdist_wheel; \
	)

test: lint type-check
	( \
    . .venv/bin/activate; \
	$(PYTHON) -m pytest -rf -vvv -x --count 5 --cov=forge --cov-fail-under=80 --cov-report term-missing; \
    )


clean:
	rm -rf forge.egg-info/ build/ dist/ .venv/ venv/ **/__pycache__/ .pytest_cache/ .coverage