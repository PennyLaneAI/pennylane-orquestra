# Copyright 2020 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
import os

with open("pennylane_orquestra/_version.py") as f:
    version = f.readlines()[-1].split()[-1].strip("\"'")

requirements = ["pyyaml", "pennylane>=0.28"]

info = {
    'name': 'PennyLane-Orquestra',
    'version': version,
    'maintainer': 'Xanadu Inc.',
    'maintainer_email': 'software@xanadu.ai',
    'url': 'https://github.com/PennyLaneAI/pennylane-orquestra',
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
    'description': 'PennyLane plugin for Orquestra by Xanadu Inc.',
    'long_description': open('README.rst').read(),
    'long_description_content_type': 'text/x-rst',
    'provides': ['pennylane_orquestra'],
    'install_requires': requirements,
    'package_dir': {
        'pl_component': 'src/python',
        'pennylane_orquestra': 'pennylane_orquestra',
        }
}

classifiers = [
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
]

setup(classifiers=classifiers, **(info))
