pennylane_orquestra.QeQulacsDevice
==================================

.. currentmodule:: pennylane_orquestra

.. autoclass:: QeQulacsDevice
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

      ~QeQulacsDevice.author
      ~QeQulacsDevice.backend_specs
      ~QeQulacsDevice.cache
      ~QeQulacsDevice.circuit_hash
      ~QeQulacsDevice.filenames
      ~QeQulacsDevice.latest_id
      ~QeQulacsDevice.name
      ~QeQulacsDevice.num_executions
      ~QeQulacsDevice.obs_queue
      ~QeQulacsDevice.observables
      ~QeQulacsDevice.op_queue
      ~QeQulacsDevice.operations
      ~QeQulacsDevice.parameters
      ~QeQulacsDevice.pennylane_requires
      ~QeQulacsDevice.qe_component
      ~QeQulacsDevice.qe_function_name
      ~QeQulacsDevice.qe_module_name
      ~QeQulacsDevice.short_name
      ~QeQulacsDevice.shots
      ~QeQulacsDevice.state
      ~QeQulacsDevice.version
      ~QeQulacsDevice.wire_map
      ~QeQulacsDevice.wires

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

      ~QeQulacsDevice.access_state
      ~QeQulacsDevice.active_wires
      ~QeQulacsDevice.analytic_probability
      ~QeQulacsDevice.apply
      ~QeQulacsDevice.batch_execute
      ~QeQulacsDevice.capabilities
      ~QeQulacsDevice.check_validity
      ~QeQulacsDevice.create_backend_specs
      ~QeQulacsDevice.define_wire_map
      ~QeQulacsDevice.density_matrix
      ~QeQulacsDevice.estimate_probability
      ~QeQulacsDevice.execute
      ~QeQulacsDevice.execution_context
      ~QeQulacsDevice.expval
      ~QeQulacsDevice.generate_basis_states
      ~QeQulacsDevice.generate_samples
      ~QeQulacsDevice.map_wires
      ~QeQulacsDevice.marginal_prob
      ~QeQulacsDevice.pauliz_operator_string
      ~QeQulacsDevice.post_apply
      ~QeQulacsDevice.post_measure
      ~QeQulacsDevice.pre_apply
      ~QeQulacsDevice.pre_measure
      ~QeQulacsDevice.probability
      ~QeQulacsDevice.process_observables
      ~QeQulacsDevice.qubit_operator_string
      ~QeQulacsDevice.reset
      ~QeQulacsDevice.sample
      ~QeQulacsDevice.sample_basis_states
      ~QeQulacsDevice.serialize_circuit
      ~QeQulacsDevice.serialize_operator
      ~QeQulacsDevice.states_to_binary
      ~QeQulacsDevice.statistics
      ~QeQulacsDevice.supports_observable
      ~QeQulacsDevice.supports_operation
      ~QeQulacsDevice.var

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
