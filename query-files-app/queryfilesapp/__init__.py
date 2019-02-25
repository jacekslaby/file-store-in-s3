from flask import Flask, jsonify, request
from s3filestore import S3FileStore

app = Flask(__name__)
s3_file_store = S3FileStore()


def bad_request(message):
    # (see also:
    #  https://stackoverflow.com/questions/21294889/how-to-get-access-to-error-message-from-abort-command-when-using-custom-error-ha
    #
    response = jsonify({'message': message})
    response.status_code = 400
    return response


@app.route('/')
def hello():
    return 'Hello, World!'


# Example: http://127.0.0.1:5000/v1/files?read_domain_regex=shell
@app.route('/v1/files')
def get_files():
    # Get regex for domains from URL parameter.
    # ( https://stackoverflow.com/questions/15182696/multiple-parameters-in-in-flask-approute )
    param_name = 'read_domain_regex'
    arg_read_domain_regex = request.args.get(param_name)
    if arg_read_domain_regex is None:
        return bad_request(f"Missing required query parameter '{param_name}' in request URL.")

    # Retrieve files from matching domains.
    # ( http://flask.pocoo.org/docs/1.0/patterns/jquery/ )
    files = s3_file_store.get_files_from_domains(arg_read_domain_regex)

    return jsonify(files)


if __name__ == "__main__":
    app.run(debug=True)

