PennyLane-Orquestra Plugin
##########################

.. image:: https://img.shields.io/github/workflow/status/PennyLaneAI/pennylane-orquestra/Tests/master?logo=github&style=flat-square
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/PennyLaneAI/pennylane-orquestra/actions?query=workflow%3ATests

.. image:: https://img.shields.io/codecov/c/github/PennyLaneAI/pennylane-orquestra/master.svg?logo=codecov&style=flat-square
    :alt: Codecov coverage
    :target: https://codecov.io/gh/PennyLaneAI/pennylane-orquestra

.. image:: https://img.shields.io/codefactor/grade/github/PennyLaneAI/pennylane-orquestra/master?logo=codefactor&style=flat-square
    :alt: CodeFactor Grade
    :target: https://www.codefactor.io/repository/github/pennylaneai/pennylane-orquestra

.. image:: https://img.shields.io/readthedocs/pennylane-orquestra.svg?logo=read-the-docs&style=flat-square
    :alt: Read the Docs
    :target: https://pennylaneorquestra.readthedocs.io

.. image:: https://img.shields.io/pypi/v/PennyLane-orquestra.svg?style=flat-square
    :alt: PyPI
    :target: https://pypi.org/project/PennyLane-orquestra

.. image:: https://img.shields.io/pypi/pyversions/PennyLane-orquestra.svg?style=flat-square
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/PennyLane-orquestra

.. header-start-inclusion-marker-do-not-remove

The PennyLane-Orquestra plugin integrates the Orquestra workflow management
system for quantum computing with PennyLane's quantum machine learning
capabilities.

`PennyLane <https://pennylane.readthedocs.io>`_ is a cross-platform Python
library for `differentiable programming
<https://en.wikipedia.org/wiki/Differentiable_programming>`_ of quantum
computers.

`Orquestra <https://www.orquestra.io/>`_ is a workflow management system for quantum computing.

.. header-end-inclusion-marker-do-not-remove

Features
========

* Provides four devices to be used with PennyLane: ``orquestra.forest``,
  ``orquestra.ibmq``, ``orquestra.orquestra`` and ``orquestra.qulacs``.
  These devices provide access to the various backends and simulators,
  including hardware devices like the IBM hardware accessible through the
  cloud.

* Allows computing expectation values by submitting and processing Orquestra
  workflows.

* Supports a wide range of PennyLane operations.

* Combines Orquestra's execution capabilities to submit batches of circuits
  that can be executed in parallel.

.. installation-start-inclusion-marker-do-not-remove

Installation
============

Folder structure of the plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The source folder of the plugin contains sub-folders for both server and
client-side code:

1. *Server-side*: the ``steps`` subfolder contains the functions used in
   generated workflows as steps and the ``src`` subfolder contains further
   server-side auxiliary code (if any). Orquestra imports the ``main`` branch
   of the ``pennylane-orquestra`` repository on each workflow submission, so
   server-side changes merged into the ``main`` branch take effect immediately.

2. *Client-side*: the ``pennylane_orquestra`` subfolder contains client-side
   code making up the PennyLane-Orquestra plugin.

Installation and tests
~~~~~~~~~~~~~~~~~~~~~~

This plugin requires Python version 3.6 and above. PennyLane and the `Quantum Engine CLI <https://github.com/zapatacomputing/qe-cli>`_ are also required.
Installation of this plugin, as well as all dependencies, can be done using ``pip``:

.. code-block:: bash

    pip install pennylane-orquestra

To test that the PennyLane-Orquestra plugin is working correctly you can run

.. code-block:: bash

    make test

in the source folder. Tests that involve submitting Orquestra workflows to test
the end-to-end integration of the plugin can be run with ``make test-e2e``.

.. note::

    Tests on the `IBMQ device
    <https://pennylaneorquestra.readthedocs.io/en/latest/devices/ibmq.html>`_
    can only be run if an IBM Q authentication token is available via the ``IBMQX_TOKEN``
    environment variable for the `IBM Q experience
    <https://quantum-computing.ibm.com/>`_.

    If this is the case, running ``make test-e2e`` also executes tests on the
    ``orquestra.ibmq`` device.  By default tests on the ``orquestra.ibmq``
    device run with ``ibmq_qasm_simulator`` backend. At the time of writing
    this means that the test are "free". Please verify that this is also the
    case for your account.

Further test cases for the ``steps`` used by the PennyLane-Orquestra plugin are
located in ``steps/tests``. To run these, Python version 3.7 and above is
required along with the dependencies contained in the
``steps/requirements_for_tests.txt``. Once these are available, running ``make
test-steps`` will run the ``steps`` test suite.

.. installation-end-inclusion-marker-do-not-remove

Please refer to the `plugin documentation <https://pennylaneorquestra.readthedocs.io/>`_ as
well as to the `PennyLane documentation <https://pennylane.readthedocs.io/>`_ for further reference.

Contributing
============

We welcome contributions - simply fork the repository of this plugin, and then make a
`pull request <https://help.github.com/articles/about-pull-requests/>`_ containing your contribution.
All contributers to this plugin will be listed as authors on the releases.

We also encourage bug reports, suggestions for new features and enhancements, and even links to cool projects
or applications built on PennyLane.

Authors
=======

PennyLane-Orquestra is the work of `many contributors <https://github.com/PennyLaneAI/pennylane-orquestra/graphs/contributors>`_.

If you are doing research using PennyLane and PennyLane-Orquestra, please cite `our paper <https://arxiv.org/abs/1811.04968>`_:

    Ville Bergholm, Josh Izaac, Maria Schuld, Christian Gogolin, M. Sohaib Alam, Shahnawaz Ahmed,
    Juan Miguel Arrazola, Carsten Blank, Alain Delgado, Soran Jahangiri, Keri McKiernan, Johannes Jakob Meyer,
    Zeyue Niu, Antal Száva, and Nathan Killoran.
    *PennyLane: Automatic differentiation of hybrid quantum-classical computations.* 2018. arXiv:1811.04968

.. support-start-inclusion-marker-do-not-remove

Support
=======

- **Source Code:** https://github.com/PennyLaneAI/pennylane-orquestra
- **Issue Tracker:** https://github.com/PennyLaneAI/pennylane-orquestra/issues
- **PennyLane Forum:** https://discuss.pennylane.ai

If you are having issues, please let us know by posting the issue on our Github issue tracker, or
by asking a question in the forum.

.. support-end-inclusion-marker-do-not-remove
.. license-start-inclusion-marker-do-not-remove

License
=======

The PennyLane orquestra plugin is **free** and **open source**, released under
the `Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_.

.. license-end-inclusion-marker-do-not-remove

A package for integrating PennyLane with Orquestra.

**Installation**

Installing `PennyLane <https://github.com/PennyLaneAI/pennylane>`__ and the `Quantum Engine CLI <https://github.com/zapatacomputing/qe-cli>`__ are required.

The package can be installed using ``pip`` and running ``pip install -e .`` from
the ``pennylane_orquestra`` folder.
