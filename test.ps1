python -m pip install virtualenv
virtualenv.exe --always-copy venv
. venv/Scripts/activate
pip3 install -r requirements.txt
pip3 install -r dev-requirements.txt

python -m pylint -j 4 -r y forge
if($LastExitCode) { exit $LastExitCode}
python -m pytest -rf -vvv -x --count 5 --cov=forge --cov-fail-under=80 --cov-report term
if($LastExitCode) { exit $LastExitCode}