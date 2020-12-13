if (test-path venv) {
    Remove-Item venv -Recurse -Force
}
python -m pip install virtualenv
virtualenv --always-copy venv
. venv/Scripts/activate
pip3 install -r requirements.txt

$version = (Get-Content setup.py | Select-String "version='(\d+\.\d+\.\d+)'" | Select-Object Matches -First 1).Matches.Groups[1].Value

python -m pip install --upgrade setuptools wheel
python setup.py sdist bdist_wheel
python -m pip install dist/tele_forge-$version-py3-none-any.whl
forge