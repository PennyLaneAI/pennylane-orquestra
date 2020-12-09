import pytest
import subprocess

import yaml
import pennylane_orquestra.gen_workflow as gw
from pennylane_orquestra.cli_actions import qe_submit

from conftest import (
    resources_default,
    backend_specs_default,
    qasm_circuit_default,
    operator_string_default,
    test_workflow,
    test_workflow_resources,
    qe_list_workflow,
)

def compare_two_expval_steps(stepA, stepB):
    """Compares two steps used to compute expectation values."""
    assert stepA["name"] == stepB["name"]
    assert stepA["config"] == stepB["config"]

    # Checking the inputs: part by part
    assert (
        stepA["inputs"][0]["backend_specs"]
        == stepB["inputs"][0]["backend_specs"]
    )
    assert (
        stepA["inputs"][1]["operators"]
        == stepB["inputs"][1]["operators"]
    )
    assert (
        stepA["inputs"][2]["circuit"]
        == stepB["inputs"][2]["circuit"]
    )

    # Check the inputs as a whole
    assert stepA["inputs"] == stepB["inputs"]

    # Checking the outputs
    assert stepA["outputs"] == stepB["outputs"]

class TestExpvalTemplate:
    """Test that workflow generation works as expected."""

    def test_can_yaml(self, tmpdir):
        """Test that filling in the workflow template for getting expectation
        values produces a valid yaml."""
        backend_component = "qe-forest"

        # Fill in workflow template
        workflow = gw.gen_expval_workflow(
            backend_component, backend_specs_default, qasm_circuit_default, operator_string_default
        )

        file_name = tmpdir.join("test_workflow.yaml")

        with open(file_name, "w") as file:
            # Testing that no errors arise here
            d = yaml.dump(workflow, file)

    def test_unsupported_backend_component(self):
        """Test that if an unsupported backend component is input then an error is raised."""
        backend_component = "SomeNonExistentBackend"

        # Fill in workflow template
        with pytest.raises(ValueError, match="The specified backend component is not supported."):
            workflow = gw.gen_expval_workflow(
                backend_component,
                backend_specs_default,
                qasm_circuit_default,
                operator_string_default,
            )

    @pytest.mark.parametrize(
        "resources, test_wf", [(None, test_workflow), (resources_default, test_workflow_resources)]
    )
    def test_matches_template(self, resources, test_wf):
        """Test that generating a two-step workflow matches the pre-defined
        template."""
        backend_component = "qe-forest"

        # Fill in workflow template
        circuits = [qasm_circuit_default, qasm_circuit_default]
        workflow = gw.gen_expval_workflow(
            backend_component,
            backend_specs_default,
            circuits,
            operator_string_default,
            resources=resources,
        )

        assert workflow["apiVersion"] == test_wf["apiVersion"]
        assert workflow["name"] == test_wf["name"]
        assert workflow["imports"] == test_wf["imports"]

        compare_two_expval_steps(workflow["steps"][0], test_wf["steps"][0])
        compare_two_expval_steps(workflow["steps"][1], test_wf["steps"][1])
        assert workflow == test_wf
