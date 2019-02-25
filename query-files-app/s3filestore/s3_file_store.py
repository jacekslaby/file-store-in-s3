import boto3


class  S3FileStore:
    def get_files_from_domains(self, read_domain_regexp):
        return {read_domain_regexp: ['f1', 'f2']}
