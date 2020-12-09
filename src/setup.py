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
    description="The PennyLane component on Orquestra",
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
