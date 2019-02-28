# Query Files App

This module provides a logic of query-files-app. (i.e. the Query part from CQRS, for File-Store-in-S3 application.)

## Getting Started

```
# Create dev environment.
#
$ mkvirtualenv query-files-app  --python=python3

# Install dependencies.
(query-files-app) $ cd file-store-in-s3/query-files-app
pip install -r requirements.txt

# Run from the command line.
# (see also http://flask.pocoo.org/docs/1.0/tutorial/factory/)
#
# (Note: It connects to AWS S3, so your credentials need to available in a standard way,
#   e.g. env variables or a .credentials file.)
#
(query-files-app) $ cd file-store-in-s3/query-files-app
export FLASK_APP=query-files-app
export FLASK_ENV=development
flask run

# Open Web Browser with:
http://127.0.0.1:5000/v1/domains?read_domain_regex=shell
http://127.0.0.1:5000/v1/file-download?read_domain_regex=shell&domain_name=Shell&file_name=Shell%3A0
```


## Developing

### Adding dependencies
```
(query-files-app) $ cd file-store-in-s3/query-files-app
(query-files-app) $ pip install flask
(query-files-app) $ pip freeze  | grep -v 'pkg-resources==0.0.0' > requirements.txt
```
### Running unit tests

```
(query-files-app) $ cd file-store-in-s3/query-files-app
pytest
```

### Running App in PyCharm

1. Using python (better, because log messages are better formatted)
    * Add 'Run' configuration 
    * with 'Script path' pointing to `...\query-files-app\queryfilesapp\__init__.py`
    * and with env variables:
        * FLASK_APP=queryfilesapp
        * QFA_AWS_S3_ENDPOINT_URL=http://192.168.99.100:4572
        * (Note: Instead of connecting to s3 it will connect to a `localstack` instance available at this URL.)
 
2. Using flask
    * Add 'Run' configuration 
    * with 'Script path' pointing to `...\file-store-in-s3\query-files-app\venv\Scripts\flask.exe` (in your virtualenv)
    * and with the same env variables as in 1.

### Building Docker image

```
docker build . -t j9soft/query-files-app:0.1.0
docker run -it -p 8000:8000 j9soft/query-files-app:0.1.0
curl http://192.168.99.100:8000/v1/domains?read_domain_regex=shell

# alternatively start in docker
docker run -it -p 8000:8000 -e "QFA_AWS_S3_ENDPOINT_URL=http://localstack:4572"  --name query-files-app --rm --network=queryfilesappit_qfa_backend_net  j9soft/query-files-app:0.1.0
docker run -it -p 8000:8000 -e "QFA_AWS_S3_ENDPOINT_URL=http://192.168.99.100:4572"  --name query-files-app --rm   j9soft/query-files-app:0.1.0
docker run -it -p 8000:8000 -e "QFA_AWS_S3_ENDPOINT_URL=http://192.168.99.100:4572" j9soft/query-files-app:0.1.0
```

### Running locally (not from Docker) during development

```
# E.g. in order to connect to a localstack instance running on docker-machine:
QFA_ENVIRONMENT_NAME=it
QFA_AWS_S3_ENDPOINT_URL=http://192.168.99.100:4572
flask run
```

## @TODO

