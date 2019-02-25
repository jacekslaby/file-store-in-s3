import os

from flask import Flask
from flask import request
from s3filestore import S3FileStore

app = Flask(__name__)
s3FileStore = S3FileStore()


@app.route('/')
def hello():
    return 'Hello, World!'


# Example: http://127.0.0.1:5000/v1/files?read_domain_regexp=shell
@app.route('/v1/files')
def get_files():
    # https://stackoverflow.com/questions/15182696/multiple-parameters-in-in-flask-approute
    read_domain_regexp = request.args.get('read_domain_regexp', None)
    return s3FileStore.get_files_from_domains(read_domain_regexp)


if __name__ == "__main__":
    app.run(debug=True)

