"""
The PennyLane-Orquestra step for computing the expectation value of Hermitian
operators given a quantum circuit and a quantum device.

Functions defined in this file may be included in an Orquestra workflow file as
a workflow step. Such workflow steps are executed on a remote Orquestra node.
"""
import json

import numpy as np
from openfermion import IsingOperator, QubitOperator
from qiskit import QuantumCircuit

from zquantum.core.circuit import Circuit
from zquantum.core.measurement import expectation_values_to_real
from zquantum.core.utils import create_object, save_list


def run_circuit_and_get_expval(
    backend_specs: dict,
    circuit: str,
    operators: str,
):
    """Takes a circuit to obtain the expectation value of an operator on a
    given backend.

    All backend calls used in this function are defined as ``QuantumBackend``
    and ``QuantumSimulator`` interface standard methods implemented are defined
    in the ``z-quantum-core`` repository.

    There are two computation modes: sampling and exact. Expectation values are
    computed by post-processing samples when an Orquestra ``QuantumBackend`` is
    used or the number of samples was specified for a ``QuantumSimulator``
    backend. When the number of samples was not specified, ``QuantumSimulator``
    backends run in exact mode.

    Args:
        backend_specs (dict): the parsed Orquestra backend specifications
        circuit (str): the circuit represented as an OpenQASM 2.0 program
        operators (str): the operator in an ``openfermion.QubitOperator``
            or ``openfermion.IsingOperator`` representation
    """
    backend_specs = json.loads(backend_specs)
    operators = json.loads(operators)

    backend = create_object(backend_specs)

    # 1. Parse circuit
    qc = QuantumCircuit.from_qasm_str(circuit)

    # 2. Create operators
    ops = []
    for op in operators:
        if backend.n_samples is not None:
            # Operator for Backend/Simulator in sampling mode
            ops.append(IsingOperator(op))
        else:
            # Operator for Simulator exact mode
            ops.append(QubitOperator(op))

    # 2.+1
    # Activate the qubits that are measured but were not acted on
    # By applying the identity
    # Note: this is a temporary logic subject to be removed once supported by
    # Orquestra

    # Get the active qubits of the circuit
    active_qubits = []
    for instr in qc.data:
        instruction_qubits = [qubit.index for qubit in instr[1]]
        active_qubits.extend(instruction_qubits)

    active_qubits = set(active_qubits)

    # Get the qubits we'd like to measure
    # Data for identities is not stored, need to account for empty terms
    op_qubits = [term[0][0] for op in ops for term in op.terms if term]

    need_to_activate = set(op_qubits) - active_qubits
    if not need_to_activate == set():
        for qubit in need_to_activate:
            # Apply the identity
            qc.id(qubit)

    # If there are still no instructions, apply identity to the first qubit
    # Can happen for an empty circuit when measuring the identity operator
    if not qc.data:
        qc.id(qc.qubits[0])

    # Convert to zquantum.core.circuit.Circuit
    circuit = Circuit(qc)

    # 3. Expval
    results = _get_expval(backend, circuit, ops)

    save_list(results, "expval.json")


def _get_expval(backend, circuit, ops):
    """Auxiliary function to get the expectation value of a list of operators
    given a quantum circuit and a quantum backend.

    In sampling mode, the same measurement outcomes are post-processed for each
    operator. In exact mode, the statevector prepared by the quantum circuit is
    simulated separately for each operator. This is required so that the
    standard ``get_exact_expectation_values`` method of the ``QuantumBackend``
    interface can be used.

    Args:
        backend (QuantumBackend): the Orquestra quantum backend to use
        circuit (zquantum.core.circuit.Circuit): the circuit represented as an
            OpenQASM 2.0 program
        operators (list): a list of operators as ``openfermion.QubitOperator``
            or ``openfermion.IsingOperator`` objects

    Returns:
        list: list of expectation values for each operator
    """
    results = []

    if backend.n_samples is not None:
        measurements = backend.run_circuit_and_measure(circuit)

        # Iterating through the operators specified e.g., [IsingOperator("[Z0]
        # + [Z1]"), IsingOperator("[Z1]")] to post-process the measurements
        # outcomes
        for op in ops:
            expectation_values = measurements.get_expectation_values(op)
            expectation_values = expectation_values_to_real(expectation_values)

            # Summing the expectation values obtained for each term of the
            # operator yields the expectation value for the operator
            # E.g., <psi|Z0 + Z1|psi> = <psi|Z0|psi> + <psi|Z1|psi>
            val = np.sum(expectation_values.values)
            results.append(val)
    else:
        for op in ops:
            expectation_values = backend.get_exact_expectation_values(circuit, op)

            val = np.sum(expectation_values.values)
            results.append(val)

    return results
