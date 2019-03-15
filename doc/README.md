
# Design

## Features:
- Querying for stored files - if a domain matches user's read-domain-regex then user may read every file from the domain. (i.e. from a bucket. Every domain as a single bucket.)  File names may contain '/' characters interpreted as folders when displayed in GUI.
- Downloading stored files - a URL with a short expiry date (<15 minutes) is returned to Web Browser  (i.e. pre-signed s3 URL)
- Commands for stored files - if a domain matches user's write-domain-regex then user may create/delete every file from the domain.
- Uploading stored files - a URL with a short expiry date (<15 minutes) is returned to Web Browser  (i.e. pre-signed s3 URL)

## Components:
- Amazon s3 (storage layer)
- Amazon Cognito User Pools (user authentication)
- Amazon API Gateway (user authorization)
- query-files-app - docker container (or serverless API Gateway + Lambda) - GET /v1/files?read_domain_regex=shell         (It neither verifies authentication nor authorisation. It does not know about users.)
- query-files-app-it - Gherkin scenarios - system & integration tests
- command-files-app - docker container
- files-store-app - react, list available domains, list files in a domain, click to download a file, click to upload a file. 

## Dev components:
- localstack - running in Docker container - used as s3 provider
- query-files-app - running in Docker container - connects to s3 endpoint provided in environment variable
- query-files-app-it - run from command line, 'behave' - connects to s3 endpoint provided in environment variable, connects to query-files-app endpoint provided in environment variable

## Architecture:
- end users in Cognito, with token containing claims: readdomainregex, writedomainregex. With email address. With email reset password option.
- static web: JavaScript, react. Talks to Cognito. Talks to query-files-app via HTTP. API Gateway extracts claim:readdomainregex from user token and provides it as an HTTP header 'read-domain-regex' to query-files-app.
- query-files-app trusts in correctness (and security) of information provided in read-domain-regex.
- query-files-app reads all buckets from aws account. Then returns all objects (as files) existing in buckets which name match read-domain-regex.
- query-files-app is released as a Docker container.  (tagged e.g. j9soft/query-files-app:0.1.0_d6c2de7c - <major.minor.patch><git commit ID>)
- query-files-app-it contains Integration Tests for Query (CQRS). Gherkin language is used to describe features and scenarios.  When tests are started first they setup some test buckets and files in s3, using s3 endpoint URL provided as environment variable.
- localstack/localstack Docker container is used during development as local s3 endpoint. (Without persistance, i.e. all test data are wiped out on container restart)

## TODO Still to describe:
- There is NO option to rename a file.
- Support for multiple Environments in one AWS region. (Every bucket name is like: <environmentName>--<domain name>--<UUID to make bucket unique>.)  (just UUID would be better, but not admin-friendly)
- Support for CORS - query-files-app returns proper CORS HTTP Header to allow GUI to connect to s3 endpoint
- query-files-app assumes an IAM role allowing it to read s3 buckets matching: <environmentName>--.*



