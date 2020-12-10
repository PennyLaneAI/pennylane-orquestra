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

import setuptools	
import os	

readme_path = os.path.join("..", "README.md")	
with open(readme_path, "r") as f:	
    long_description = f.read()	


setuptools.setup(	
    name="pl_orquestra",	
    version="0.0.1",	
    maintainer="Xanadu Inc.",
    maintainer_email="software@xanadu.ai",
    description="The PennyLane component for the PennyLane-Orquestra plugin",
    long_description=long_description,	
    long_description_content_type="text/markdown",	
    url="https://github.com/PennyLaneAI/pennylane-orquestra",
    packages=setuptools.find_packages(where="src/python"),	
    package_dir={"": "python"},	
    classifiers=(	
        "Programming Language :: Python :: 3",	
        "Operating System :: OS Independent",	
    ),	
    install_requires=[	
        "qiskit==0.18.3",	
        "qiskit-ibmq-provider==0.6.1",	
        "pyquil==2.17.0",	
        "numpy>=1.18.1",	
    ],	
)
