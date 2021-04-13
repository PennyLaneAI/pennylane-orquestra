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
The Qulacs device class for PennyLane-Orquestra.
"""
from pennylane_orquestra.orquestra_device import OrquestraDevice


class QeQulacsDevice(OrquestraDevice):
    """The Orquestra Qulacs device.

    Args:
        wires (int, Iterable[Number, str]]): Number of subsystems represented
            by the device, or iterable that contains unique labels for the
            subsystems as numbers (i.e., ``[-1, 0, 2]``) or strings (``['ancilla',
            'q1', 'q2']``). Default 1 if not specified.
        shots (int or list[int]): Number of circuit evaluations/random samples used to estimate
            expectation values of observables. If an integer,
            it specifies the number of samples to estimate these quantities.
            If a list of integers is passed, the circuit evaluations are batched over the list of shots.
    """

    short_name = "orquestra.qulacs"

    qe_component = "qe-qulacs"
    qe_module_name = "qequlacs.simulator"
    qe_function_name = "QulacsSimulator"

    def __init__(self, wires, shots=None, **kwargs):
        super().__init__(wires, shots=shots, **kwargs)
