from s3filestore.query_files import _get_domains_with_buckets
from s3filestore.query_files import _NAME_SEPARATOR
import pytest

# Data used to create test scenarios, i.e. to create inputs and expected results.
environment_name = 'it'
test_domain_names = ['shell', 'statoil', 'ca', 'bp-upstream', 'bp-downstream']


# Helper function.
def setup_test_data():
    """return a list containing tuples where each tuple represents a single test scenario"""

    def generate_bucket_name(domain_name, domain_unique_suffix):
        return environment_name + _NAME_SEPARATOR + domain_name \
               + _NAME_SEPARATOR + str(domain_unique_suffix)

    map_domain_to_bucket = {}
    for i, domain_name_str in enumerate(test_domain_names):
        map_domain_to_bucket[domain_name_str] = generate_bucket_name(domain_name_str, i)

    test_bucket_names = map_domain_to_bucket.values()

    def generate_expected(*domain_name_args):
        result = {}
        for domain_name in domain_name_args:
            result[domain_name] = map_domain_to_bucket[domain_name]
        return result

    return [
        # every tuple contains: (all_buckets_names, read_domain_regex_str, expected_mapping_of_domains_to_buckets)
        ([], 'dummy', {}),                                           # Scenario: no buckets exist in s3
        (test_bucket_names, 'shell', generate_expected('shell')),    # Scenario: user with access to 'shell' domain
        (test_bucket_names, 'shell.*', generate_expected('shell')),  # Scenario: user with access to 'shell' domains
        (test_bucket_names, 'shell|ca', generate_expected('shell', 'ca')),  # Scenario: with access to a few domains
        (test_bucket_names, 'bp.*', generate_expected('bp-upstream', 'bp-downstream')),
        (test_bucket_names, 'bp.*|ca', generate_expected('bp-upstream', 'bp-downstream', 'ca')),
        (test_bucket_names, 'alos', {}),
        (test_bucket_names, None, {})
    ]


# Variable containing test scenarios to be iterated by unit tests framework
#   when testing method _get_domains_with_buckets().
test_data_for_get_domains_with_buckets = setup_test_data()


# Unit tests of a single method:  _get_domains_with_buckets(...)
# Testing is done using several input scenarios,
#   i.e. there are many runs of the tested method,
#   with different input parameters and with different expected result verified after an execution.
# (see also https://docs.pytest.org/en/latest/example/parametrize.html#paramexamples )
#
@pytest.mark.parametrize("all_buckets_names, read_domain_regex_str, expected", test_data_for_get_domains_with_buckets)
def test_get_domains_with_buckets(all_buckets_names, read_domain_regex_str, expected):

    result = _get_domains_with_buckets(environment_name, all_buckets_names, read_domain_regex_str)
    assert result == expected


# Note: It makes little sense to add unit tests for the remaining methods of module query_files,
#  because their logic is very simple and very dependent on boto3 and access to s3.
#  So, testing them would require a lot of mocking. (and too much mocking means too much maintenance)
#  Better approach is to assume that integration tests (from module query-files-app-it) do the verification anyway.
