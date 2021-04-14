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
The IBMQ device class for PennyLane-Orquestra.
"""
import os
import warnings

from pennylane_orquestra.orquestra_device import OrquestraDevice


class QeIBMQDevice(OrquestraDevice):
    """The Orquestra IBMQ device.

    Args:
        wires (int, Iterable[Number, str]]): Number of subsystems represented
            by the device, or iterable that contains unique labels for the
            subsystems as numbers (i.e., ``[-1, 0, 2]``) or strings (``['ancilla',
            'q1', 'q2']``). Default 1 if not specified.
        shots (int or list[int]): Number of circuit evaluations/random samples used to estimate
            expectation values of observables. If ``None``, the device calculates
            probability, expectation values, and variances analytically. If an integer,
            it specifies the number of samples to estimate these quantities.
            If a list of integers is passed, the circuit evaluations are batched over the list of shots.
        backend (str): the name of the Qiskit backend to use supported by
            Orquestra, e.g., ``"ibmq_qasm_simulator"`` or the name of real hardware
            devices

    Keyword Args:
        ibmqx_token=None (str): the authentication token needed to run a job on
            IBMQ
    """

    short_name = "orquestra.ibmq"

    qe_component = "qe-qiskit"
    qe_module_name = "qeqiskit.backend"
    qe_function_name = "QiskitBackend"

    def __init__(self, wires, shots=8192, backend="ibmq_qasm_simulator", **kwargs):

        self._token = kwargs.get("ibmqx_token", None) or os.getenv("IBMQX_TOKEN")

        if self._token is None:
            raise ValueError(
                "Please pass a valid IBMQX token to the device using the "
                "'ibmqx_token' argument or by specifying the IBMQX_TOKEN "
                "environment variable."
            )

        if shots is None:
            # Raise a warning if the analytic attribute was set to True
            warnings.warn(
                f"The {self.short_name} device cannot be used in analytic "
                "mode. Setting shots to 8192. Results are based on "
                "sampling."
            )

            shots = 8192

        super().__init__(wires, backend=backend, shots=shots, **kwargs)

    def create_backend_specs(self):
        backend_dict = super().create_backend_specs()

        # Plug in the IBMQ token
        backend_dict["api_token"] = self._token
        return backend_dict
