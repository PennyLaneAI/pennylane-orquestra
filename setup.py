from setuptools import setup, find_packages
import os

with open("pennylane_orquestra/_version.py") as f:
    version = f.readlines()[-1].split()[-1].strip("\"'")

requirements = ["pyyaml", "pennylane>=0.11"]

info = {
    'name': 'PennyLane-Orquestra',
    'version': version,
    'author': 'Antal Szava',
    'author_email': 'antalszava@gmail.com',
    'url': 'https://github.com/antalszava/pl_orquestra',
    'packages': [
        'pl_component',
        'pennylane_orquestra',
    ],
    'entry_points': {
        'pennylane.plugins': [
            'orquestra.qiskit = pennylane_orquestra:QeQiskitDevice',
            'orquestra.ibmq = pennylane_orquestra:QeIBMQDevice',
            'orquestra.qulacs = pennylane_orquestra:QeQulacsDevice',
            'orquestra.forest = pennylane_orquestra:QeForestDevice',
            ]
    },
    'description': 'PennyLane is a Python quantum machine learning library by Xanadu Inc.',
    'long_description': open('README.md').read(),
    'long_description_content_type': 'text/x-rst',
    'provides': ['pennylane'],
    'install_requires': requirements,
    'package_dir': {
        'pl_component': 'src/python',
        'pennylane_orquestra': '',
        }
}

classifiers = [
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
]

setup(classifiers=classifiers, **(info))
