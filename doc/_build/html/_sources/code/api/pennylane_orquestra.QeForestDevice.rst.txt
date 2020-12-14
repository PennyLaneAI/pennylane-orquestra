pennylane_orquestra.QeForestDevice
==================================

.. currentmodule:: pennylane_orquestra

.. autoclass:: QeForestDevice
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

      ~QeForestDevice.author
      ~QeForestDevice.backend_specs
      ~QeForestDevice.cache
      ~QeForestDevice.circuit_hash
      ~QeForestDevice.filenames
      ~QeForestDevice.latest_id
      ~QeForestDevice.name
      ~QeForestDevice.num_executions
      ~QeForestDevice.obs_queue
      ~QeForestDevice.observables
      ~QeForestDevice.op_queue
      ~QeForestDevice.operations
      ~QeForestDevice.parameters
      ~QeForestDevice.pennylane_requires
      ~QeForestDevice.qe_component
      ~QeForestDevice.qe_function_name
      ~QeForestDevice.qe_module_name
      ~QeForestDevice.short_name
      ~QeForestDevice.shots
      ~QeForestDevice.state
      ~QeForestDevice.version
      ~QeForestDevice.wire_map
      ~QeForestDevice.wires

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

      ~QeForestDevice.access_state
      ~QeForestDevice.active_wires
      ~QeForestDevice.analytic_probability
      ~QeForestDevice.apply
      ~QeForestDevice.batch_execute
      ~QeForestDevice.capabilities
      ~QeForestDevice.check_validity
      ~QeForestDevice.create_backend_specs
      ~QeForestDevice.define_wire_map
      ~QeForestDevice.density_matrix
      ~QeForestDevice.estimate_probability
      ~QeForestDevice.execute
      ~QeForestDevice.execution_context
      ~QeForestDevice.expval
      ~QeForestDevice.generate_basis_states
      ~QeForestDevice.generate_samples
      ~QeForestDevice.map_wires
      ~QeForestDevice.marginal_prob
      ~QeForestDevice.pauliz_operator_string
      ~QeForestDevice.post_apply
      ~QeForestDevice.post_measure
      ~QeForestDevice.pre_apply
      ~QeForestDevice.pre_measure
      ~QeForestDevice.probability
      ~QeForestDevice.process_observables
      ~QeForestDevice.qubit_operator_string
      ~QeForestDevice.reset
      ~QeForestDevice.sample
      ~QeForestDevice.sample_basis_states
      ~QeForestDevice.serialize_circuit
      ~QeForestDevice.serialize_operator
      ~QeForestDevice.states_to_binary
      ~QeForestDevice.statistics
      ~QeForestDevice.supports_observable
      ~QeForestDevice.supports_operation
      ~QeForestDevice.var

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
