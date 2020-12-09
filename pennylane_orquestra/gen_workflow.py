"""
This module contains utilities and auxiliary functions for generating Orquestra
workflows.
"""
# Backend import dictionaries used for generating Orquestra workflows

forest_import = {
    "name": "qe-forest",
    "type": "git",
    "parameters": {"repository": "git@github.com:zapatacomputing/qe-forest.git", "branch": "dev"},
}


qiskit_import = {
    "name": "qe-qiskit",
    "type": "git",
    "parameters": {"repository": "git@github.com:zapatacomputing/qe-qiskit.git", "branch": "dev"},
}

qulacs_import = {
    "name": "qe-qulacs",
    "type": "git",
    "parameters": {"repository": "git@github.com:zapatacomputing/qe-qulacs.git", "branch": "dev"},
}

backend_import_db = {
    "qe-forest": forest_import,
    "qe-qiskit": qiskit_import,
    "qe-qulacs": qulacs_import,
}


def step_dictionary(name_suffix):
    """Creates a new step with a pre-defined name suffixed with the name
    passed.

    Args:
        name_suffix (str): The name suffix to use, usually the index of the
            step. Such an index as suffix can be used for sorting the workflow
            steps (e.g., for batch execution for the Orquestra device).

    Returns:
        dict: the dictionary containing information for the step
    """
    name = "run-circuit-and-get-expval-" + name_suffix
    step_dict = {
        "name": name,
        "config": {
            "runtime": {
                "language": "python3",
                "imports": [
                    "pl_orquestra",
                    "z-quantum-core",
                    "qe-openfermion",
                    # Place to insert: step backend component import
                ],
                "parameters": {
                    "file": "pl_orquestra/steps/expval.py",
                    "function": "run_circuit_and_get_expval",
                },
            }
        },
        # Place to insert: inputs
        "outputs": [{"name": "expval", "type": "expval", "path": "/app/expval.json"}],
    }

    return step_dict


def gen_expval_workflow(component, backend_specs, circuits, operators, **kwargs):
    """Workflow template for computing the expectation value of operators
    given a quantum circuit and a device backend.

    Args:
        component (str): the name of the Orquestra component to use
        backend_specs (str): the Orquestra backend specifications as a json
            string
        circuits (list): list of OpenQASM 2.0 programs, each representing a
            circuit as an input for a workflow step
        operators (list): A list of json strings, each representing a list of
            operators as an input for a workflow step. Each operator is a string in
            an ``openfermion.QubitOperator`` or ``openfermion.IsingOperator``
            representation. For example, ``['["1 [Z0]", "1 [Z1]"]']`` is an
            input for a single step that returns the expectation value of two
            observables: ``Z0`` and ``Z1``.

    Keyword arguments:
        resources=None (str): the machine resources to use for executing the
            workflow

    Returns:
        dict: the dictionary that contains the workflow template to be
        submitted to Orquestra
    """
    backend_import = backend_import_db.get(component, None)
    if backend_import is None:
        raise ValueError("The specified backend component is not supported.")

    expval_template = {
        "apiVersion": "io.orquestra.workflow/1.0.0",
        "name": "expval",
        "imports": [
            {
                "name": "pl_orquestra",
                "type": "git",
                "parameters": {
                    "repository": "git@github.com:antalszava/pl_orquestra.git",
                    "branch": "master",
                },
            },
            {
                "name": "z-quantum-core",
                "type": "git",
                "parameters": {
                    "repository": "git@github.com:zapatacomputing/z-quantum-core.git",
                    "branch": "dev",
                },
            },
            {
                "name": "qe-openfermion",
                "type": "git",
                "parameters": {
                    "repository": "git@github.com:zapatacomputing/qe-openfermion.git",
                    "branch": "dev",
                },
            },
            # Place to insert: main backend import
        ],
        "steps": [],
        "types": ["circuit", "expval"],
    }

    # Insert the backend component to the main imports
    expval_template["imports"].append(backend_import)

    resources = kwargs.get("resources", None)

    for idx, (circ, ops) in enumerate(zip(circuits, operators)):
        new_step = step_dictionary(str(idx))
        expval_template["steps"].append(new_step)

        if resources is not None:
            # Insert the backend component to the import list of the step
            expval_template["steps"][idx]["config"]["resources"] = resources

        # Insert the backend component to the import list of the step
        expval_template["steps"][idx]["config"]["runtime"]["imports"].append(component)

        # Insert step inputs
        expval_template["steps"][idx]["inputs"] = []
        expval_template["steps"][idx]["inputs"].append(
            {"backend_specs": backend_specs, "type": "string"}
        )

        expval_template["steps"][idx]["inputs"].append({"operators": ops, "type": "string"})

        expval_template["steps"][idx]["inputs"].append({"circuit": circ, "type": "string"})
    return expval_template
