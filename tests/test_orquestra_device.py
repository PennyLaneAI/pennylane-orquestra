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
import pytest
import subprocess
import os
import uuid
import time
import numpy as np

import pennylane as qml
import pennylane.tape
import pennylane_orquestra
from pennylane_orquestra import OrquestraDevice, QeQiskitDevice, QeIBMQDevice
from conftest import (
    test_batch_res0,
    test_batch_res1,
    test_batch_res2,
    resources_default,
    MockPopen,
)

qiskit_analytic_specs = '{"module_name": "qeqiskit.simulator", "function_name": "QiskitSimulator", "device_name": "statevector_simulator"}'
qiskit_sampler_specs = '{"module_name": "qeqiskit.simulator", "function_name": "QiskitSimulator", "device_name": "statevector_simulator", "n_samples": 1000}'
ibmq_specs = '{"module_name": "qeqiskit.backend", "function_name": "QiskitBackend", "device_name": "ibmq_qasm_simulator", "n_samples": 1000, "api_token": "Some token"}'


class TestBaseDevice:
    """Test the Orquestra base device"""

    def test_error_if_not_expval(self):
        """Test that an error is raised if not an expectation value is computed"""
        dev = qml.device("orquestra.qiskit", wires=2)

        @qml.qnode(dev)
        def circuit():
            return qml.var(qml.PauliZ(0))

        with pytest.raises(NotImplementedError):
            circuit()

    def test_qasm_simulator_analytic_warning(self):
        """Test that a warning is raised when using the QeQiskitDevice with the
        qasm_simulator backend in analytic mode and that we'll switch to
        sampling mode."""
        with pytest.warns(
            Warning,
            match="The qasm_simulator backend device cannot be used in "
            "analytic mode. Results are based on sampling.",
        ):
            dev = qml.device("orquestra.qiskit", backend="qasm_simulator", wires=2, analytic=True)

        assert not dev.analytic

    def test_ibmq_analytic_warning(self):
        """Test that a warning is raised when using the IBMQDevice in analytic
        mode and that we'll switch to sampling mode."""
        with pytest.warns(
            Warning, match="device cannot be used in analytic mode. Results are based on sampling."
        ):
            dev = qml.device("orquestra.ibmq", wires=2, analytic=True, ibmqx_token="Some token")

        assert not dev.analytic

    def test_ibmq_no_token_error(self):
        """Test that an error is raised when using the IBMQDevice without any
        tokens specified."""
        with pytest.raises(ValueError, match="Please pass a valid IBMQX token"):
            dev = qml.device("orquestra.ibmq", wires=2, analytic=False)

    def test_empty_apply(self):
        """Test that calling the empty apply method returns None."""
        dev = qml.device("orquestra.qiskit", wires=2, analytic=False)

        assert dev.apply([]) is None

class TestCreateBackendSpecs:
    """Test the create_backend_specs function"""

    def test_backend_specs_analytic(self):
        """Test that the backend specs are created well for an analytic device"""
        dev = qml.device(
            "orquestra.qiskit", backend="statevector_simulator", wires=1, analytic=True
        )
        assert dev.backend_specs == qiskit_analytic_specs

    def test_backend_specs_sampling(self):
        """Test that the backend specs are created well for a sampling device"""
        dev = qml.device(
            "orquestra.qiskit", backend="statevector_simulator", wires=1, shots=1000, analytic=False
        )
        assert dev.backend_specs == qiskit_sampler_specs

    def test_backend_specs_ibmq(self):
        dev = qml.device(
            "orquestra.ibmq", wires=1, analytic=False, shots=1000, ibmqx_token="Some token"
        )
        assert dev.backend_specs == ibmq_specs


class TestSerializeCircuit:
    """Test the serialize_circuit function"""

    def test_serialize_circuit_rotations(self):
        """Test that a circuit that is serialized correctly with rotations for
        a remote hardware backend"""
        dev = QeQiskitDevice(wires=1, shots=1000, backend="qasm_simulator", analytic=False)

        def circuit():
            qml.Hadamard(wires=[0])
            return qml.expval(qml.Hadamard(0))

        qnode = qml.QNode(circuit, dev)
        qnode._construct([], {})

        qasm = dev.serialize_circuit(qnode.circuit)
        expected = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[1];\ncreg c[1];\nh q[0];\nry(-0.7853981633974483) q[0];\n'
        assert qasm == expected

    def test_serialize_circuit_no_rotations(self):
        """Test that a circuit that is serialized correctly without rotations for
        a simulator backend"""
        dev = QeQiskitDevice(wires=1, shots=1000, backend="statevector_simulator", analytic=True)

        def circuit():
            qml.Hadamard(wires=[0])
            return qml.expval(qml.Hadamard(0))

        qnode = qml.QNode(circuit, dev)
        qnode._construct([], {})

        qasm = dev.serialize_circuit(qnode.circuit)
        expected = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[1];\ncreg c[1];\nh q[0];\n'
        assert qasm == expected


mx = np.diag(np.array([1, 2, 3, 4]))

obs_serialize = [
    # Don't decomposition
    (qml.Identity(wires=[0]), "1 []"),
    (qml.PauliX(wires=[0]), "1 [X0]"),
    (qml.PauliY(wires=[0]), "1 [Y0]"),
    (qml.PauliZ(wires=[0]), "1 [Z0]"),
    # Need decomposition
    (qml.Hadamard(wires=[0]), "0.7071067811865475 [X0] + 0.7071067811865475 [Z0]"),
    (qml.Hermitian(mx, wires=[0, 1]), "2.5 [] + -0.5 [Z1] + -1.0 [Z0]"),
    (qml.Identity(wires=[0]) @ qml.Identity(wires=[1]), "1 []"),
    (qml.PauliX(wires=[0]) @ qml.Identity(wires=[1]), "1 [X0]"),
    (qml.PauliY(wires=[0]) @ qml.Identity(wires=[1]), "1 [Y0]"),
    (qml.PauliZ(wires=[0]) @ qml.Identity(wires=[1]), "1 [Z0]"),
    (qml.Hermitian(mx, wires=[0, 1]) @ qml.Identity(wires=[2]), "2.5 [] + -0.5 [Z1] + -1.0 [Z0]"),
]

obs_serialize_custom_labels = [
    # Custom wires
    (qml.PauliZ(wires=["a"]), "1 [Z0]"),
    (qml.PauliX(wires=["c"]), "1 [X2]"),
    (
        qml.Hermitian(mx, wires=["a", "b"]) @ qml.Identity(wires=["c"]),
        "2.5 [] + -0.5 [Z1] + -1.0 [Z0]",
    ),
]

serialize_needs_rot = [
    (qml.PauliZ(0) @ qml.PauliZ(2), "[Z0 Z2]"),
    (qml.PauliZ(2), "[Z2]"),
    (qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(2), "[Z0 Z1 Z2]"),
    # Rotations need to be included
    (qml.PauliY(2), "[Z2]"),
    (qml.PauliX(0) @ qml.PauliY(2), "[Z0 Z2]"),
    (qml.PauliY(0) @ qml.PauliX(1) @ qml.PauliY(2), "[Z0 Z1 Z2]"),
]

# More advanced examples for testing the correct wires
obs_decomposed_wires_check = [
    (qml.Hadamard(0), '0.7071067811865475 [X0] + 0.7071067811865475 [Z0]'),
    (qml.Hadamard(2), '0.7071067811865475 [X2] + 0.7071067811865475 [Z2]'),
    (qml.Hadamard(2) @ qml.Hadamard(1), '0.4999999999999999 [X2 X1] + 0.4999999999999999 [X2 Z1] + 0.4999999999999999 [Z2 X1] + 0.4999999999999999 [Z2 Z1]'),
    (qml.Hermitian((qml.PauliY(1) @ qml.PauliX(0) @ qml.PauliZ(2)).matrix, wires=[1,0,2]), '1.0 [Y1 X0 Z2]'),
    (qml.PauliY(2) @ qml.Hermitian((qml.PauliX(1)).matrix, wires=[1]), '1.0 [Y2 X1]')
]

class TestSerializeOperator:
    """Test the serialize_operator function"""

    @pytest.mark.parametrize(
        "wires, expected", [([2], "[Z2]"), ([0, 2], "[Z0 Z2]"), ([0, 1, 2], "[Z0 Z1 Z2]")]
    )
    def test_pauliz_operator_string(self, wires, expected):
        """Test that an operator is serialized correctly on a device with
        consecutive integer wires."""
        dev = QeQiskitDevice(wires=3, shots=1000, backend="qasm_simulator", analytic=False)
        op_str = dev.pauliz_operator_string(wires)
        assert op_str == expected

    @pytest.mark.parametrize("obs, expected", obs_serialize)
    def test_qubit_operator_consec_int_wires(self, obs, expected):
        """Test that an operator is serialized correctly on a device with
        consecutive integer wires."""
        dev = QeQiskitDevice(wires=3, shots=1000, backend="qasm_simulator", analytic=False)
        op_str = dev.qubit_operator_string(obs)
        assert op_str == expected

    @pytest.mark.parametrize("obs, expected", obs_serialize_custom_labels)
    def test_qubit_operator_custom_labels(self, obs, expected):
        """Test that an operator is serialized correctly on a device with
        custom wire labels."""
        dev = QeQiskitDevice(
            wires=["a", "b", "c"], shots=1000, backend="qasm_simulator", analytic=False
        )
        op_str = dev.qubit_operator_string(obs)
        assert op_str == expected

    @pytest.mark.parametrize("obs, expected", serialize_needs_rot)
    def test_serialize_operator_needs_rotation(self, obs, expected):
        """Test that a device that needs to include rotations serializes the
        operators correctly."""
        dev = QeQiskitDevice(wires=3, shots=1000, backend="qasm_simulator", analytic=False)
        op_str = dev.serialize_operator(obs)
        assert op_str == expected

    @pytest.mark.parametrize("obs, expected", obs_serialize)
    def test_serialize_operator_no_rot(self, obs, expected):
        """Test that a device that does not need to include rotations
        serializes the operators with consecutive integer wires correctly."""
        dev = QeQiskitDevice(wires=3, backend="statevector_simulator", analytic=True)
        op_str = dev.serialize_operator(obs)
        assert op_str == expected

    @pytest.mark.parametrize("obs, expected", obs_serialize_custom_labels)
    def test_serialize_operator_no_rot_custom_labels(self, obs, expected):
        """Test that a device that does not need to include rotations
        serializes the operators with custom labels correctly."""
        dev = QeQiskitDevice(wires=["a", "b", "c"], backend="statevector_simulator", analytic=True)
        op_str = dev.serialize_operator(obs)
        assert op_str == expected

    @pytest.mark.parametrize("obs, expected", obs_decomposed_wires_check)
    def test_decomposed_operator_correct_wires(self, obs, expected):
        """Test that the serialized form of observables that need decomposition
        match the correct wires."""
        dev = qml.device('orquestra.qulacs', wires=3)

        res = dev.serialize_operator(obs)
        assert res == expected

    def test_operator_with_invalid_wire(self, monkeypatch, test_result):
        """Test that a device with custom wire labels raises an error when an
        invalid wire is used in the operator definition.

        This test is meant to check that the internal wire mappings do not
        introduce false positive behaviour when using custom wire labels.
        """
        dev = QeQiskitDevice(
            wires=["a", "b", "c"], shots=1000, backend="qasm_simulator", analytic=False
        )

        with monkeypatch.context() as m:
            m.setattr(pennylane_orquestra.cli_actions, "user_data_dir", lambda *args: tmpdir)

            # Disable submitting to the Orquestra platform by mocking Popen
            m.setattr(subprocess, "Popen", lambda *args, **kwargs: MockPopen())
            m.setattr(
                pennylane_orquestra.orquestra_device,
                "loop_until_finished",
                lambda *args, **kwargs: test_result,
            )

            @qml.qnode(dev)
            def circuit():
                return qml.expval(qml.PauliZ(0))

            with pytest.raises(
                qml.qnodes.base.QuantumFunctionError,
                match="Operation PauliZ applied to invalid wire",
            ):
                circuit()