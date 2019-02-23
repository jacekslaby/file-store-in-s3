import boto3

# @TODO Read config settings from env variables.
environment_name = 'it'
s3_region_name = 'Dummy'
s3_endpoint_url = 'http://192.168.99.100:4572'

# Define test data to be created in s3.
#
# Let's provide domains names. Each with number of files.
domains = {'Shell': 2, 'BP-upstream': 4, 'BP-midstream': 0, 'BP-downstream': 10, 'AL': 3, 'CA': 2}
#
# Let's create file names for every domain, e.g. 'Shell:0', 'Shell:1', etc.
files_existing_in_domains = {domain_name: [domain_name + ':' + str(i) for i in range(file_count)]
                             for domain_name, file_count in domains.items()}
#
# Let's create bucket names, e.g. bucket 'it::Shell' with files ['Shell:0', 'Shell:1']
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
    s3_resource = boto3.resource('s3', endpoint_url=s3_endpoint_url,
                                 use_ssl=False,
                                 region_name='Dummy',
                                 aws_access_key_id='AccessKey',
                                 aws_secret_access_key='SecertKey')
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
                bucket.Object(object_name)

    # provide files in the scenario's context   (e.g. to check correctness of returned results)
    context.files_existing_in_domains = files_existing_in_domains

    print(files_existing_in_domains)
