pennylane_orquestra.QeQiskitDevice
==================================

.. currentmodule:: pennylane_orquestra

.. autoclass:: QeQiskitDevice
   :show-inheritance:

   .. raw:: html

      <a class="attr-details-header collapse-header" data-toggle="collapse" href="#attrDetails" aria-expanded="false" aria-controls="attrDetails">
         <h2 style="font-size: 24px;">
            <i class="fas fa-angle-down rotate" style="float: right;"></i> Attributes
         </h2>
      </a>
      <div class="collapse" id="attrDetails">

   .. autosummary::
      :nosignatures:

      ~QeQiskitDevice.author
      ~QeQiskitDevice.backend_specs
      ~QeQiskitDevice.cache
      ~QeQiskitDevice.circuit_hash
      ~QeQiskitDevice.filenames
      ~QeQiskitDevice.latest_id
      ~QeQiskitDevice.name
      ~QeQiskitDevice.num_executions
      ~QeQiskitDevice.obs_queue
      ~QeQiskitDevice.observables
      ~QeQiskitDevice.op_queue
      ~QeQiskitDevice.operations
      ~QeQiskitDevice.parameters
      ~QeQiskitDevice.pennylane_requires
      ~QeQiskitDevice.qe_component
      ~QeQiskitDevice.qe_function_name
      ~QeQiskitDevice.qe_module_name
      ~QeQiskitDevice.short_name
      ~QeQiskitDevice.shots
      ~QeQiskitDevice.state
      ~QeQiskitDevice.version
      ~QeQiskitDevice.wire_map
      ~QeQiskitDevice.wires

   .. autoattribute:: author
   .. autoattribute:: backend_specs
   .. autoattribute:: cache
   .. autoattribute:: circuit_hash
   .. autoattribute:: filenames
   .. autoattribute:: latest_id
   .. autoattribute:: name
   .. autoattribute:: num_executions
   .. autoattribute:: obs_queue
   .. autoattribute:: observables
   .. autoattribute:: op_queue
   .. autoattribute:: operations
   .. autoattribute:: parameters
   .. autoattribute:: pennylane_requires
   .. autoattribute:: qe_component
   .. autoattribute:: qe_function_name
   .. autoattribute:: qe_module_name
   .. autoattribute:: short_name
   .. autoattribute:: shots
   .. autoattribute:: state
   .. autoattribute:: version
   .. autoattribute:: wire_map
   .. autoattribute:: wires

   .. raw:: html

      </div>

   .. raw:: html

      <a class="meth-details-header collapse-header" data-toggle="collapse" href="#methDetails" aria-expanded="false" aria-controls="methDetails">
         <h2 style="font-size: 24px;">
            <i class="fas fa-angle-down rotate" style="float: right;"></i> Methods
         </h2>
      </a>
      <div class="collapse" id="methDetails">

   .. autosummary::

      ~QeQiskitDevice.access_state
      ~QeQiskitDevice.active_wires
      ~QeQiskitDevice.analytic_probability
      ~QeQiskitDevice.apply
      ~QeQiskitDevice.batch_execute
      ~QeQiskitDevice.capabilities
      ~QeQiskitDevice.check_validity
      ~QeQiskitDevice.create_backend_specs
      ~QeQiskitDevice.define_wire_map
      ~QeQiskitDevice.density_matrix
      ~QeQiskitDevice.estimate_probability
      ~QeQiskitDevice.execute
      ~QeQiskitDevice.execution_context
      ~QeQiskitDevice.expval
      ~QeQiskitDevice.generate_basis_states
      ~QeQiskitDevice.generate_samples
      ~QeQiskitDevice.map_wires
      ~QeQiskitDevice.marginal_prob
      ~QeQiskitDevice.pauliz_operator_string
      ~QeQiskitDevice.post_apply
      ~QeQiskitDevice.post_measure
      ~QeQiskitDevice.pre_apply
      ~QeQiskitDevice.pre_measure
      ~QeQiskitDevice.probability
      ~QeQiskitDevice.process_observables
      ~QeQiskitDevice.qubit_operator_string
      ~QeQiskitDevice.reset
      ~QeQiskitDevice.sample
      ~QeQiskitDevice.sample_basis_states
      ~QeQiskitDevice.serialize_circuit
      ~QeQiskitDevice.serialize_operator
      ~QeQiskitDevice.states_to_binary
      ~QeQiskitDevice.statistics
      ~QeQiskitDevice.supports_observable
      ~QeQiskitDevice.supports_operation
      ~QeQiskitDevice.var

   .. automethod:: access_state
   .. automethod:: active_wires
   .. automethod:: analytic_probability
   .. automethod:: apply
   .. automethod:: batch_execute
   .. automethod:: capabilities
   .. automethod:: check_validity
   .. automethod:: create_backend_specs
   .. automethod:: define_wire_map
   .. automethod:: density_matrix
   .. automethod:: estimate_probability
   .. automethod:: execute
   .. automethod:: execution_context
   .. automethod:: expval
   .. automethod:: generate_basis_states
   .. automethod:: generate_samples
   .. automethod:: map_wires
   .. automethod:: marginal_prob
   .. automethod:: pauliz_operator_string
   .. automethod:: post_apply
   .. automethod:: post_measure
   .. automethod:: pre_apply
   .. automethod:: pre_measure
   .. automethod:: probability
   .. automethod:: process_observables
   .. automethod:: qubit_operator_string
   .. automethod:: reset
   .. automethod:: sample
   .. automethod:: sample_basis_states
   .. automethod:: serialize_circuit
   .. automethod:: serialize_operator
   .. automethod:: states_to_binary
   .. automethod:: statistics
   .. automethod:: supports_observable
   .. automethod:: supports_operation
   .. automethod:: var

   .. raw:: html

      </div>

   .. raw:: html

      <script type="text/javascript">
         $(".collapse-header").click(function () {
             $(this).children('h2').eq(0).children('i').eq(0).toggleClass("up");
         })
      </script>
