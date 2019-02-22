# Query Files App (Integration Tests)

This module provides a logic to execute Integration Tests (IT) of query-files-app. (i.e. the Query part from CQRS, for File-Store-in-S3 application.)
Using docker-compose it sets up:
- s3 local server (i.e. mock/stub) (@todo  https://stackoverflow.com/questions/6615988/how-to-mock-amazon-s3-in-an-integration-test)
- tested instance of query-files-app.

Afterwards it runs end-to-end scenarios defined in behave (BDD).

## Getting Started

```
# Create dev environment.
#
$ mkvirtualenv file-store-in-s3 --python=python3

# Install dependencies.
$ cd file-store-in-s3/query-files-app-it
(file-store-in-s3) $ pip install -r requirements.txt


(file-store-in-s3) $ cd file-store-in-s3/query-files-app-it
(file-store-in-s3) $ pip install behave
(file-store-in-s3) $ pip freeze > requirements.txt






@TODO

# Build images of modules: (and put them in the local docker)
#  query-files-app          - app to be tested
#  query-files-app-it       - integration tests
#
$ run_on_local_docker__install_all_images.sh 

$ docker image ls
REPOSITORY                         TAG                  IMAGE ID            CREATED             SIZE

# Start Up the required containers and run ITs.
#
$ run_on_local_docker__run_all_it.sh 
```

## Building Docker image

```
docker build . -t j9soft/query-files-app-it:latest

# alternatively start in docker
docker run -e "QFIT_QUERY_FILES_APP_URL=http://localhost:8090"  --name query-files-app--it --rm --network=query-files-app_backend_net -it j9soft/query-files-app-it:latest
```

## Running locally (not from Docker) during development

```
QFIT_QUERY_FILES_APP_URL="http://localhost:8090"

behave
```
