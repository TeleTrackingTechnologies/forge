# forge

There are many adjunct command line utilities that have been created by many [TeleTracking](https://www.teletracking.com)
employees to assist with their everyday activities.
The goal of this tool is to provide an extensible command line utility that will allow
for anyone to create new plugins for it that will be automatically pulled in by the
base tool when placed in the proper directory.

In order for a plugin to be used by the utility, a simple contract must be met and a requirements.txt containing all of the packages required by the plugin must be provided at the root directory of the plugin.
Each primary plugin file must have an execute method that accepts an array of args,
a helptext method that returns a very basic explanation of what the module does,
and a register method that accepts an instance of the app and passes the desired name of
the plugin, the execute method, and the value returned from the helptext method.

Example as follows shows what would represent the interface to a simple echo example.

```
def execute(args):
    print(args[0])


def helptext():
    return 'echoes the provided string'


def register(app):
    app.register_plugin('echo', execute, helptext())
```

## Pre-Requisites and Virtual Environments
Forge is a python package that utilizes many Python dependencies.

As such, it is highly recommended that you install and use forge within a Python virtual environment to avoid any potential issues with version requirements with your existing Python packages.

For those not familiar with using a virtual environment, the ability to initialize a simple one is provided within the Makefile of this repository.

In order to activate and use the included virtual environment, proceed with the following steps:

## Unix
```
$ make init
$ . .venv/bin/activate
```

You should see a visual representation on your command prompt that will indicate that you are within the virtual environment.
Anything installed while this virtual environment is active will only be available while you are within. Read more about Python virtual environments [here](https://realpython.com/python-virtual-environments-a-primer/).

You can leave the virtual environment at any time with the following command:
```
$ deactivate
```

## Installation
Once within your virtual environment, there are a number of ways that you can install the forge package.

### From Source
If you are already within the repository and using the included virtual environment, you can easily run another single make command in order to install forge from source:

```
$ make install
```

To verify your installation was successful:
```
$ which forge
```
should return the installed location of forge and:
```
$ forge
```
should return the simple help interface.

### Via PyPI

```
$ pip3 install tele-forge
```

To verify your installation was successful:
```
$ which forge
```
should return the installed location of forge and:
```
$ forge
```
should return the simple help interface.




## Usage
```
forge <plugin-name> [plugin-arguments]
```
