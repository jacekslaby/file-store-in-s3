import boto3
import re
import os
import logging

logger = logging.getLogger(__name__)

# Read global config settings from env variables.  (e.g. to have different settings for development and production)
#
# - Name of environment   (i.e. a name of an installation of file-store-in-s3 application)
if 'QFA_ENVIRONMENT_NAME' not in os.environ:
    # For dev we always just use the same name. (so no need to setup env vars which is troublesome)
    environment_name = 'it'
else:
    # For production we configure based on the provided value.
    environment_name = os.environ['QFA_ENVIRONMENT_NAME']
#
# - Location of s3 endpoint
#   (i.e. an optional environment variable may redefine location of s3 endpoint, e.g. when we use localstack for dev)
#   (see also:
#    - https://github.com/aws/aws-cli/issues/1270
#    - https://clouductivity.com/amazon-web-services/aws-credentials-access-keys-secret-keys/
#   )
if 'QFA_AWS_S3_ENDPOINT_URL' in os.environ:
    # For dev we redefine config used by boto3.
    s3_config = {'endpoint_url': os.environ['QFA_AWS_S3_ENDPOINT_URL'],
                 'use_ssl': False,            # For now we assume it makes sense. (no need to add another env var)
                 'region_name': 'Dummy',
                 'aws_access_key_id': 'AccessKey',
                 'aws_secret_access_key': 'SecretKey'
                 }
else:
    # For production we use defaults. (i.e. boto3 will use defaults)
    s3_config = None

# Let's log global config settings.
logger.info("S3FileStore global config: environment_name = '%s'", environment_name)
logger.info("S3FileStore global config: s3_config = '%s'", s3_config)


class S3FileStore:
    """S3FileStore() --> an object providing mapping between s3 objects and file-store's files

    Instances of this class can be used like this:
    s3FileStore = s3filestore.S3FileStore()
    files = s3FileStore.get_files_from_domains('shell|bp.*')
    """

    # Separator used in bucket name, e.g. <environment>--<domain>--<UUID> = testenv--shell--234666
    NAME_SEPARATOR = '--'

    def __init__(self):
        if s3_config is None:
            # It means we are happy for boto3 to figure out AWS settings. (e.g. from credentials file, IAM role, etc.)
            self.s3_resource = boto3.resource('s3')
        else:
            # We are on local dev environment and we want to tell boto3 where to connect.
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
        result = [bucket.name for bucket in self.s3_resource.buckets.all()]
        logger.info("S3FileStore: _get_all_buckets_names = '%s'", result)

        return result

    def _get_domains_with_buckets(self, all_buckets_names, read_domain_regex_str):
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
            if bucket_name.startswith(environment_name + S3FileStore.NAME_SEPARATOR):
                # Find name of the domain.
                domain_name_start_position = len(environment_name) + len(S3FileStore.NAME_SEPARATOR)
                domain_name_end_position = bucket_name.find(S3FileStore.NAME_SEPARATOR, domain_name_start_position)
                if domain_name_end_position < 0:
                    logger.warning(f'Unsupported bucket encountered: "{bucket_name}'
                                   f'" - expected format is like "<environment>--<domain name>--<uuid>".')
                    continue

                domain_name = bucket_name[domain_name_start_position:domain_name_end_position]

                # Gather domains which names match the input regex.
                if domain_pattern.match(domain_name):
                    result[domain_name] = bucket_name

        logger.info("S3FileStore: _get_domains_with_buckets = '%s'", result)
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
            domain_file_names = [obj.key for obj in bucket.objects.all()]
            result[domain_name] = domain_file_names

        logger.info("S3FileStore: _get_file_names_from_objects = '%s'", result)
        return result
