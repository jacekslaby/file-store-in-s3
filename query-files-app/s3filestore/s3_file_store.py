import boto3
import re

# @TODO Read config settings from env variables.
environment_name = 'it'
s3_config = {'endpoint_url': 'http://192.168.99.100:4572',
             'use_ssl': False,
             'region_name': 'Dummy',
             'aws_access_key_id': 'AccessKey',
             'aws_secret_access_key': 'SecertKey'
             }


class S3FileStore:
    """Separator used in bucket name, e.g. <environment>--<domain>--<UUID> = testenv--shell--234666"""
    NAME_SEPARATOR = '--'

    def __init__(self):
        self.s3_resource = boto3.resource('s3', **s3_config)

    def get_files_from_domains(self, read_domain_regex_str):
        """retrieve files from matching domains.
           Returns a dict containing domain names as keys and lists of file names as values."""

        if read_domain_regex_str is None:
            # Return nothing for missing regex.
            return {}

        # Find all existing buckets.
        all_buckets_names = self._get_all_buckets_names()

        # Find all matching domains with their respective s3 buckets.
        domains_with_buckets = self._get_domains_with_buckets(all_buckets_names, read_domain_regex_str)

        # Load file names for every domain. File names are names of objects from a domain's bucket.
        return self._get_file_names_from_objects(domains_with_buckets)

    def _get_all_buckets_names(self):
        """retrieve names of all existing buckets"""

        # Every time we need to read available buckets. (because admin could add/remove some buckets in the meantime)
        return self.s3_resource.get_available_subresources()

    def _get_domains_with_buckets(self, all_buckets_names, read_domain_regex_str):
        """retrieve matching domains. Returns a dict containing domain names as keys and bucket names as values."""

        domain_pattern = re.compile(read_domain_regex_str)

        # Filter out buckets not belonging to this environment
        #  and not belonging to the domain regex string.
        # As a result we have a dict where key is domain name and value is bucket name.
        result = {}
        for bucket_name in all_buckets_names:
            if bucket_name.startswith(environment_name + S3FileStore.NAME_SEPARATOR):
                # Find name of the domain.
                domain_name_start_position = len(environment_name) + len(S3FileStore.NAME_SEPARATOR)
                domain_name_end_position = bucket_name.find(S3FileStore.NAME_SEPARATOR, domain_name_start_position)
                if domain_name_end_position < 0:
                    # @TODO add better logging
                    print(f'Unsupported bucket encountered: "{bucket_name}" - domain name is not between separators like "<environment>--<domain name>--...".')
                    continue

                domain_name = bucket_name[domain_name_start_position:domain_name_end_position]

                # Gather domains which names match the input regex.
                if domain_pattern.match(domain_name):
                    result[domain_name] = bucket_name

        return result

    def _get_file_names_from_objects(self, domains_with_buckets):
        """retrieve file names from object names from every bucket.
           Returns a dict containing domain names as keys and lists of file names as values."""

        # Load file names for every domain. File names are names of objects from a bucket.
        # As a result we have a dict where key is domain name
        #  and value is a list of names of files. (i.e. names of objects)
        result = {}
        for domain_name, bucket_name in domains_with_buckets.items():
            bucket = self.s3_resource.Bucket(bucket_name)
            domain_file_names = [object_name for object_name in bucket.get_available_subresources()]
            result[domain_name] = domain_file_names

        return result

