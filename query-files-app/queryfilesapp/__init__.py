import os

from flask import Flask, jsonify
from flask import request
from s3filestore import S3FileStore

app = Flask(__name__)
s3_file_store = S3FileStore()


@app.route('/')
def hello():
    return 'Hello, World!'


# Example: http://127.0.0.1:5000/v1/files?read_domain_regex=shell
@app.route('/v1/files')
def get_files():
    # Get regex for domains from URL parameter.
    # ( https://stackoverflow.com/questions/15182696/multiple-parameters-in-in-flask-approute )
    arg_read_domain_regex = request.args.get('read_domain_regex', None)

    # Retrieve files from matching domains.
    # ( http://flask.pocoo.org/docs/1.0/patterns/jquery/ )
    files = s3_file_store.get_files_from_domains(arg_read_domain_regex)

    return jsonify(files)


if __name__ == "__main__":
    app.run(debug=True)

