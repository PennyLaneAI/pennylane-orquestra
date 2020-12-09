An approach for integrating PennyLane with Orquestra.

**Installation**

Installing [PennyLane](https://github.com/PennyLaneAI/pennylane) and the [qe-cli](https://github.com/zapatacomputing/qe-cli) are required.

The package can be installed using `pip` and running `pip install -e .` from
the `pl_orquestra` folder.

**Folder structure**

*Server-side*

The `steps` folder contains the functions used in generated workflows as steps.

*Client-side*

The `pennylane_orquestra` folder contains client-side code created as a
PennyLane plugin.

**Supported Orquestra backends**

The following Orquestra backends are supported at the moment:

* `QiskitSimulator`: `"orquestra.qiskit"`
* `ForestSimulator`: `"orquestra.forest"`
* `QulacsSimulator`: `"orquestra.qulacs"`
* `IBMQBackend`: `"orquestra.ibmq"`

The `backend` option can be passed as a keyword argument to the
`qml.device` PennyLane function (see example).

**Examples**

Examples can be run after authentication using the `qe` command-line tool happened.

*Using `QulacsSimulator`*

```python
import pennylane as qml

dev = qml.device('orquestra.qulacs', wires=3, analytic=True, keep_files=True)

@qml.qnode(dev)
def circuit():
    qml.PauliX(0)
    return qml.expval(qml.PauliZ(0))

circuit()
```
```
-1
```

*Using `QiskitSimulator` with the `statevector_simulator`*

```python
import pennylane as qml

dev = qml.device('orquestra.qiskit', wires=3, backend='statevector_simulator', analytic=True, keep_files=True)

@qml.qnode(dev)
def circuit():
    qml.PauliX(0)
    return qml.expval(qml.PauliZ(0)), qml.expval(qml.PauliZ(1))

circuit()
```
```
array([-1, 1])
```
