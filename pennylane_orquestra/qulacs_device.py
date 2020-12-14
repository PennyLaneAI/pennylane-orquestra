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
    """Orquestra device"""

    short_name = "orquestra.qulacs"

    qe_component = "qe-qulacs"
    qe_module_name = "qequlacs.simulator"
    qe_function_name = "QulacsSimulator"

    def __init__(self, wires, shots=1024, **kwargs):
        super().__init__(wires, shots=shots, **kwargs)
