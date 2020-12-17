IBMQ device
===========
PennyLane-Orquestra supports running PennyLane on IBM Q hardware via the ``qistkit.ibmq`` device.
You can choose between different backends --- either simulators tailor-made to emulate the real hardware,
or the real hardware itself.

IBMQX Tokens
~~~~~~~~~~~~

The ``orquestra.ibmq`` device will use an IBMQ API token directly passed to the device:

.. code-block:: python

    dev = qml.device('orquestra.ibmq', wires=2, backend='ibmq_qasm_simulator', ibmqx_token="XXX")


.. warning:: Never publish code containing your token online.

Backends
~~~~~~~~

By default, the ``orquestra.ibmq`` device uses the simulator backend
``ibmq_qasm_simulator``, but this may be changed to any of the real backends.

Most of the backends of the ``orquestra.ibmq`` device, such as ``ibmq_london``
or ``ibmq_16_melbourne``, are *hardware backends*. Running PennyLane with these
backends means that the circuit is sent as a job to the actual quantum computer and the results are retrieved via the cloud and Orquestra.
