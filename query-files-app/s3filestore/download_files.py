"""Module provides logic to retrieve properties used by a client to download a file from s3 object."""

import logging

_logger = logging.getLogger(__name__)


def get_file_download(s3_client, bucket_name, object_key):
    """retrieves a file-download object containing properties to be used by a client to launch a download operation.

           Returns a dict containing {'download_url': '<URL to be used>'}."""

    expiry_seconds = 300
    download_url = s3_client.generate_presigned_url('get_object',
                                                    {'Bucket': bucket_name, 'Key': object_key},
                                                    ExpiresIn=expiry_seconds,
                                                    HttpMethod='GET')

    result = {'download_url': download_url}

    _logger.info("get_file_download = '%s'", result)

    return result
