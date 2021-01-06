""" Setup """
from setuptools import setup


with open('requirements.txt') as f:
    required_dependencies = f.read().splitlines()


setup(
    name='tele-forge',
    version="2.0.0",
    description='convenient cli with extendable collection of useful plugins',
    url='https://github.com/TeleTrackingTechnologies/forge',
    author=('Brandon Horn, Kenneth Poling, Paul Verardi, '
            'Cameron Tucker, Clint Wadley, Morgan Szafranski'),
    author_email='opensource@teletracking.com',
    license='MIT',
    packages=[
        'forge'
    ],
    install_requires=required_dependencies,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
    zip_safe=True,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'forge = forge:main'
        ]
    }
)
