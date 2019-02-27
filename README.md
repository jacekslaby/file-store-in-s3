
* [Overview](#overview)
* [Running The Modules](#running-the-modules)
* [Prerequisities](#prerequisites)


# Overview

File-Store-in-s3 application provides functionality of storing and sharing files between several users in the cloud. Files are grouped in domains. Users can access the files depending on privileges they have to a domain (none, read, read+write). Users use Web Browser to access the application and the files. Users must authenticate themselves with user name and password. Using AWS console an Administrator manages domains (buckets in s3), users and their privileges (user accounts and claims in Cognito user pool).

There are multiple modules in this repo that are parts of File-Store-in-s3 application.
Each module resides in its own subfolder.

| Modules                                       | Description 
| ------------------------------------------ | -------------------------------------------------------------------------------- 
| [doc](doc/README.md)     | Design documentation for File-Store-in-s3 application.
| [query-files-app](query-files-app/README.md)     | Query-Files-App is a web application (HTTP) developed in `python`+`flask`+`Gunicorn`+`Docker`.
| [query-files-app-it](k-repository-it/README.md)     | Integration Tests (IT) of Query-Files-App. Using docker-compose it sets up a localstack, several s3 buckets and objects, an instance of Query-Files-App and then runs end-to-end scenarios defined in `python`+`behave`.


# Running The Modules

1. Clone the repo: `git clone https://github.com/jacekslaby/file-store-in-s3`
2. Change directory to one of the module subfolders
3. Read the `README.md` for each module for precise instructions

# Prerequisites

* Docker version 18.02.0+
* Docker Compose version 1.14.0 with Docker Compose file format 3.2

# @TODO

* module file-store-gui
* modules: command-files-app + command-files-app-it
