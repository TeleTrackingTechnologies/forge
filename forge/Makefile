init: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv -p python3 venv
	. venv/bin/activate; pip install -Ur requirements.txt

test: init lint
	. venv/bin/activate; \
	coverage run -m unittest discover -s test/; \
	coverage report -m *.py;

install:
	mkdir -p /usr/local/etc/forge/plugins
	cp -r _internal/ /usr/local/etc/forge/plugins
	pip3 install -Ur requirements.txt
	cd ../; pip3 install .
