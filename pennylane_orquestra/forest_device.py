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
The Forest device class for PennyLane-Orquestra.
"""
from pennylane_orquestra.orquestra_device import OrquestraDevice


class QeForestDevice(OrquestraDevice):
    """Orquestra device"""

    short_name = "orquestra.forest"

    qe_component = "qe-forest"
    qe_module_name = "qeforest.simulator"
    qe_function_name = "ForestSimulator"

    def __init__(self, wires, shots=1024, backend="wavefunction-simulator", **kwargs):
        if "qvm" in backend:
            if kwargs.get("analytic", False):
                # Raise a warning if the analytic attribute was set to True
                warnings.warn(
                    f"The {backend} backend device cannot be used in "
                    "analytic mode. Results are based on sampling."
                )

            kwargs["analytic"] = False
        super().__init__(wires, backend=backend, shots=shots, **kwargs)
