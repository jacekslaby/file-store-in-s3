# Query Files App (Integration Tests)

This module provides a logic to execute Integration Tests (IT) of query-files-app.

Using docker-compose it sets up services:
- localhost - an s3 local server (i.e. a mock/stub) 
    - (see also: https://stackoverflow.com/questions/6615988/how-to-mock-amazon-s3-in-an-integration-test)
- query-files-app - a tested instance of query-files-app.

Afterwards it is possible to run end-to-end scenarios defined in Gherkin (BDD+`behave`).

## Getting Started

```
# Create dev environment.
#
$ cd file-store-in-s3/query-files-app-it
$ mkvirtualenv venv --python=python3

# Install dependencies.
$ cd file-store-in-s3/query-files-app-it
(file-store-in-s3) $ pip install -r requirements.txt

@TODO
# Build images of modules: (and put them in the local docker)
#  query-files-app          - app to be tested
#  query-files-app-it       - integration tests
#
$ run_on_local_docker__install_all_images.sh 

$ docker image ls
REPOSITORY                         TAG                  IMAGE ID            CREATED             SIZE

@TODO
# Start Up the required containers and run ITs.
#
$ run_on_local_docker__run_all_it.sh 
```

## Developing

### Using [localstack](https://github.com/localstack/localstack)

Only s3 service is used. Without persistence.

To browse contents use: http://192.168.99.100:8080

(localstack was selected based on the following comments: 
- "If you're ok with depending on a running docker container [...] consider using localstack" https://stackoverflow.com/questions/6615988/how-to-mock-amazon-s3-in-an-integration-test
- "SAM Local is basically just for testing your Lambda functions locally." https://stackoverflow.com/questions/45719388/aws-sam-local-vs-localstack
)

### Configure PyCharm

Add Run configuration as described here: https://stackoverflow.com/questions/15860074/pycharm-how-to-run-behave-exe
```
Script: put dot (.) in here [this way PyCharm recognizes the configuration as valid and doesn't show red cross mark]
Working Directory points to the dirctory where .feature file is
Interpreter options: -m behave
```

### Building Docker image

```
docker build . -t j9soft/query-files-app-it:latest

# alternatively start in docker
docker run --name query-files-app--it --rm --network=qfa_backend_net -it j9soft/query-files-app-it:latest
```

### Running locally (not from Docker) during development

```
# Connect to s3 provided by localstack (running in docker-compose on a docker-machine) 
QFAIT_AWS_S3_ENDPOINT_URL=http://192.168.99.100:4572

# Connect to query-files-app (running locally via 'flask run')
QFAIT_QUERY_FILES_APP_URL=http://127.0.0.1:5000
# OR, alternatively, connect to query-files-app running in docker-compose on a docker-machine)
QFAIT_QUERY_FILES_APP_URL=http://192.168.99.100:8000

# Start the integration tests
behave
```

## @TODO

- add mistakes-in-url.feature - to verify that correct HTTP error codes are returned
- Use pytest-bdd instead of behave, because assert messages are better
  https://automationpanda.com/2018/10/22/python-testing-101-pytest-bdd/
  "all of pytest‘s features and plugins can be used with pytest-bdd. This is a huge advantage!"
