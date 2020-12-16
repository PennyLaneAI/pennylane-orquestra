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
The Qiskit device class for PennyLane-Orquestra.
"""
import warnings

from pennylane_orquestra.orquestra_device import OrquestraDevice


class QeQiskitDevice(OrquestraDevice):
    """The Orquestra Qiskit device.

    Args:
        wires (int, Iterable[Number, str]]): Number of subsystems represented
            by the device, or iterable that contains unique labels for the
            subsystems as numbers (i.e., ``[-1, 0, 2]``) or strings (``['ancilla',
            'q1', 'q2']``). Default 1 if not specified.
        shots (int): number of circuit evaluations/random samples used to estimate
            expectation values of observables
        backend (str): the name of the Qiskit backend to use supported by
            Orquestra, e.g., ``"qasm_simulator"`` or ``"statevector_simulator"``

    Keyword Args:
        analytic=False (bool): If ``True``, the device calculates expectation
            values analytically. If ``False``, a finite number of samples set by
            the argument ``shots`` are used to estimate these quantities. Hardware
            devices like the ``"qasm_simulator"`` can only be run with
            ``analytic=False`` and this option will be set internally.
    """

    short_name = "orquestra.qiskit"

    qe_component = "qe-qiskit"
    qe_module_name = "qeqiskit.simulator"
    qe_function_name = "QiskitSimulator"

    def __init__(self, wires, shots=10000, backend="qasm_simulator", **kwargs):
        if backend == "qasm_simulator":
            if kwargs.get("analytic", None):
                # Raise a warning if the analytic attribute was set to True
                warnings.warn(
                    f"The {self.short_name} device cannot be used in analytic "
                    f"mode with the {backend} backend. Setting analytic to False. "
                    "Results are based on sampling."
                )

            kwargs["analytic"] = False

        # TODO: Remove when the Orquestra supports qiskit>0.18.3 with its Qiskit component
        if backend == "statevector_simulator":
            if not kwargs.get("analytic", True):
                # Raise a warning if the analytic attribute was set to False
                warnings.warn(
                    f"The {self.short_name} device with the {backend} backend "
                    "always runs with shots=1 due to a malfunction in the "
                    "version of Qiskit used by Orquestra."
                )

        super().__init__(wires, backend=backend, shots=shots, **kwargs)
