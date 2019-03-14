"""Package contains a flask app which provides HTTP based read access to domains and files kept in s3."""

import logging
from flask import Flask, jsonify, request, abort

# Setup logging.
if __name__ == '__main__':
    # During development let's include messages from our logger(s) in the output.
    # (see also: http://flask.pocoo.org/docs/dev/logging/ )
    from flask.logging import default_handler
    root = logging.getLogger()
    root.addHandler(default_handler)
    root.setLevel(logging.INFO)
else:
    # On production let's align logging with settings given to Gunicorn.
    # (see also: https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f )
    gunicorn_logger = logging.getLogger('gunicorn.error')

    # Configure loggers from s3filestore lib to follow gunicorn level and handlers.
    for module_logger in (
            logging.getLogger('s3filestore.s3_file_store'),
            logging.getLogger('s3filestore.download_files'),
            logging.getLogger('s3filestore.query_files')
    ):
        module_logger.handlers = gunicorn_logger.handlers
        module_logger.setLevel(gunicorn_logger.level)


# Setup file store. (Note: It must be done after logging setup, otherwise messages are missing.)
from s3filestore import S3FileStore
s3_file_store = S3FileStore()


# Setup web app.
#
app = Flask(__name__)


def bad_request(message):
    """Builds and returns an HTTP 400 response containing the message."""

    # (see also:
    #  https://stackoverflow.com/questions/21294889/how-to-get-access-to-error-message-from-abort-command-when-using-custom-error-ha
    #
    response = jsonify({'message': message})
    response.status_code = 400
    return response


def extract_param_from_request(param_name, request_args):
    """Extracts value of a parameter by its name. Returns it as str. Throws ValueError if parameter not found."""

    # ( see:
    #   https://stackoverflow.com/questions/15182696/multiple-parameters-in-in-flask-approute
    #   http://flask.pocoo.org/docs/1.0/patterns/jquery/ )
    param_value = request_args.get(param_name)

    if param_value is None:
        raise ValueError(f"Missing required query parameter '{param_name}' in request URL.")

    return param_value


@app.route('/v1/domains')
def get_domains_with_files():
    """Retrieves domains matching a specified regex.

    Returns a JSON object containing key:value pairs  (i.e. a dict)
     where key is a domain name (string)
     and value is a list of files names (strings).

    Example: http://127.0.0.1:5000/v1/domains?read_domain_regex=shell
    """

    # Extract input parameters from URL.
    try:
        arg_read_domain_regex = extract_param_from_request('read_domain_regex', request.args)
    except ValueError as e:
        return bad_request(str(e))

    # Retrieve matching domains with files.
    files = s3_file_store.get_domains_with_files(arg_read_domain_regex)

    return jsonify(files)


@app.route('/v1/file-download')
def get_file_download():
    """Retrieves a file-download object with properties to be used by a client to launch a download operation.

    Returns a JSON object containing {'download_url': '<URL to be used>'}.

    http://127.0.0.1:5000/v1/file-download?read_domain_regex=shell&domain_name=Shell&file_name=Shell%3A0
    """

    # Extract input parameters from URL.
    try:
        arg_read_domain_regex = extract_param_from_request('read_domain_regex', request.args)
        domain_name = extract_param_from_request('domain_name', request.args)
        file_name = extract_param_from_request('file_name', request.args)
    except ValueError as e:
        return bad_request(str(e))

    # Retrieve file-download.
    file_download = s3_file_store.get_file_download(arg_read_domain_regex, domain_name, file_name)

    if file_download:
        return jsonify(file_download)
    else:
        # Return 404 Not Found
        return abort(404)


@app.route('/headers')
def get_headers():
    """Used to debug headers provided by Zappa when using Cognito authorizer.

    Returns a JSON object containing dictionary of headers.
    """

    return jsonify({k: v for k, v in request.headers})


if __name__ == "__main__":
    app.run(debug=True)
