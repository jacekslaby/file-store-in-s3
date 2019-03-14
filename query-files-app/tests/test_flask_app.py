from queryfilesapp import extract_param_from_request
from queryfilesapp import get_domains_with_files
from queryfilesapp import get_file_download
import pytest
from unittest.mock import patch


# Unit tests of a single method:  extract_param_from_request(...)
# Testing is done using several input scenarios,
#   i.e. there are many runs of the tested method,
#   with different input parameters and with different expected result verified after an execution.
# (see also https://docs.pytest.org/en/latest/example/parametrize.html#paramexamples )
#
@pytest.mark.parametrize("param_name, request_args, expected", [
    ('read_domain_regex', {'read_domain_regex': 'alos'}, 'alos')         # Scenario: attribute is correctly provided
])
def test_extract_param_from_request(param_name, request_args, expected):

    result = extract_param_from_request(param_name, request_args)
    assert result == expected


@pytest.mark.parametrize("param_name, request_args, expected", [
    ('read_domain_regex', {'other': 'alos'}, pytest.raises(ValueError)),  # Scenario: attribute is not provided
    ('read_domain_regex', {}, pytest.raises(ValueError))                  # Scenario: attribute is not provided
])
def test_failed_extract_param_from_request(param_name, request_args, expected):

    with expected:
        _ = extract_param_from_request(param_name, request_args)


@patch('queryfilesapp.request')
@patch('queryfilesapp.jsonify')
@patch('queryfilesapp.s3_file_store.get_domains_with_files')
def test_get_domains_with_files(get_domains_with_files_mock, _, request_mock):
    """Verify that correct parameters are extracted from HTTP request and passed to s3_file_store module."""

    # Stub a result which does not matter here. (because module s3_file_store has own unit tests)
    get_domains_with_files_mock.return_value = {}
    # This 'alos' string is expected to be passed as parameter in a call to a method from s3_file_store.
    request_mock.args = {'read_domain_regex': 'alos'}

    # call tested method
    get_domains_with_files()

    get_domains_with_files_mock.assert_called_with('alos')


@patch('queryfilesapp.request')
@patch('queryfilesapp.jsonify')
@patch('queryfilesapp.s3_file_store.get_file_download')
def test_get_file_download(get_file_download_mock, _, request_mock):
    """Verify that correct parameters are extracted from HTTP request and passed to s3_file_store module."""

    # Stub a result which does not matter here. (because module s3_file_store has own unit tests)
    get_file_download_mock.return_value = {'download_url': 'dummy'}
    # These strings are expected to be provided as parameters in a call to a method from s3_file_store.
    request_mock.args = {'read_domain_regex': 'alos|bp', 'domain_name': 'alos', 'file_name': 'file1'}

    # call tested method
    get_file_download()

    get_file_download_mock.assert_called_with('alos|bp', 'alos', 'file1')
