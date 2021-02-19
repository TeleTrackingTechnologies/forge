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

> **Are you a ZSH User?** Zsh doesn't source `~/.profile`, use `~/.zprofile` instead

> **IMPORTANT:** Now reboot/logout to gain access to `pipx`

### **Windows**

Go to: https://gitforwindows.org/, then download and install latest git build

In PowerShell, running as administartor, run the following:

```shell
python -m pip install --user pipx
setx /m PIPX_HOME "~/.forge"
setx /m PIPX_BIN_DIR "~/.forge/bin"
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
#/home/USERNAME/.forge/bin/forge
# OR
where.exe forge
#C:\Users\USERNAME\.forge\bin\forge.exe
```

Then, to see the help interface:

```
$ forge -h
```

---

## Adding plugins

```
forge add -s SOURCE
forge add -s git+ssh://git@REPO_LINK
...
```

---

## Usage

```
forge <plugin-name> [plugin-arguments]
```

---

## Want to contribute to forge?

Fork this repo, then be sure to read our `CONTRIBUTING.md`

To install a specific branch/commit (suppose you've forked this repo, made changes and want to test your work):

```shell
pipx install git+https://github.com/GIT_USERNAME/forge@YOUR_BRANCH_NAME --force
pipx install git+https://github.com/GIT_USERNAME/forge@COMMIT_LONG_HASH_HERE --force
```

This is good way to share your work with others to test changes.

You can also use `pipx` to live edit locally:

- cd to a locally cloned version of forge
- `pipx install -e . --force`

This will install the local forge repo, any change you make in the repo will be reflected in the next run without having to update or reinstall

To revert back to the mainstream branch you will need to uninstall your local plugin first with either:

`pipx uninstall .`

Then follow the above section's install instructions. (`pipx install tele-forge`)
