# Release 0.15.0

### Breaking changes

* For compatibility with PennyLane v0.15, the `analytic` keyword argument
  has been removed from all devices. Analytic expectation values can
  still be computed by setting `shots=None`.
  [(#16)](https://github.com/XanaduAI/pennylane-orquestra/pull/16)

### Contributors

This release contains contributions from (in alphabetical order):

Josh Izaac

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
