
environment_name = 'it'

# Let's provide domains names. Each with number of files.
domains = {'Shell': 2, 'BP-upstream': 4, 'BP-midstream': 0, 'BP-downstream': 10, 'AL': 3, 'CA': 2}

# Let's create file names for every domain, e.g. 'Shell:0', 'Shell:1', etc.
files_existing_in_domains = {domain_name: [domain_name + ':' + str(i) for i in range(file_count)]
                             for domain_name, file_count in domains.items()}

# Let's provide buckets' names. Each with number of files.
# <environmentName>::<grupa alos>::projSecret:_2345_345_333.
# buckets_existing_in_s3 = {environment_name + '::' + domain_name + ':: @TODO unique UUID': file_count
#                          for domain_name, file_count in domains.items()}

# Let's create bucket names, e.g. bucket 'it::Shell' with files ['Shell:0', 'Shell:1']
files_existing_in_s3_buckets = {environment_name + '::' + domain_name + ':: @TODO unique UUID': files_list
                                for domain_name, files_list in files_existing_in_domains.items()}


def before_all(context):
    # @TODO Create all required files. (in s3 bucket)
    # (it takes time so we want to do it once before all features/scenarios are run)
    #  - key is domain name
    #  - value is list of files existing in this domain

    # provide files in the scenario's context   (e.g. to check correctness of returned results)
    context.files_existing_in_domains = files_existing_in_domains

    print(files_existing_in_domains)
