"""Package contains a flask app which provides HTTP based read access to domains and files kept in s3."""

import logging
from flask import Flask, jsonify, request

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
            logging.getLogger('s3filestore.query_files')
    ):
        module_logger.handlers = gunicorn_logger.handlers
        module_logger.setLevel(gunicorn_logger.level)


# Setup file store. (Note: It must be after logging setup, otherwise messages are missing.)
from s3filestore import S3FileStore
s3_file_store = S3FileStore()


# Setup web app.
#
app = Flask(__name__)


def bad_request(message):
    # (see also:
    #  https://stackoverflow.com/questions/21294889/how-to-get-access-to-error-message-from-abort-command-when-using-custom-error-ha
    #
    response = jsonify({'message': message})
    response.status_code = 400
    return response


@app.route('/v1/domains')
def get_domains_with_files():
    """Retrieves domains matching a specified regex.

    Returns a JSON object containing key:value pairs  (i.e. a dict)
     where key is a domain name (string)
     and value is a list of files names (strings).

     Example: http://127.0.0.1:5000/v1/domains?read_domain_regex=shell
    """

    # Extract regex for domains from URL parameter.
    # ( https://stackoverflow.com/questions/15182696/multiple-parameters-in-in-flask-approute
    #   http://flask.pocoo.org/docs/1.0/patterns/jquery/ )
    param_name = 'read_domain_regex'
    arg_read_domain_regex = request.args.get(param_name)
    if arg_read_domain_regex is None:
        return bad_request(f"Missing required query parameter '{param_name}' in request URL.")

    # Retrieve matching domains with files.
    files = s3_file_store.get_domains_with_files(arg_read_domain_regex)

    return jsonify(files)


if __name__ == "__main__":
    app.run(debug=True)

