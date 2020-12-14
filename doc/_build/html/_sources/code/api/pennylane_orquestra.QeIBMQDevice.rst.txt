pennylane_orquestra.QeIBMQDevice
================================

.. currentmodule:: pennylane_orquestra

.. autoclass:: QeIBMQDevice
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

      ~QeIBMQDevice.author
      ~QeIBMQDevice.backend_specs
      ~QeIBMQDevice.cache
      ~QeIBMQDevice.circuit_hash
      ~QeIBMQDevice.filenames
      ~QeIBMQDevice.latest_id
      ~QeIBMQDevice.name
      ~QeIBMQDevice.num_executions
      ~QeIBMQDevice.obs_queue
      ~QeIBMQDevice.observables
      ~QeIBMQDevice.op_queue
      ~QeIBMQDevice.operations
      ~QeIBMQDevice.parameters
      ~QeIBMQDevice.pennylane_requires
      ~QeIBMQDevice.qe_component
      ~QeIBMQDevice.qe_function_name
      ~QeIBMQDevice.qe_module_name
      ~QeIBMQDevice.short_name
      ~QeIBMQDevice.shots
      ~QeIBMQDevice.state
      ~QeIBMQDevice.version
      ~QeIBMQDevice.wire_map
      ~QeIBMQDevice.wires

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

      ~QeIBMQDevice.access_state
      ~QeIBMQDevice.active_wires
      ~QeIBMQDevice.analytic_probability
      ~QeIBMQDevice.apply
      ~QeIBMQDevice.batch_execute
      ~QeIBMQDevice.capabilities
      ~QeIBMQDevice.check_validity
      ~QeIBMQDevice.create_backend_specs
      ~QeIBMQDevice.define_wire_map
      ~QeIBMQDevice.density_matrix
      ~QeIBMQDevice.estimate_probability
      ~QeIBMQDevice.execute
      ~QeIBMQDevice.execution_context
      ~QeIBMQDevice.expval
      ~QeIBMQDevice.generate_basis_states
      ~QeIBMQDevice.generate_samples
      ~QeIBMQDevice.map_wires
      ~QeIBMQDevice.marginal_prob
      ~QeIBMQDevice.pauliz_operator_string
      ~QeIBMQDevice.post_apply
      ~QeIBMQDevice.post_measure
      ~QeIBMQDevice.pre_apply
      ~QeIBMQDevice.pre_measure
      ~QeIBMQDevice.probability
      ~QeIBMQDevice.process_observables
      ~QeIBMQDevice.qubit_operator_string
      ~QeIBMQDevice.reset
      ~QeIBMQDevice.sample
      ~QeIBMQDevice.sample_basis_states
      ~QeIBMQDevice.serialize_circuit
      ~QeIBMQDevice.serialize_operator
      ~QeIBMQDevice.states_to_binary
      ~QeIBMQDevice.statistics
      ~QeIBMQDevice.supports_observable
      ~QeIBMQDevice.supports_operation
      ~QeIBMQDevice.var

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
