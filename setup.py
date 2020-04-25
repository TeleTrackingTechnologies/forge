""" Setup """
from setuptools import setup
from pathlib import Path

setup(name='tele-forge',
      version='0.0.2',
      description='convenient cli with extendable collection of useful plugins',
      url='https://github.com/TeleTrackingTechnologies/forge',
      author='Brandon Horn, Kenneth Poling, Paul Verardi, Cameron Tucker, Clint Wadley',
      author_email='opensource@teletracking.com',
      packages=[
          'forge',
          'forge.config',
          'forge._internal_plugins',
          'forge._internal_plugins.manage_plugins',
          'forge._internal_plugins.manage_plugins.manage_plugins_logic'
      ],
      install_requires=[
          'colorama',
          'GitPython',
          'pluginbase',
          'requests',
          'tabulate'
      ],
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent'
      ],
      python_requires='>=3.7',
      scripts=['bin/forge'],
      zip_safe=False
      )
