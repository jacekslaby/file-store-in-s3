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


```

## Developing

### Adding dependencies
(query-files-app) $ cd file-store-in-s3/query-files-app
(query-files-app) $ pip install flask
(query-files-app) $ pip freeze  | grep -v 'pkg-resources==0.0.0' > requirements.txt

### Unit tests

```
(query-files-app) $ cd file-store-in-s3/query-files-app
pytest

http://127.0.0.1:5000/v1/files?read_domain_regex=shell
```

### Running

http://flask.pocoo.org/docs/1.0/tutorial/factory/
```
(query-files-app) $ cd file-store-in-s3/query-files-app
export FLASK_APP=query-files-app
export FLASK_ENV=development
flask run
```

### Building Docker image

```
docker build . -t j9soft/query-files-app:latest
docker run -it -p 8000:8000 j9soft/query-files-app:latest
curl http://192.168.99.100:8000/

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
AWS_DEFAULT_REGION=dummy
AWS_ACCESS_KEY_ID=AccessKeyIfNeeded
AWS_SECRET_ACCESS_KEY=SecertKeyIfNeeded
flask run
```

## @TODO

- create the first skeleton of the app
