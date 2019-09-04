# forge

There are many adjunct command line utilities that have been created by many Teletracking
employees to assist with their everyday activities.
The goal of this tool is to provide an extensible command line utility that will allow
for anyone to create new plugins for it that will be automatically pulled in by the 
base tool when placed in the proper directory.

In order for a plugin to be used by the utility, a few requirements must be met.
Each primary plugin file must have an execute method that accepts an array of args,
a helptext method that returns a very basic explanation of what the module does, 
and a register method that accepts an instance of the app and passes the desired name of
the plugin, the execute method, and the value returned from the helptext method.

Example as follows shows what is contained in the echo.py example.

```
def execute(args):
    print(args[0])


def helptext():
    return 'echoes the provided string'


def register(app):
    app.register_plugin('echo', execute, helptext())
```

## Installation
### Via Brew
```
// TODO: Update install instructions
```
### From Code
```
cd forge 
make install
```

## Usage
```
forge <plugin-name> [plugin-arguments]
```