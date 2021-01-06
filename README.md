# **forge**

There are many adjunct command line utilities that have been created by many [TeleTracking](https://www.teletracking.com)
employees to assist with their everyday activities.
The goal of this tool is to provide an extensible command line utility that will allow
for anyone to create new plugins accessible

---

## Pre-Requisites

- Forge is a python package that utilizes many Python dependencies.

- Forge and its plugins uses pipx to isolate dependencies and make self contained globally available executables.

- If you haven't used Python before, you'll need to [install Python 3](https://docs.python-guide.org/starting/installation/) first. (If you're on a Mac, avoid using the default Python installation.)

- You will also need access to `git`.

### **Unix**

```shell
$ apt-get -y install python3-pip
$ apt-get -y install python3-venv
$ apt-get -y install git
$ python3 -m pip install --user pipx
$ echo 'export PIPX_HOME="$HOME/.forge"' >> ~/.profile
$ echo 'export PIPX_BIN_DIR="$HOME/.forge/bin"' >> ~/.profile
$ python3 -m pipx ensurepath
```

> **IMPORTANT:** Now reboot/logout to gain access to `pipx`

### **Windows**

Go to: https://gitforwindows.org/, then download and install latest git build

In PowerShell, running as administartor, run the following:

```shell
python -m pip install --user pipx
$env:PIPX_HOME="~/.forge"
$env:PIPX_BIN_DIR="~/.forge/bin"
python -m pipx ensurepath --force
```

> **IMPORTANT:** Now reboot/logout to gain access to `pipx`

---

## Installation

### **Via PyPI**

```shell
$ pipx install tele-forge
```

### **From VCS**

```shell
$ pipx install git+https://git@github.com/TeleTrackingTechnologies/forge
```

### **From Source (after cloning)**

```shell
$ pipx install .
# OR as editable for developing forge changes
$ pipx install -e .
```

---

## Post Install

To verify your installation was successful

```shell
$ which forge
# OR
where.exe forge
```

should return the installed location of forge, then:

```
$ forge -h
```

should return the simple help interface.

---

## Usage

```
forge <plugin-name> [plugin-arguments]
```
