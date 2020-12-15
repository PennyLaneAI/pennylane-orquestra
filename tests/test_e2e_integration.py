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
"""
End-to-end integration tests between the local machine and the remote Orquestra
platform.

These test cases connect to the Orquestra platform. Prior authentication to the
Orquestra platform is required for running them. The roundtrip time can be 1-2
minutes for test cases including assertions on the output of the computation.
"""
import pytest
import numpy as np
import math
import yaml
import os

import pennylane as qml
from pennylane_orquestra import OrquestraDevice, QeQiskitDevice, QeIBMQDevice
import pennylane_orquestra.gen_workflow as gw
from pennylane_orquestra.cli_actions import qe_submit, workflow_details

from qiskit import IBMQ

from conftest import (
    qe_list_workflow,
    backend_specs_default,
    operator_string_default,
    qasm_circuit_default,
    resources_default,
)

qiskit_analytic_specs = '{"module_name": "qeqiskit.simulator", "function_name": "QiskitSimulator", "device_name": "qasm_simulator"}'
qiskit_sampler_specs = '{"module_name": "qeqiskit.simulator", "function_name": "QiskitSimulator", "device_name": "qasm_simulator", "n_samples": 1000}'

analytic_tol = 10e-10

# The tolerance for sampling is expected to be higher
tol = 10e-2

class TestWorkflowSubmissionIntegration:
    """Test that workflow generation works as expected."""

    @pytest.mark.parametrize("resources", [None, resources_default])
    def test_can_submit_and_query_workflow_details(self, resources, tmpdir):
        """Test that filling in the workflow template for getting expectation
        values can be submitted to Orquestra and workflow details can be queried."""
        # Skip if not logged in to Orquestra
        try_resp = qe_list_workflow()
        need_login_msg = "token has expired, please log in again\n"

        if need_login_msg in try_resp:
            pytest.skip("Has not logged in to the Orquestra platform.")

        backend_component = "qe-forest"
        op = ['["[Z0]"]']
        circuits = [qasm_circuit_default]

        # Fill in workflow template
        workflow = gw.gen_expval_workflow(
            backend_component, backend_specs_default, circuits, op, resources=resources
        )
        file_name = tmpdir.join("test_workflow.yaml")

        with open(file_name, "w") as file:
            d = yaml.dump(workflow, file)

        # Submit a workflow
        workflow_id = qe_submit(file_name)

        workflow_msg = workflow_details(workflow_id)
        details_string = "".join(workflow_msg)
        assert workflow_id in details_string

    @pytest.mark.parametrize("backend_component", list(gw.backend_import_db.keys()))
    def test_submit_raises(self, backend_component, tmpdir):
        """Test that submitting a workflow to Orquestra with invalid
        requirements raises an error."""
        # Skip if not logged in to Orquestra
        try_resp = qe_list_workflow()
        need_login_msg = "token has expired, please log in again\n"

        if need_login_msg in try_resp:
            pytest.skip("Has not logged in to the Orquestra platform.")

        circuits = [qasm_circuit_default]

        # This will not be a valid operator: will raise error
        operator = []

        # Fill in workflow template
        workflow = gw.gen_expval_workflow(
            backend_component, backend_specs_default, circuits, operator
        )
        file_name = tmpdir.join("test_workflow.yaml")

        with open(file_name, "w") as file:
            d = yaml.dump(workflow, file)

        # Submit a workflow --- error due to the operator
        with pytest.raises(ValueError, match="Error"):
            workflow_id = qe_submit(file_name)


devices = [
    ("orquestra.forest", "wavefunction-simulator", True),
    ("orquestra.forest", "wavefunction-simulator", False),
    ("orquestra.qiskit", "statevector_simulator", True),
    ("orquestra.qiskit", "statevector_simulator", False),
    ("orquestra.qiskit", "qasm_simulator", False),
]


class TestOrquestraIntegration:
    """Test the Orquestra integration with PennyLane."""

    @pytest.mark.parametrize("device_name,backend,analytic", devices)
    def test_apply_hadamard(self, device_name, backend, analytic):
        """Test a simple circuit that applies Hadamard on the first wire."""
        dev = qml.device(device_name, wires=3, backend=backend, analytic=analytic, keep_files=False)

        TOL = analytic_tol if dev.analytic else tol

        # Skip if not logged in to Orquestra
        try_resp = qe_list_workflow()
        need_login_msg = "token has expired, please log in again\n"

        if need_login_msg in try_resp:
            pytest.skip("Has not logged in to the Orquestra platform.")

        @qml.qnode(dev)
        def circuit():
            qml.Hadamard(0)
            return qml.expval(qml.PauliZ(0))

        assert math.isclose(circuit(), 0, abs_tol=TOL)

    def test_compute_expval_including_identity(self):
        """Test a simple circuit that involves computing the expectation value of the
        Identity operator."""
        dev = qml.device("orquestra.qiskit", wires=3)

        # Skip if not logged in to Orquestra
        try_resp = qe_list_workflow()
        need_login_msg = "token has expired, please log in again\n"

        if need_login_msg in try_resp:
            pytest.skip("Has not logged in to the Orquestra platform.")

        @qml.qnode(dev)
        def circuit():
            qml.PauliX(0)
            qml.PauliX(1)
            qml.PauliX(2)
            return (
                qml.expval(qml.Identity(0)),
                qml.expval(qml.PauliZ(1)),
                qml.expval(qml.Identity(2)),
            )

        assert np.allclose(circuit(), np.array([1, -1, 1]))

    def test_jacobian_with_batch_execute(self):
        """Test that the value of the jacobian computed using the internal
        batch_execute method corresponds to the value computed with
        the default.qubit device.

        There are ``qubits * layers * 3 * 2`` many circuits to evaluate.
        """
        try_resp = qe_list_workflow()
        need_login_msg = "token has expired, please log in again\n"

        if need_login_msg in try_resp:
            pytest.skip("Has not logged in to the Orquestra platform.")

        qml.enable_tape()

        # Evaluate 12 circuits (2 * 1 * 3 * 2)
        # By default, this fits into two separate workflow files
        qubits = 2
        layers = 1
        weights = qml.init.strong_ent_layers_uniform(layers, qubits)

        dev1 = qml.device(
            "orquestra.qiskit",
            backend="statevector_simulator",
            wires=qubits,
            analytic=True,
            keep_files=False,
        )
        dev2 = qml.device("default.qubit", wires=qubits, analytic=True)

        def func(weights):
            qml.templates.StronglyEntanglingLayers(weights, wires=range(qubits))
            return qml.expval(qml.PauliZ(0))

        orquestra_qnode = qml.QNode(func, dev1)
        default_qnode = qml.QNode(func, dev2)

        dfunc1 = qml.grad(orquestra_qnode)
        dfunc2 = qml.grad(default_qnode)

        res_orquestra = dfunc1(weights)
        res_default_qubit = dfunc2(weights)

        assert np.allclose(res_orquestra, res_default_qubit)
        qml.disable_tape()

class TestOrquestraIBMQIntegration:
    def test_apply_x(self, token):
        """Test a simple circuit that applies PauliX on the first wire."""
        TOL = tol

        dev = qml.device("orquestra.ibmq", wires=3, ibmqx_token=token)

        # Skip if not logged in to Orquestra
        try_resp = qe_list_workflow()
        need_login_msg = "token has expired, please log in again\n"

        if need_login_msg in try_resp:
            pytest.skip("Has not logged in to the Orquestra platform.")

        @qml.qnode(dev)
        def circuit():
            qml.PauliX(0)
            return qml.expval(qml.PauliZ(0))

        assert math.isclose(circuit(), -1, abs_tol=TOL)
