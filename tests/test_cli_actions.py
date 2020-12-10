"""
Unit tests for the ```cli_actions`` module, without sending any requests to
Orquestra.
"""
import pytest
import subprocess
import tarfile
import os
import urllib.request
import json

import yaml
import pennylane_orquestra.gen_workflow as gw
import pennylane_orquestra
from pennylane_orquestra.cli_actions import qe_submit, write_workflow_file, loop_until_finished

from conftest import backend_specs_default, qasm_circuit_default, operator_string_default, MockPopen


class TestCLIFunctions:
    """Test functions for CLI actions work as expected."""

    def test_submit_raises_no_success(self, monkeypatch):
        """Test that the qe_submit method raises an error if not a successful
        message was received."""

        no_success_msg = "Not a success message."
        with monkeypatch.context() as m:
            # Disable submitting to the Orquestra platform by mocking Popen
            m.setattr(subprocess, "Popen", lambda *args, **kwargs: MockPopen(no_success_msg))

            with pytest.raises(ValueError, match=no_success_msg):
                workflow_id = qe_submit("some_filename")

    @pytest.mark.parametrize("response", [["Test Success"], "Test Success"])
    def test_submit_raises_unexpected_resp(self, monkeypatch, response):
        """Test that the qe_submit method raises an error if the workflow id
        could not be obtained."""

        unexp_resp_msg = "Received an unexpected response after submitting workflow."
        with monkeypatch.context() as m:
            # Disable submitting to the Orquestra platform by mocking Popen
            m.setattr(subprocess, "Popen", lambda *args, **kwargs: MockPopen(response))
            m.setattr(os, "remove", lambda *args, **kwargs: None)

            with pytest.raises(ValueError, match=unexp_resp_msg):
                workflow_id = qe_submit("some_filename")

    def test_workflow_results(self, monkeypatch):
        """Test that the workflow_results function passes the correct option to
        qe_get."""

        mock_results = "12345"

        def mock_qe_get(wf_id, option=None):
            if option == "workflowresult":
                return mock_results

        with monkeypatch.context() as m:
            m.setattr(pennylane_orquestra.cli_actions, "qe_get", mock_qe_get)
            res = pennylane_orquestra.cli_actions.workflow_results("Some workflow ID")
            assert res == mock_results

    def test_write_workflow_file(self, tmpdir, monkeypatch):
        """Test that filling in the workflow template for getting expectation
        values produces a valid yaml."""
        backend_component = "qe-forest"

        # Fill in workflow template
        workflow = gw.gen_expval_workflow(
            backend_component, backend_specs_default, qasm_circuit_default, operator_string_default
        )

        file_name = "test_workflow.yaml"
        with monkeypatch.context() as m:
            m.setattr(pennylane_orquestra.cli_actions, "user_data_dir", lambda *args: tmpdir)
            write_workflow_file(file_name, workflow)

        with open(tmpdir.join(file_name)) as file:
            loaded_yaml = yaml.load(file, Loader=yaml.FullLoader)

        assert workflow == loaded_yaml

    @pytest.mark.parametrize("res_msg", ["Some message2", "First line\n Second "])
    def test_loop_until_finished_raises(self, res_msg, monkeypatch):
        """Check that certain errors are raised and handled correctly by the
        loop_until_finished function."""
        with monkeypatch.context() as m:
            m.setattr(
                pennylane_orquestra.cli_actions, "workflow_details", lambda *args: "Some message1"
            )
            m.setattr(pennylane_orquestra.cli_actions, "workflow_results", lambda *args: res_msg)

            # Check that indexing into the message raises an IndexError
            # (this shows that it will be handled internally)
            with pytest.raises(IndexError, match="list index out of range"):
                location = res_msg[1].split()[1]

            # Check that looping eventually times out
            with pytest.raises(TimeoutError, match="were not obtained after"):
                loop_until_finished("Some ID", timeout=1)

    def test_loop_raises_workflow_fail(self, monkeypatch):
        """Check that an error is raised if the workflow exeuction failed."""
        with monkeypatch.context() as m:
            status = "Status:              Failed\n"
            result_message = "Some message2"

            m.setattr(pennylane_orquestra.cli_actions, "workflow_details", lambda *args: status)
            m.setattr(
                pennylane_orquestra.cli_actions,
                "workflow_results",
                lambda *args: result_message,
            )

            # Check that looping raises an error if the workflow details
            # contain a failed status
            with pytest.raises(
                ValueError, match=f"Something went wrong with executing the workflow. {status}"
            ):
                loop_until_finished("Some ID", timeout=1)

    def test_valid_url(self, monkeypatch, tmpdir):
        """Test that when receiving a valid url, data will be decoded and
        returned."""
        decoded_data = {"res": "Decoded Data"}
        test_file = os.path.join(tmpdir, "workflow_result.json")
        test_tar = os.path.join(tmpdir, "test.tgz")

        with open(test_file, "w") as outfile:
            json.dump(decoded_data, outfile)

        tar = tarfile.open(test_tar, mode="w:gz")
        tar.add(test_tar)
        tar.close()

        # Change to the test directory
        os.chdir(tmpdir)
        with monkeypatch.context() as m:
            status = "Status:              Failed\n"
            result_message = ["Some message2", "Some location"]

            m.setattr(
                pennylane_orquestra.cli_actions, "workflow_results", lambda *args: result_message
            )
            m.setattr(urllib.request, "urlopen", lambda arg: arg)
            m.setattr(urllib.request, "urlretrieve", lambda *args, **kwargs: (test_tar,))
            assert loop_until_finished("Some ID", timeout=1) == decoded_data

    def test_invalid_url_loop_till_timeout(self, monkeypatch):
        """Test that when receiving an invalid url, looping continues until the
        timeout."""
        decoded_data = "Decoded Data"

        class MockDecodableObj:
            """A mock class that can be decoded."""

            def decode(self):
                return decoded_data

        class MockURL:
            """A mock class for URLs that can serve as a context manager."""

            def __enter__(self):
                pass

            def __exit__(self, *args):
                pass

            def read(self):
                return MockDecodableObj()

        def raise_urllib_error(*args):
            """Auxiliary function that raises a URLError."""
            raise urllib.error.URLError("Test error due to an incorrect URL.")

        with monkeypatch.context() as m:
            status = "Status:              Failed\n"
            result_message = ["Some message2", "Some location"]

            m.setattr(
                pennylane_orquestra.cli_actions, "workflow_results", lambda *args: result_message
            )
            m.setattr(urllib.request, "urlopen", raise_urllib_error)

            with pytest.raises(TimeoutError, match="were not obtained after"):
                loop_until_finished("Some ID", timeout=1)
