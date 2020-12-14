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
Base device class for PennyLane-Orquestra.
"""
# pylint: disable=protected-access, consider-using-enumerate

import abc
import json
import re
import uuid

from pennylane import QubitDevice
from pennylane.operation import Expectation, Tensor
from pennylane.ops import Identity
from pennylane.utils import decompose_hamiltonian
from pennylane.wires import Wires

from pennylane_orquestra._version import __version__
from pennylane_orquestra.cli_actions import loop_until_finished, qe_submit, write_workflow_file
from pennylane_orquestra.gen_workflow import gen_expval_workflow
from pennylane_orquestra.utils import _terms_to_qubit_operator_string


class OrquestraDevice(QubitDevice, abc.ABC):
    """The Orquestra base device.

    Provides the ``~.execute`` and ``~.batch_execute`` methods which allows
    remote device executions by generating, submitting Orquestra workflows and
    processing their results.

    The ``~.batch_execute`` method can be utilized to send workflows that
    contain several circuits which are computed in parallel on a remote device.

    The workflow files generated are placed into a user specific data folder
    specified by the output of ``appdirs.user_data_dir("pennylane-orquestra",
    "Xanadu")``. By default, such files are removed (see
    ``keep_files`` keyword argument). After each device execution,
    filenames for the generated workflows are stored in the ``filenames``
    attribute.

    Computing the expectation value of the identity operator does not involve a
    workflow submission (hence no files are created).

    Args:
        wires (int, Iterable[Number, str]]): Number of subsystems represented
            by the device, or iterable that contains unique labels for the
            subsystems as numbers (i.e., ``[-1, 0, 2]``) or strings (``['ancilla',
            'q1', 'q2']``). Default 1 if not specified.
        shots (int): number of circuit evaluations/random samples used to estimate
            expectation values of observables
        analytic (bool): If ``True``, the device calculates probability,
            expectation values, and variances analytically. If ``False``, a finite
            number of samples set by the argument ``shots`` are used to estimate
            these quantities.

    Keyword Args:
        backend=None (str): the Orquestra backend device to use for the
            specific Orquestra backend, if applicable
        batch_size=10 (int): the size of each circuit batch when using the
            ``~.batch_execute`` method to send multiple workflows
        keep_files=False (bool): Whether or not the workflow files
            generated during the circuit execution should be kept or deleted.
        resources=None (dict): An option for Orquestra, specifies the resources
            provisioned for the clusters running each workflow step.
        timeout=300 (int): The time until a job should timeout after getting no
            response from Orquestra (in seconds).
    """

    name = "Orquestra base device for PennyLane"
    short_name = "orquestra.base"
    pennylane_requires = ">=0.11.0"
    version = __version__
    author = "Xanadu"

    operations = {
        "BasisState",
        "CNOT",
        "CRX",
        "CRY",
        "CRZ",
        "CRot",
        "CSWAP",
        "CY",
        "CZ",
        "Hadamard",
        "MultiRZ",
        "PauliX",
        "PauliY",
        "PauliZ",
        "PhaseShift",
        "QubitStateVector",
        "RX",
        "RY",
        "RZ",
        "Rot",
        "S",
        "SWAP",
        "SX",
        "T",
        "Toffoli",
    }

    observables = {"PauliX", "PauliY", "PauliZ", "Identity", "Hadamard"}

    def __init__(self, wires, shots=1000, analytic=True, **kwargs):
        super().__init__(wires=wires, shots=shots, analytic=analytic)

        self.backend = kwargs.get("backend", None)
        self._batch_size = kwargs.get("batch_size", 10)
        self._keep_files = kwargs.get("keep_files", False)
        self._resources = kwargs.get("resources", None)
        self._timeout = kwargs.get("timeout", 300)
        self._latest_id = None
        self._filenames = []
        self._backend_specs = None

    def apply(self, operations, **kwargs):
        pass

    @classmethod
    def capabilities(cls):
        capabilities = super().capabilities().copy()
        capabilities.update(
            model="qubit",
            supports_inverse_operations=False,
            supports_analytic_computation=True,
            returns_probs=False,
        )
        return capabilities

    @property
    def backend_specs(self):
        """The backend specifications defined for the device.

        Returns:
            str: the backend specifications represented as a string
        """
        if self._backend_specs is None:
            backend_specs_dict = self.create_backend_specs()
            self._backend_specs = json.dumps(backend_specs_dict)

        return self._backend_specs

    def create_backend_specs(self):
        """Create the backend specifications based on the device options.

        Returns:
            dict: the backend specifications represented as a dictionary
        """
        backend_specs = {}
        backend_specs["module_name"] = self.qe_module_name
        backend_specs["function_name"] = self.qe_function_name

        if self.backend is not None:
            # Only devices that allow multiple backends need to specify one
            # E.g., qe-qiskit
            backend_specs["device_name"] = self.backend

        if not self.analytic:
            backend_specs["n_samples"] = self.shots

        return backend_specs

    @property
    def latest_id(self):
        """Returns the latest workflow ID that has been executed.

        Returns:
            str: the ID of the latest workflow that has been submitted
        """
        return self._latest_id

    @property
    def filenames(self):
        """Returns the names of the workflow files created during device
        executions.

        Returns:
            list: the workflow filenames
        """
        return self._filenames

    @property
    @abc.abstractmethod
    def qe_module_name(self):
        """Device specific Orquestra module name used in the backend
        specification."""

    @property
    @abc.abstractmethod
    def qe_function_name(self):
        """Device specific Orquestra function name used in the backend
        specification."""

    @property
    @abc.abstractmethod
    def qe_component(self):
        """Device specific Orquestra component name used in the backend
        specification."""

    def serialize_circuit(self, circuit):
        """Serializes the circuit before submission according to the backend
        specified.

        The circuit is represented as an OpenQASM 2.0 program. Measurement
        instructions are removed from the program as the operator is passed
        separately.

        Args:
            circuit (~.CircuitGraph): circuit to serialize

        Returns:
            str: OpenQASM 2.0 representation of the circuit without any
            measurement instructions
        """
        qasm_str = circuit.to_openqasm(rotations=not self.analytic)

        qasm_without_measurements = re.sub("measure.*?;\n", "", qasm_str)
        return qasm_without_measurements

    def process_observables(self, observables):
        """Processes the observables provided with the circuits.

        If the observable defined is the identity, then no serialization
        happens. Instead, the index of the observable is saved.

        Args:
            observables (list): a list of observables to process

        Returns:
            tuple:

                * the serialized non-identity operators
                * the indices of the identity operators
        """
        ops = []
        identity_indices = []
        for idx, obs in enumerate(observables):
            if not isinstance(obs, Identity):
                # Only serialize if it's not the identity
                ops.append(self.serialize_operator(obs))
            else:
                # Otherwise keep track of the indices and use the theoreticaly
                # value as a result later
                identity_indices.append(idx)

        return ops, identity_indices

    def serialize_operator(self, observable):
        """
        Serialize the observable specified for the circuit as an OpenFermion
        operator.

        Args:
            observable (~.Observable): the observable to get the operator
                representation for

        Returns:
            str: string representation of terms making up the observable
        """
        if not self.analytic:
            obs_wires = observable.wires
            wires = self.wires.indices(obs_wires)
            op_str = self.pauliz_operator_string(wires)
        else:
            op_str = self.qubit_operator_string(observable)

        return op_str

    @staticmethod
    def pauliz_operator_string(wires):
        """Creates an OpenFermion operator string based on the related wires
        that can be passed when creating an ``openfermion.IsingOperator``.

        This method is used if rotations are needed for the backend specified.
        In such a case a string that represents measuring PauliZ on each of the
        affected wires is used.

        **Example**

        >>> dev = QeQiskitDevice(wires=2)
        >>> wires = [0, 1, 2]
        >>> op_str = dev.pauliz_operator_string(wires)
        >>> print(op_str)
        [Z0 Z1 Z2]
        >>> print(openfermion.IsingOperator(op_str))
        1.0 [Z0 Z1 Z2]

        Args:
            wires (Wires): the wires the observable of the quantum function
                acts on

        Returns:
            str: the ``openfermion.IsingOperator`` string representation
        """
        op_wires_but_last = [f"Z{w} " for w in wires[:-1]]
        op_last_wire = f"Z{wires[-1]}"
        op_str = "".join(["[", *op_wires_but_last, op_last_wire, "]"])
        return op_str

    def qubit_operator_string(self, observable):
        """Creates an OpenFermion operator string from an observable that can
        be passed when creating an ``openfermion.QubitOperator``.

        This method decomposes an observable into a sum of Pauli terms and
        identities, if needed.

        **Example**

        >>> dev = QeQiskitDevice(wires=2)
        >>> obs = qml.PauliZ(0)
        >>> op_str = dev.qubit_operator_string(obs)
        >>> print(op_str)
        1 [Z0]
        >>> obs = qml.Hadamard(0)
        >>> op_str = dev.qubit_operator_string(obs)
        >>> print(op_str)
        0.7071067811865475 [X0] + 0.7071067811865475 [Z0]

        Args:
            observable (pennylane.operation.Observable): the observable to serialize

        Returns:
            str: the ``openfermion.QubitOperator`` string representation
        """
        accepted_obs = {"PauliX", "PauliY", "PauliZ", "Identity"}

        if isinstance(observable, Tensor):
            need_decomposition = any(o.name not in accepted_obs for o in observable.obs)
        else:
            need_decomposition = observable.name not in accepted_obs

        if need_decomposition:

            original_observable = observable

            # Decompose the matrix of the observable
            # This removes information about the wire labels used and
            # consecutive integer wires are used
            coeffs, obs_list = decompose_hamiltonian(original_observable.matrix)

            for idx in range(len(obs_list)):
                obs = obs_list[idx]

                if not isinstance(obs, Tensor):
                    # Convert terms to Tensor such that _terms_to_qubit_operator
                    # can be used
                    obs_list[idx] = Tensor(obs)

                # Need to use the custom wire labels of the original observable
                original_wires = original_observable.wires.tolist()
                for o, mapped_w in zip(obs_list[idx].obs, original_wires):
                    o._wires = Wires(mapped_w)

        else:
            if not isinstance(observable, Tensor):
                # If decomposition is not needed and is not a Tensor, we need
                # to convert the single observable
                observable = Tensor(observable)

            coeffs = [1]
            obs_list = [observable]

        # Use consecutive integers as default wire_map
        wire_map = {v: idx for idx, v in enumerate(self.wires)}
        return _terms_to_qubit_operator_string(coeffs, obs_list, wires=wire_map)
