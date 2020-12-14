pennylane_orquestra.OrquestraDevice
===================================

.. currentmodule:: pennylane_orquestra

.. autoclass:: OrquestraDevice
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

      ~OrquestraDevice.author
      ~OrquestraDevice.backend_specs
      ~OrquestraDevice.cache
      ~OrquestraDevice.circuit_hash
      ~OrquestraDevice.filenames
      ~OrquestraDevice.latest_id
      ~OrquestraDevice.name
      ~OrquestraDevice.num_executions
      ~OrquestraDevice.obs_queue
      ~OrquestraDevice.observables
      ~OrquestraDevice.op_queue
      ~OrquestraDevice.operations
      ~OrquestraDevice.parameters
      ~OrquestraDevice.pennylane_requires
      ~OrquestraDevice.qe_component
      ~OrquestraDevice.qe_function_name
      ~OrquestraDevice.qe_module_name
      ~OrquestraDevice.short_name
      ~OrquestraDevice.shots
      ~OrquestraDevice.state
      ~OrquestraDevice.version
      ~OrquestraDevice.wire_map
      ~OrquestraDevice.wires

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

      ~OrquestraDevice.access_state
      ~OrquestraDevice.active_wires
      ~OrquestraDevice.analytic_probability
      ~OrquestraDevice.apply
      ~OrquestraDevice.batch_execute
      ~OrquestraDevice.capabilities
      ~OrquestraDevice.check_validity
      ~OrquestraDevice.create_backend_specs
      ~OrquestraDevice.define_wire_map
      ~OrquestraDevice.density_matrix
      ~OrquestraDevice.estimate_probability
      ~OrquestraDevice.execute
      ~OrquestraDevice.execution_context
      ~OrquestraDevice.expval
      ~OrquestraDevice.generate_basis_states
      ~OrquestraDevice.generate_samples
      ~OrquestraDevice.map_wires
      ~OrquestraDevice.marginal_prob
      ~OrquestraDevice.pauliz_operator_string
      ~OrquestraDevice.post_apply
      ~OrquestraDevice.post_measure
      ~OrquestraDevice.pre_apply
      ~OrquestraDevice.pre_measure
      ~OrquestraDevice.probability
      ~OrquestraDevice.process_observables
      ~OrquestraDevice.qubit_operator_string
      ~OrquestraDevice.reset
      ~OrquestraDevice.sample
      ~OrquestraDevice.sample_basis_states
      ~OrquestraDevice.serialize_circuit
      ~OrquestraDevice.serialize_operator
      ~OrquestraDevice.states_to_binary
      ~OrquestraDevice.statistics
      ~OrquestraDevice.supports_observable
      ~OrquestraDevice.supports_operation
      ~OrquestraDevice.var

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
