import boto3
import os

# Name of environment - For integration tests we always just use the same name.
environment_name = 'it'

# Read global config settings from env variables.  (e.g. to have different settings for development and production)
#
# - Name of AWS region where s3 buckets should be created
if 'QFAIT_AWS_S3_REGION_NAME' not in os.environ:
    # For dev we always just use the same name. (so no need to setup env vars which is troublesome)
    s3_region_name = 'Dummy'
else:
    # For production we configure based on the provided value.
    # @TODO Is this scenario even used at all ?  Maybe if we want to test against real s3, but... hm...
    s3_region_name = os.environ['QFAIT_AWS_S3_REGION_NAME']
#
# - Location of s3 endpoint
#   (i.e. an optional environment variable may redefine location of s3 endpoint, e.g. when we use localstack for dev)
#   (see also:
#    - https://github.com/aws/aws-cli/issues/1270
#    - https://clouductivity.com/amazon-web-services/aws-credentials-access-keys-secret-keys/
#   )
if 'QFAIT_AWS_S3_ENDPOINT_URL' in os.environ:
    # For dev we redefine config used by boto3.
    s3_config = {'endpoint_url': os.environ['QFAIT_AWS_S3_ENDPOINT_URL'],
                 'use_ssl': False,            # For now we assume it makes sense. (no need to add another env var)
                 'region_name': 'Dummy',
                 'aws_access_key_id': 'AccessKey',
                 'aws_secret_access_key': 'SecretKey'
                 }
else:
    # For production we use defaults. (i.e. boto3 will use defaults)
    # @TODO Is this scenario even used at all ?  Maybe if we want to test against real s3, but... hm...
    s3_config = None
#
# - Location of query-files-app endpoint
if 'QFAIT_QUERY_FILES_APP_URL' not in os.environ:
    # For dev we always just use the localhost. (so no need to setup env vars which is troublesome)
    query_files_app_url = 'http://127.0.0.1:5000'
else:
    # For dev against a docker-compose we configure based on the provided value.
    query_files_app_url = os.environ['QFAIT_QUERY_FILES_APP_URL']

# Define test data to be created in s3.
#
# Let's provide domains names. Each with number of files.
domains = {'Shell': 2, 'BP-upstream': 4, 'BP-midstream': 0, 'BP-downstream': 10, 'AL': 3, 'CA': 2}
#
# Let's prepare file names for every domain, e.g. 'Shell:0', 'Shell:1', etc.
files_existing_in_domains = {domain_name: [domain_name + ':' + str(i) for i in range(file_count)]
                             for domain_name, file_count in domains.items()}
#
# Let's prepare bucket names, e.g. bucket 'it::Shell' with files ['Shell:0', 'Shell:1']
files_existing_in_s3_buckets = {environment_name + '--' + domain_name + '--unique-uuid': files_list
                                for domain_name, files_list in files_existing_in_domains.items()}


def before_all(context):
    # Prepare s3 client.
    # (based on:
    #   https://realpython.com/python-boto3-aws-s3/
    #   https://stackoverflow.com/questions/45981950/how-to-specify-credentials-when-connecting-to-boto3-s3
    #   https://stackoverflow.com/questions/32618216/overwrite-s3-endpoint-using-boto3-configuration-file
    #   https://stackoverflow.com/questions/48690698/using-boto3-through-sam-local-to-interact-with-localstack-s3
    #   )
    if s3_config is None:
        # It means we are happy for boto3 to figure out AWS settings. (e.g. from credentials file, IAM role, etc.)
        s3_resource = boto3.resource('s3')
    else:
        # We are on local dev environment and we want to tell boto3 where to connect.
        s3_resource = boto3.resource('s3', **s3_config)

    # Specify the region.
    # (otherwise: "If you don't specify a region, the bucket will be created in US Standard." )
    bucket_configuration = {'LocationConstraint': s3_region_name}

    # Create all required buckets and objects in s3, (it takes time so we do it before all features/scenarios are run)
    # based on dictionary in which:
    #  - key is bucket name
    #  - value is list of object names in this bucket
    #
    for bucket_name, files_list in files_existing_in_s3_buckets.items():
        # Let's assure existence of buckets and objects.
        # (BTW: If a bucket exists then we assume that its objects exist as well. (i.e. It's another run of these tests)
        #       The reason for this is that checking for object existence is expensive and not really required here.)
        #
        # (https://stackoverflow.com/questions/26871884/how-can-i-easily-determine-if-a-boto-3-s3-bucket-resource-exists)
        bucket = s3_resource.Bucket(bucket_name.lower())
        if not bucket.creation_date:
            # Bucket does not exist. We need to create it.
            bucket = s3_resource.create_bucket(Bucket=bucket_name.lower(), CreateBucketConfiguration=bucket_configuration)
            # Then create all required objects. (in this bucket)
            for object_name in files_list:
                object = bucket.Object(object_name)
                object.put(Body='something')     # btw: without put 'Body' object was not created
                # @TODO better logging
                print(f"Object '{object.key}' created in bucket '{object.bucket_name}'")

        existing_objects = [obj.key for obj in bucket.objects.all()]
        # @TODO better logging
        print(f"Bucket '{bucket_name}' contains objects: {existing_objects}")
        assert set(files_list) == set(existing_objects),\
            f"Test setup FAILED to create objects in s3.  Wanted: '{files_list}', existing: '{existing_objects}'."

    # provide files in the scenario's context   (e.g. to check correctness of returned results)
    context.files_existing_in_domains = files_existing_in_domains

    # @TODO better logging
    print(f"Domains with files: {files_existing_in_domains}")

    # provide a location of the app to be tested
    context.query_files_app_url = query_files_app_url

