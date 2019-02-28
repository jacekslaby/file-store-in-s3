import re
import logging

_logger = logging.getLogger(__name__)

# Separator used in bucket name, e.g. <environment>--<domain>--<UUID> = testenv--shell--234666
_NAME_SEPARATOR = '--'


def get_files_from_domains(s3_resource, environment_name, read_domain_regex_str):
    """From s3 retrieve files from domains matching the read_domain_regex_str existing in the specified environment.

       Returns a dict containing domain names as keys.
       Each domain has a corresponding value being a list of file names from that domain."""

    if read_domain_regex_str is None:
        # Return nothing for missing regex.
        return {}

    # Find all existing buckets.
    all_buckets_names = _get_all_buckets_names(s3_resource)

    # Find all matching domains with their respective s3 buckets.
    domains_with_buckets = _get_domains_with_buckets(environment_name, all_buckets_names, read_domain_regex_str)

    # Load file names for every domain. File names are names of objects from a domain's bucket.
    return _get_file_names_from_objects(s3_resource, domains_with_buckets)


def _get_all_buckets_names(s3_resource):
    """retrieve names of all existing buckets"""

    # Every time we need to read available buckets. (because admin could add/remove some buckets in the meantime)
    result = [bucket.name for bucket in s3_resource.buckets.all()]
    _logger.info("S3FileStore: _get_all_buckets_names = '%s'", result)

    return result


def _get_domains_with_buckets(environment_name, all_buckets_names, read_domain_regex_str):
    """retrieve matching domains. Returns a dict containing domain names as keys and bucket names as values."""

    if read_domain_regex_str is None:
        # Return nothing for missing regex.
        return {}

    # Let's ignore case, it is more user friendly.
    domain_pattern = re.compile(read_domain_regex_str, flags=re.IGNORECASE)

    # Filter out buckets not belonging to this environment
    #  and not belonging to the domain regex string.
    # As a result we have a dict where key is domain name and value is bucket name.
    result = {}
    for bucket_name in all_buckets_names:
        if bucket_name.startswith(environment_name + _NAME_SEPARATOR):
            # Find name of the domain.
            domain_name_start_position = len(environment_name) + len(_NAME_SEPARATOR)
            domain_name_end_position = bucket_name.find(_NAME_SEPARATOR, domain_name_start_position)
            if domain_name_end_position < 0:
                _logger.warning(f'Unsupported bucket encountered: "{bucket_name}'
                               f'" - expected format is like "<environment>--<domain name>--<uuid>".')
                continue

            domain_name = bucket_name[domain_name_start_position:domain_name_end_position]

            # Gather domains which names match the input regex.
            if domain_pattern.match(domain_name):
                result[domain_name] = bucket_name

    _logger.info("S3FileStore: _get_domains_with_buckets = '%s'", result)
    return result


def _get_file_names_from_objects(s3_resource, domains_with_buckets):
    """retrieve file names from object names from every bucket.
       Returns a dict containing domain names as keys and lists of file names as values."""

    # Load file names for every domain. File names are names of objects from a bucket.
    # As a result we have a dict where key is domain name
    #  and value is a list of names of files. (i.e. names of objects)
    result = {}
    for domain_name, bucket_name in domains_with_buckets.items():
        bucket = s3_resource.Bucket(bucket_name)
        domain_file_names = [obj.key for obj in bucket.objects.all()]
        result[domain_name] = domain_file_names

    _logger.info("S3FileStore: _get_file_names_from_objects = '%s'", result)
    return result
