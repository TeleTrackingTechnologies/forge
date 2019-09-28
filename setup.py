from setuptools import setup

setup(name='forge',
      version='0.1',
      description='convenient cli with extendable collection of useful plugins',
      author='Brandon Horn, Kenneth Poling, Paul Verardi, Cameron Tucker, Clint Wadley',
      packages=['forge', 'forge.config', 'forge._internal_plugins', 'forge._internal_plugins.manage_plugins', 'forge._internal_plugins.manage_plugins.manage_plugins_logic'],
      install_requires=[
            "boto3==1.9.122",
            "botocore==1.12.122",
            "colorama==0.4.1",
            "docutils==0.14",
            "jmespath==0.9.4",
            "nested-lookup==0.2.12",
            "pluginbase==1.0.0",
            "python-dateutil==2.8.0",
            "python-slugify==3.0.1",
            "requests==2.21.0",
            "s3transfer==0.2.0",
            "six==1.12.0",
            "tabulate==0.8.3",
            "urllib3==1.25.3",
            'jsonschema==3.0.1',
            'strict-rfc3339==0.7',
            'pyjwt==1.7.1',
            'cryptography==2.3'
      ],
      scripts=['bin/forge'],
      zip_safe=False)
