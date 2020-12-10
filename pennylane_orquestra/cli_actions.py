"""
This module contains utilities and auxiliary functions for using the Orquestra
Quantum Engine command line interface (CLI).
"""
import subprocess
import time
import os
import urllib.request
import json
import tarfile

import yaml
from appdirs import user_data_dir


def qe_get(workflow_id, option="workflow"):
    """Function for getting information via an Orquestra Quantum Engine CLI
    call.

    This function is mostly used for retrieving workflow related information.

    Args:
        workflow_id (str): the workflow id for which information will be
            retrieved

    Kwargs:
        option (str): The option specified for the ``qe get`` CLI call.
            Examples include ``workflow`` and ``workflowresult``.

    Returns:
        str: response message of the CLI call
    """
    process = subprocess.Popen(
        ["qe", "get", option, str(workflow_id)], stdout=subprocess.PIPE, universal_newlines=True
    )
    return process.stdout.readlines()


def qe_submit(filepath, keep_file=False):
    """Function for submitting a workflow via a CLI call.

    Handling submission response messages was based on using Orquestra API
    v1.0.0.

    Args:
        filepath (str): the filepath for the workflow file

    Keyword Args:
        keep_file=False (bool): whether or not to keep or delete the workflow
            file after submission

    Returns:
        str: the ID of the workflow submitted

    Raises:
        ValueError: if the submission was not successful
    """
    process = subprocess.Popen(
        ["qe", "submit", "workflow", str(filepath)], stdout=subprocess.PIPE, universal_newlines=True
    )
    res = process.stdout.readlines()

    details = "".join(res)
    if "Success" not in details:
        raise ValueError(res)

    if not keep_file:
        os.remove(filepath)

    unexpected_resp_msg = "Received an unexpected response after submitting workflow."
    if isinstance(res, list):
        try:
            # Get the workflow ID after submitting a workflow
            workflow_id = res[1].split()[-1]
        except IndexError as e:
            raise ValueError(unexpected_resp_msg) from e
    else:
        raise ValueError(unexpected_resp_msg)

    return workflow_id


def workflow_details(workflow_id):
    """Function for getting workflow details via a CLI call.

    Args:
        workflow_id (str): the workflow id for which information will be
            retrieved

    Returns:
        str: response message of the CLI call
    """
    return qe_get(workflow_id, option="workflow")


def workflow_results(workflow_id):
    """Function for getting workflow results via a CLI call.

    Args:
        workflow_id (str): the workflow id for which information will be
            retrieved

    Kwargs:
        option (str): The option specified for the ``qe get`` CLI call.
            Examples include ``workflow`` and ``workflowresult``.

    Returns:
        str: response message of the CLI call
    """
    return qe_get(workflow_id, option="workflowresult")


def write_workflow_file(filename, workflow):
    """Write a workflow file given the name of the file.

    This function will create a YAML file with the workflow content. The file
    is placed into a user specific data folder specified by using
    ``appdirs.user_data_dir``.

    Args:
        filename (str): the name of the file to write
        workflow (dict): the workflow generated as a dictionary
    """
    # Get the directory to write the file to
    directory = user_data_dir("pennylane-orquestra", "Xanadu")

    # Create target Directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    filepath = os.path.join(directory, filename)

    with open(filepath, "w") as file:
        # The order of the keys within the YAML file is pre-defined for Orquestra,
        # hence need to keep the order
        yaml.dump(workflow, file, sort_keys=False)

    return filepath


def loop_until_finished(workflow_id, timeout=300):
    """Loops until the workflow execution has finished by querying workflow
    details using the workflow ID.

    The flows of messages and the checks were based on responses obtained when
    using Orquestra API v1.0.0.

    Args:
        workflow_id (str): the ID of the workflow for which to return the
            results

    Keyword args:
        timeout (int): seconds to wait until raising a TimeoutError

    Returns:
        dict: the resulting dictionary parsed from a json file
    """
    start = time.time()
    query_results = True
    tries = 0
    while query_results:
        tries += 1

        # Check if we've exceeded the timeout time, otherwise loop further
        if time.time() - start > timeout:
            current_status = workflow_details(workflow_id)
            raise TimeoutError(
                f"The workflow results for workflow "
                f"{workflow_id} were not obtained after {timeout/60} minutes. "
                f"{current_status}"
            )

        if tries % 20 == 0:

            # Check if the status shows that the workflow failed, after a
            # certain number of tries
            status = workflow_details(workflow_id)
            details_string = "".join(status).split()
            if "Failed" in details_string:
                raise ValueError(f"Something went wrong with executing the workflow. {status}")

        results = workflow_results(workflow_id)

        # 1. Attempt to extract a location
        try:
            # Assume that the second line of the message contains the URL
            location = results[1].split()[1]
        except IndexError:
            # The format of the results were not like the message with URL
            continue

        # 2. Check that the location is a valid URL
        try:

            # We expect that this fails if an invalid URL location was outputted
            urllib.request.urlopen(location)

            # If we managed to get the URL, we can stop querying
            query_results = False

        except urllib.error.URLError:
            continue

    # 3. Obtain the data from the URL
    # Seting filename=None will treat the file as temporary and it will be
    # removed
    file_tmp = urllib.request.urlretrieve(location, filename=None)[0]
    if tarfile.is_tarfile(file_tmp):
        tar = tarfile.open(file_tmp, "r:gz")
        tar.extractall()
        tar.close()

        with open("workflow_result.json") as json_file:
            data = json.load(json_file)

    return data
