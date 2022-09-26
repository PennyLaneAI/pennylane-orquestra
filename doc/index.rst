PennyLane-Orquestra Plugin
##########################

:Release: |release|

.. include:: ../README.rst
  :start-after:	header-start-inclusion-marker-do-not-remove
  :end-before: header-end-inclusion-marker-do-not-remove


Once the PennyLane-Orquestra plugin is installed, multiple devices offered by
Orquestra can be accessed straightaway in PennyLane, without the need to import
new packages.

Devices
~~~~~~~

There are four different devices available:

.. title-card::
    :name: 'orquestra.forest'
    :description: Integration with Rigetti Forest devices.
    :link: devices/forest.html

.. title-card::
    :name: 'orquestra.ibmq'
    :description: Integration with Qiskit remote hardware and simulators.
    :link: devices/ibmq.html

.. title-card::
    :name: 'orquestra.qiskit'
    :description: Integration with Qiskit simulator backends.
    :link: devices/qiskit.html

.. title-card::
    :name: 'orquestra.qulacs'
    :description: Integration with the Qulacs simulator.
    :link: devices/qulacs.html

.. raw:: html

        <div style='clear:both'></div>
        </br>

For example, the ``'orquestra.qiskit'`` device with two wires is called like this:

.. code-block:: python

    import pennylane as qml
    dev = qml.device('orquestra.qiskit', wires=2)

Device options
~~~~~~~~~~~~~~

The devices provided by the PennyLane-Orquestra plugin accept additional
arguments beyond the PennyLane default device arguments. These are added to a
base :class:`~.OrquestraDevice` class.

``backend=None``
    The Orquestra backend device to use for the specific Orquestra backend, if
    applicable (e.g., ``'statevector_simulator'`` for ``'orquestra.qiskit'``)

``batch_size=10``
    The size of each circuit batch when using the
    :meth:`~.OrquestraDevice.batch_execute` method to send multiple workflows.

``keep_files=False``
    Whether or not the workflow files generated during the circuit execution should
    be kept or deleted.

``resources=None``
    An option for Orquestra, specifies the resources to be specified for each
    workflow step.

``timeout=600``
    The time until a job should timeout after getting no response from
    Orquestra (in seconds).

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :hidden:

   installation
   support

.. toctree::
   :maxdepth: 2
   :caption: Usage
   :hidden:

   devices/forest
   devices/ibmq
   devices/qiskit
   devices/qulacs

.. toctree::
   :maxdepth: 1
   :caption: API
   :hidden:

   code
