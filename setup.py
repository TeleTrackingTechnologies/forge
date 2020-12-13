""" Setup """
from setuptools import setup
setup(name='tele-forge',
      version='1.0.1',
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
          'colorama==0.4.4',
          'GitPython==3.1.1',
          'pluginbase==1.0.0',
          'requests==2.25.0',
          'tabulate==0.8.7',
          'halo==0.0.31'
      ],
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent'
      ],
      python_requires='>=3.7',
      scripts=[
          'bin/forge',
          'bin/forge.bat'],
      zip_safe=False
      )
