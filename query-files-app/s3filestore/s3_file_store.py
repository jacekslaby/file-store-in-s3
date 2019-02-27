import boto3
import os
import logging
from s3filestore.query_files import get_files_from_domains

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

        return get_files_from_domains(self.s3_resource, environment_name, read_domain_regex_str)
