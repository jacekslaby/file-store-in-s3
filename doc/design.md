
# Design

## Features:
- Querying for stored files - if a domain matches user's read-domain-regexp then user may read every file from the domain. (i.e. from a bucket. Every domain as a single bucket.)  Files names may contain '/' characters interpreted as folders in GUI.
- Downloading stored files - a URL with a short expiry date (<15 minutes) is returned to Web Browser  (i.e. pre-signed s3 URL)
- Commands for stored files - if a domain matches user's write-domain-regexp then user may create/delete every file from the domain.
- Uploading stored files - a URL with a short expiry date (<15 minutes) is returned to Web Browser  (i.e. pre-signed s3 URL)

## Components:
- s3
- Cognito
- API Gateway
- query-files-app - docker container - GET /v1/files?readDomainRegexp=shell         (It neither verifies authentication nor authorisation. It does not know about users.)
- query-files-app-it - Gherkin scenarios - integration tests
- command-files-app - docker container
- files-store-app - react, list available domains, list files in a domain, click to download a file, click to upload a file. 

## Dev components:
- localstack - running in Docker container - used as s3 provider
- query-files-app - running in Docker container - connects to s3 endpoint provided in environment variable
- query-files-app-it - run from command line, 'behave' - connects to s3 endpoint provided in environment variable, connects to query-files-app endpoint provided in environment variable

## Architecture:
- end users in Cognito, with token containing claims: read-domain-regexp, write-domain-regexp. With email address. With email reset password option.
- static web: JavaScript, react. Talks to Cognito. Talks to query-files-app via HTTP. API Gateway extracts claim:read-domain-regexp from user token and provides it as a parameter in URL to query-files-app.
- query-files-app trusts in correctness (and security) of information provided in read-domain-regexp.
- query-files-app reads all buckets from aws account. Then returns all objects (as files) existing in buckets which name match read-domain-regexp.
- query-files-app is released as a Docker container.  (tagged e.g. j9soft/query-files-app:0.1.0_b7322563 - b<git commit ID>)
- query-files-app-it contains Integration Tests for Query (CQRS). Gherkin language is used to describe features and scenarios.  When tests are started first they setup some test buckets and files in s3, using s3 endpoint URL provided as environment variable.
- localstack/localstack Docker container is used during development as local s3 endpoint. (Without persistance, i.e. all test data are wiped out on container restart)

## TODO Still to describe:
- No option to rename a file.
- Support for multiple Environments in one AWS region. (Every bucket name is like: <environmentName>--<domain name>--<UUID to make bucket unique>.)  (just UUID would be better, but not admin-friendly)
- Support for CORS - query-files-app returns proper CORS HTTP Header to allow GUI to connect to s3 endpoint
- query-files-app assumes an IAM role allowing it to read s3 buckets matching: <environmentName>--.*



