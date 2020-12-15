# Copyright 2018-2020 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module contains utility functions for the PennyLane-Orquestra plugin.

The original implementation of the ``_process_wires`` and
``_terms_to_qubit_operator`` functions is a part of the PennyLane-QChem
library.
"""
from pennylane.wires import Wires


def _process_wires(wires, n_wires=None):
    r"""
    Checks and consolidates custom user wire mapping into a consistent, direction-free, `Wires`
    format. Used for converting between OpenFermion qubit numbering and Pennylane wire labels.

    Since OpenFermion's qubit numbering is always consecutive int, simple iterable types such as
    list, tuple, or Wires can be used to specify the 2-way `qubit index` <-> `wire label` mapping
    with indices representing qubits. Dict can also be used as a mapping, but does not provide any
    advantage over lists other than the ability to do partial mapping/permutation in the
    `qubit index` -> `wire label` direction.

    It is recommended to pass Wires/list/tuple `wires` since it's direction-free, i.e. the same
    `wires` argument can be used to convert both ways between OpenFermion and Pennylane. Only use
    dict for partial or unordered mapping.

    Args:
        wires (Wires, list, tuple, dict): User wire labels or mapping for Pennylane ansatz.
            For types Wires, list, or tuple, each item in the iterable represents a wire label
            corresponding to the qubit number equal to its index.
            For type dict, only int-keyed dict (for qubit-to-wire conversion) or
            consecutive-int-valued dict (for wire-to-qubit conversion) is accepted.
            If None, will be set to consecutive int based on ``n_wires``.
        n_wires (int): Number of wires used if known. If None, will be inferred from ``wires``; if
            ``wires`` is not available, will be set to 1.

    Returns:
        Wires: Cleaned wire mapping with indices corresponding to qubits and values
            corresponding to wire labels.

    **Example**

    >>> # consec int wires if no wires mapping provided, ie. identity map: 0<->0, 1<->1, 2<->2
    >>> _process_wires(None, 3)
    <Wires = [0, 1, 2]>

    >>> # List as mapping, qubit indices with wire label values: 0<->w0, 1<->w1, 2<->w2
    >>> _process_wires(['w0','w1','w2'])
    <Wires = ['w0', 'w1', 'w2']>

    >>> # Wires as mapping, qubit indices with wire label values: 0<->w0, 1<->w1, 2<->w2
    >>> _process_wires(Wires(['w0', 'w1', 'w2']))
    <Wires = ['w0', 'w1', 'w2']>

    >>> # Dict as partial mapping, int qubits keys to wire label values: 0->w0, 1 unchanged, 2->w2
    >>> _process_wires({0:'w0',2:'w2'})
    <Wires = ['w0', 1, 'w2']>

    >>> # Dict as mapping, wires label keys to consec int qubit values: w2->2, w0->0, w1->1
    >>> _process_wires({'w2':2, 'w0':0, 'w1':1})
    <Wires = ['w0', 'w1', 'w2']>
    """

    # infer from wires, or assume 1 if wires is not of accepted types.
    if n_wires is None:
        n_wires = len(wires) if isinstance(wires, (Wires, list, tuple, dict)) else 1

    # defaults to no mapping.
    if wires is None:
        return Wires(range(n_wires))

    if isinstance(wires, (Wires, list, tuple)):
        # does not care about the tail if more wires are provided than n_wires.
        wires = Wires(wires[:n_wires])

    elif isinstance(wires, dict):

        if all([isinstance(w, int) for w in wires.keys()]):
            # Assuming keys are taken from consecutive int wires. Allows for partial mapping.
            n_wires = max(wires) + 1
            labels = list(range(n_wires))  # used for completing potential partial mapping.
            for k, v in wires.items():
                if k < n_wires:
                    labels[k] = v
            wires = Wires(labels)
        elif set(range(n_wires)).issubset(set(wires.values())):
            # Assuming values are consecutive int wires (up to n_wires, ignores the rest).
            # Does NOT allow for partial mapping.
            wires = {v: k for k, v in wires.items()}  # flip for easy indexing
            wires = Wires([wires[i] for i in range(n_wires)])
        else:
            raise ValueError("Expected only int-keyed or consecutive int-valued dict for `wires`")

    else:
        raise ValueError(
            "Expected type Wires, list, tuple, or dict for `wires`, got {}".format(type(wires))
        )

    if len(wires) != n_wires:
        # check length consistency when all checking and cleaning are done.
        raise ValueError(
            "Length of `wires` ({}) does not match `n_wires` ({})".format(len(wires), n_wires)
        )

    return wires


def _terms_to_qubit_operator_string(coeffs, ops, wires=None):
    r"""Converts a 2-tuple of complex coefficients and PennyLane operations to
    a string representation of OpenFermion ``QubitOperator``.

    Although this function assumes that the terms in ops are unique. If that is
    not the case, duplicate terms are summed when constructing a
    ``QubitOperator``.

    Args:
        coeffs (array[complex]):
            coefficients for each observable, same length as ops
        ops (Iterable[pennylane.operation.Observable]): List of PennyLane observables as
            Tensor products of Pauli observables
        wires (Wires, list, tuple, dict): Custom wire mapping used to convert to qubit operator
            from an observable terms measurable in a PennyLane ansatz.
            For types Wires/list/tuple, each item in the iterable represents a wire label
            corresponding to the qubit number equal to its index.
            For type dict, only consecutive-int-valued dict (for wire-to-qubit conversion) is
            accepted. If None, will map sorted wires from all `ops` to consecutive int.

    Returns:
        str: the string representation for an instance of ``openfermion.QubitOperator``.

    **Example**

    >>> coeffs = np.array([0.1, 0.2])
    >>> ops = [
    ...     qml.operation.Tensor(qml.PauliX(wires=['w0'])),
    ...     qml.operation.Tensor(qml.PauliY(wires=['w0']), qml.PauliZ(wires=['w2']))
    ... ]
    >>> _terms_to_qubit_operator(coeffs, ops, wires=Wires(['w0', 'w1', 'w2']))
    0.1 [X0] +
    0.2 [Y0 Z2]
    """
    all_wires = Wires.all_wires([op.wires for op in ops], sort=True)

    if wires is not None:
        qubit_indexed_wires = _process_wires(
            wires,
        )
        if not set(all_wires).issubset(set(qubit_indexed_wires)):
            raise ValueError("Supplied `wires` does not cover all wires defined in `ops`.")
    else:
        qubit_indexed_wires = all_wires

    q_op = []
    for coeff, op in zip(coeffs, ops):

        extra_obsvbs = set(op.name) - {"PauliX", "PauliY", "PauliZ", "Identity"}
        if extra_obsvbs != set():
            raise ValueError(
                "Expected only PennyLane observables PauliX/Y/Z or Identity, "
                + "but also got {}.".format(extra_obsvbs)
            )

        # Pauli axis names, note s[-1] expects only 'Pauli{X,Y,Z}'
        pauli_names = [s[-1] if s != "Identity" else s for s in op.name]

        all_identity = all(obs.name == "Identity" for obs in op.obs)
        if (op.name == ["Identity"] and len(op.wires) == 1) or all_identity:
            term_str = ""
        else:
            term_str = " ".join(
                [
                    "{}{}".format(pauli, qubit_indexed_wires.index(wire))
                    for pauli, wire in zip(pauli_names, op.wires)
                    if pauli != "Identity"
                ]
            )

        # This is how one makes a string for a QubitOperator in OpenFermion
        q_op.append(f"{coeff} [{term_str}]")
        q_op.append(" + ")

    # Remove the last ' + ' element
    q_op.pop()
    return "".join(q_op)
