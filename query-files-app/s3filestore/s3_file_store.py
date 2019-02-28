"""Module provides logic to access domains and files kept in s3."""

import boto3
import os
import logging
from s3filestore.query_files import get_domains_with_files
from s3filestore.query_files import get_bucket_for_domain
from s3filestore.download_files import get_file_download

_logger = logging.getLogger(__name__)

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
_logger.info("S3FileStore global config: environment_name = '%s'", environment_name)
_logger.info("S3FileStore global config: s3_config = '%s'", s3_config)


class S3FileStore:
    """S3FileStore() --> an object providing mapping between s3 objects and file-store's files

    Instances of this class can be used like this:
    s3FileStore = s3filestore.S3FileStore()
    files = s3FileStore.get_domains_with_files('shell|bp.*')
    """

    def __init__(self):
        if s3_config is None:
            # It means we are happy for boto3 to figure out AWS settings. (e.g. from credentials file, IAM role, etc.)
            self.s3_resource = boto3.resource('s3')
            self.s3_client = boto3.client('s3')
        else:
            # We are on local dev environment and we want to tell boto3 where to connect.
            self.s3_resource = boto3.resource('s3', **s3_config)
            self.s3_client = boto3.client('s3', **s3_config)

    def get_domains_with_files(self, read_domain_regex_str):
        """retrieves domains (with files) matching regex.
           Returns a dict containing domain names as keys and lists of file names as values."""

        return get_domains_with_files(self.s3_resource, environment_name, read_domain_regex_str)

    def get_file_download(self, read_domain_regex_str, domain_name, file_name):
        """retrieves a file-download object containing properties to be used by a client to launch a download operation.

           Returns a dict containing {'download_url': '<URL to be used>'}.
           Returns None if domain or file do not exist.
           Returns None if user does not have privileges to the file."""

        target_s3bucket = get_bucket_for_domain(self.s3_resource, environment_name, read_domain_regex_str, domain_name)

        if target_s3bucket:
            _logger.info("S3FileStore get_file_download: file_name = '%s', target_s3bucket.object_names = '%s'",
                         file_name, target_s3bucket.object_names)
            if file_name in target_s3bucket.object_names:
                return get_file_download(self.s3_client, target_s3bucket.name, file_name)

        return None
