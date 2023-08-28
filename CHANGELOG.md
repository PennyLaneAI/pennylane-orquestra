# Release 0.32.0

### Improvements 🛠

* Add support for `qml.StatePrep` as a state preparation operation.
  [(#39)](https://github.com/PennyLaneAI/pennylane-orquestra/pull/39)

### Breaking changes 💔

* Support for Python 3.8 has been removed, and support for Python 3.11 has been added.
  [(#40)](https://github.com/PennyLaneAI/pennylane-orquestra/pull/40)

### Contributors ✍️

This release contains contributions from (in alphabetical order):

Mudit Pandey,
Jay Soni

---

# Release 0.28.0

### Bug fixes 
* Update plugin to remove the use of `decompose_hamiltonian` in favour of `pauli_decompose`. [(#34)](https://github.com/PennyLaneAI/pennylane-orquestra/pull/34)

### Contributors

This release contains contributions from (in alphabetical order):

Jay Soni, Antal Száva

---

# Release 0.22.0

### Bug fixes

* Changes the `batch_execute` method to support executing single tapes as per
  PennyLane `v0.20.0` where batch execution is the default for a QNode.
  [(#22)](https://github.com/XanaduAI/pennylane-orquestra/pull/22)

* Fixes issues that came from updates with `v0.22.0` PennyLane and in the
  Z-Quantum libraries.
  [(#22)](https://github.com/XanaduAI/pennylane-orquestra/pull/22)

### Contributors

This release contains contributions from (in alphabetical order):

Sam Banning, Antal Száva

---

# Release 0.15.0

### Breaking changes

* For compatibility with PennyLane v0.15, the `analytic` keyword argument
  has been removed from all devices. Analytic expectation values can
  still be computed by setting `shots=None`.
  [(#16)](https://github.com/XanaduAI/pennylane-orquestra/pull/16)

### Contributors

This release contains contributions from (in alphabetical order):

Josh Izaac, Antal Száva.

---

# Release 0.14.0

### Improvements

* Updated the test suite for environments with IBMQX tokens and for the new
  core of PennyLane.
  [(#14)](https://github.com/PennyLaneAI/pennylane-orquestra/pull/14/files)
  [(#17)](https://github.com/PennyLaneAI/pennylane-orquestra/pull/17/files)

This release contains contributions from (in alphabetical order):

Josh Izaac, Antal Száva.

# Release 0.13.1

### Bug fixes

* Fixed a bug related to building the wheel.
  [(#13)](https://github.com/PennyLaneAI/pennylane-orquestra/pull/13)

### Contributors

This release contains contributions from (in alphabetical order):

Antal Száva.

---

# Release 0.13.0

Initial release.

This release contains contributions from (in alphabetical order):

Chase Roberts, Alain Delgado Gran, Theodor Isacsson, Josh Izaac, Nathan
Killoran, Antal Száva.
