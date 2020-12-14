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
    """The Orquestra Qiskit device."""

    short_name = "orquestra.qiskit"

    qe_component = "qe-qiskit"
    qe_module_name = "qeqiskit.simulator"
    qe_function_name = "QiskitSimulator"

    def __init__(self, wires, shots=1024, backend="qasm_simulator", **kwargs):
        if backend == "qasm_simulator":
            if "analytic" in kwargs and kwargs["analytic"]:
                # Raise a warning if the analytic attribute was set to True
                warnings.warn(
                    "The qasm_simulator backend device cannot be used in "
                    "analytic mode. Results are based on sampling."
                )

            kwargs["analytic"] = False
        super().__init__(wires, backend=backend, shots=shots, **kwargs)