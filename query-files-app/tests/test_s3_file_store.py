from s3filestore import S3FileStore
import pytest

environment_name = 'it'


def setup_test_data():

    def generate_bucket_name(domain_name, domain_unique_suffix):
        return environment_name + S3FileStore.NAME_SEPARATOR + domain_name\
               + S3FileStore.NAME_SEPARATOR + str(domain_unique_suffix)

    test_domain_names = ['shell', 'statoil', 'ca', 'bp-upstream', 'bp-downstream']
    map_domain_bucket = {}
    for i, domain_name_str in enumerate(test_domain_names):
        map_domain_bucket[domain_name_str] = generate_bucket_name(domain_name_str, i)

    test_bucket_names = map_domain_bucket.values()
    print(map_domain_bucket)

    def generate_expected(*domain_name_args):
        result = {}
        for domain_name in domain_name_args:
            result[domain_name] = map_domain_bucket[domain_name]
        return result

    return [
        ([], 'dummy', {}),
        (test_bucket_names, 'shell', generate_expected('shell')),
        (test_bucket_names, 'shell.*', generate_expected('shell')),
        (test_bucket_names, 'bp.*', generate_expected('bp-upstream', 'bp-downstream')),
        (test_bucket_names, 'none', {})
    ]


test_data_for_get_domains_with_buckets = setup_test_data()


@pytest.fixture()
def s3_file_store():
    """create a new tested instance for each run of a test_* method"""
    return S3FileStore()


@pytest.mark.parametrize("all_buckets_names,read_domain_regex_str,expected", test_data_for_get_domains_with_buckets)
def test_get_domains_with_buckets(s3_file_store, all_buckets_names, read_domain_regex_str, expected):
    """verify that method works correctly for different input scenarios"""
    
    result = s3_file_store._get_domains_with_buckets(all_buckets_names, read_domain_regex_str)
    assert result == expected


@pytest.mark.parametrize("all_buckets_names,read_domain_regex_str,expected", test_data_for_get_domains_with_buckets)
def test_get_domains_with_buckets(s3_file_store, all_buckets_names, read_domain_regex_str, expected):
    """verify that method works correctly for different input scenarios"""

    result = s3_file_store._get_domains_with_buckets(all_buckets_names, read_domain_regex_str)
    assert result == expected
