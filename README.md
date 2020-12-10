An approach for integrating PennyLane with Orquestra.

**Installation**

Installing [PennyLane](https://github.com/PennyLaneAI/pennylane) and the [Quantum Engine CLI](https://github.com/zapatacomputing/qe-cli) are required.

The package can be installed using `pip` and running `pip install -e .` from
the `pennylane_orquestra` folder.

**Folder structure**

*Server-side*

The `steps` folder contains the functions used in generated workflows as steps.
The `src` folder contains further server-side auxiliary code (if any).

*Client-side*

The `pennylane_orquestra` folder contains client-side code created as a
PennyLane plugin.
