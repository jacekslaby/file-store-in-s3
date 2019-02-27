import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

# Setup our logging.
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

    # Configure logger from s3filestore lib to follow gunicorn level and handlers.
    s3_file_store_logger = logging.getLogger('s3filestore.s3_file_store')
    s3_file_store_logger.handlers = gunicorn_logger.handlers
    s3_file_store_logger.setLevel(gunicorn_logger.level)

    # @TODO Is it required ?  (as app.logger is not used then perhaps we can remove these 2 lines ?)
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


# Setup our file store. (Note: It must be after logging setup, otherwise messages are missing.)
from s3filestore import S3FileStore
s3_file_store = S3FileStore()


# Let's setup our web app logic.
#

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

