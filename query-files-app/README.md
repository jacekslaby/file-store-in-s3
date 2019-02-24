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
docker run -e "QF_QUERY_FILES_APP_S3_URL=http://192.168.99.100:4572"  --name query-files-appt --rm --network=query-files-app_backend_net -it j9soft/query-files-app:latest
```

### Running locally (not from Docker) during development

```
QF_QUERY_FILES_APP_S3_URL=http://192.168.99.100:4572


```

## @TODO

- create the first skeleton of the app
