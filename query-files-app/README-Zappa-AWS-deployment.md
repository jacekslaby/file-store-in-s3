# Deployment on AWS

Description of how to deploy this project on AWS (API Gateway + Lambda) using [Zappa](https://github.com/Miserlou/Zappa).

## Why Zappa ?

Quote from [documentation](https://github.com/Miserlou/Zappa):
> Zappa will automatically
> - package up your application and local virtual environment into a Lambda-compatible archive,
> - replace any dependencies with versions precompiled for Lambda, 
> - set up the function handler and necessary WSGI Middleware, 
> - upload the archive to S3, 
> - create and manage the necessary Amazon IAM policies and roles, 
> - register it as a new Lambda function, 
> - create a new API Gateway resource, create WSGI-compatible routes for it, link it to the new Lambda function, 
> - and finally delete the archive from your S3 bucket. 


## Deploying to AWS

```
# Create python dev environment.  (on the same machine/user where you have your 'aws cli' command (and your AWS CLI profiles) ) 
#
$ mkvirtualenv query-files-app-zappa  --python=python3

# Install dependencies.
(query-files-app-zappa) $ cd file-store-in-s3/query-files-app
pip install -r requirements-in-container.txt
pip install zappa

# Create zappa_settings.yaml as described in 'Developing' chapter below. (It is not included in git due to security concerns.)

# Deploy to AWS.
zappa deploy

# Open Web Browser with url from Zappa's output:
#  (e.g.: Your updated Zappa deployment is live!: https://<your value here>.execute-api.eu-west-2.amazonaws.com/dev  )
#
https://<your value here>.execute-api.eu-west-2.amazonaws.com/dev/v1/domains
https://<your value here>.execute-api.eu-west-2.amazonaws.com/dev/v1/file-download?domain_name=Shell&file_name=Shell%3A0
```


## Developing

### User pool in Cognito

Before you deploy the app first you need to prepare a user pool in Cognito:
- create a new user pool in [Cognito](https://eu-west-2.console.aws.amazon.com/cognito/).
- add a custom attribute `readdomainregex`
- add an app client named `file-store-in-s3-app` 
  - no secret key 
  - disabled: ADMIN_NO_SRP_AUTH, CUSTOM_AUTH_FLOW_ONLY, USER_PASSWORD_AUTH
  - in `Set attribute read and write permissions` make sure 
  the attribute `custom:readdomainregex` (yes, with the prefix "`custom:`", because it was added by Cognito)
  is enabled in section `Readable Attributes`.
- in `App integration -> App client settings` for `App client file-store-in-s3-app`:
  - in `Enabled Identity Providers` enable `Cognito User Pool`.
  - set callback url, e.g. https://o64sert334d.execute-api.eu-west-2.amazonaws.com/dev/v1/domains  (based on Zappa output)
  - in `Allowed OAuth Flows` enable `Authorization code grant`  (and possibly `Implicit grant`)
  - in `Allowed OAuth Scopes` enable `openid` and `profile` (and possibly `email`)
- in `App integration -> Domain name` add your domain prefix, e.g. `file-store-in-s3`.

### New user account in Cognito

You need an email for your new user, e.g. `my-dev-user-name@gmail.com`.

With this email please follow: (example for a user allowed to read access to `bp` and `alos` domains)
```
#
# You need to grab the user pool id, e.g. 'eu-west-2_zwert3', from the previous step.
#
$ aws --profile admin --region eu-west-2 cognito-idp admin-create-user --user-pool-id eu-west-2_zwert3 --username my-dev-user-name@gmail.com --user-attributes=Name=email,Value=my-dev-user-name@gmail.com --message-action SUPPRESS
$ aws --profile admin --region eu-west-2 cognito-idp admin-update-user-attributes --user-pool-id eu-west-2_zwert3 --username my-dev-user-name@gmail.com --user-attributes  Name="custom:readdomainregex",Value="bp|alos"

# To verify you may use:
$ aws --profile admin --region eu-west-2 cognito-idp admin-get-user --user-pool-id eu-west-2_zwert3 --username my-dev-user-name@gmail.com

```


### Creating python dev environment
```
# Create python dev environment.  
#
$ mkvirtualenv query-files-app-zappa  --python=python3

# Install dependencies.
(query-files-app-zappa) $ cd file-store-in-s3/query-files-app
pip install -r requirements.txt
pip install zappa

$ zappa init   # creates a zappa_settings.json
```

### Creating zappa_settings.yaml

```
# Please, convert zappa_settings.json to yaml. (e.g. copy&paste in https://www.json2yaml.com/ )
#

# edit zappa_settings.yaml to include:

$ cat zappa_settings.yaml
---
dev:
  app_function: queryfilesapp.__init__.app
  authorizer:
    type: COGNITO_USER_POOLS
    provider_arns:
      - arn:aws:cognito-idp:{region}:{account_id}:userpool/{user_pool_id}   # your Cognito User Pool (e.g. created in AWS console)
  context_header_mappings:  # specify what claims should be retrieved from ID token and delivered to Flask (by Zappa) 
    email: authorizer.claims.email                                     # currently not used
    cognito-username: authorizer.claims.cognito:username               # currently not used
    read-domain-regex: authorizer.claims.custom:readdomainregex        # used to authorize an HTTP request
  environment_variables:
    QFA_ENVIRONMENT_NAME: "it"                                         # prefix to buckets (Query Files App environment name)
  profile_name: admin        # your aws cli profile with privileges to manage resources in AWS
  project_name: query-files-app
  runtime: python3.6
  s3_bucket: zappa-6jg330n4a   # any bucket will do
```

### Deploy to AWS

```
zappa deploy    # equivalent: zappa deploy dev
Calling deploy for stage dev..
...
Deployment complete!: https://o64sert334d.execute-api.eu-west-2.amazonaws.com/dev

curl https://o64sert334d.execute-api.eu-west-2.amazonaws.com/dev/v1/domains


# Re-deploy in case of new changes in code.
zappa status
zappa update
```

### Create test files in AWS S3

Here is an example of how to create one bucket with three files.
The files will be available via query-files-app (when it is configured to an environment name "`it`")
 to a user which has the claim "`custom:readdomainregex`" set to "`alos|bp|etc`" (in user object created in Cognito user pool).
```
# create dummy files
#
$ mkdir it--alos--456-789 & cd it--alos--456-789
$ touch file1, file3, file3

# create bucket
#
$ aws --profile admin s3api create-bucket --bucket it--alos--456-789 --create-bucket-configuration LocationConstraint=eu-west-2
{
    "Location": "http://it--alos--456-789.s3.amazonaws.com/"
}

# put the dummy files in the bucket
#
$ aws --profile admin s3 sync . s3://it--alos--456-789
```

## See the results

- Open Web Browser with url from Zappa's output:
  -  (e.g.: `Your updated Zappa deployment is live!: https://<your value here>.execute-api.eu-west-2.amazonaws.com/dev ` )
  - `https://<your value here>.execute-api.eu-west-2.amazonaws.com/dev/v1/domains`
  - `https://<your value here>.execute-api.eu-west-2.amazonaws.com/dev/v1/file-download?domain_name=Shell&file_name=Shell%3A0`

- Login as your Cognito user (e.g. my-dev-user-name@gmail.com)
 - Your web browser will be redirected to a new URL.
 - From this URL please copy the query parameter `id_token`. (be careful to not copy too much, there may be also access_token at the end)

- In Postman prepare a GET request with: 
  - header `Authorization` and put here the copied id_token
  - address `https://<your value here>.execute-api.eu-west-2.amazonaws.com/dev/v1/domains`


---
Note:
- You may test (and decode) the `id_token` using AWS [API Gateway](https://eu-west-2.console.aws.amazon.com/apigateway)
  - Navigate to your API Gateway instance `query-files-app-dev`
  - Navigate to `Authorizers` and find one named `ZappaAuthorizer`. Click `Test` and paste the id_token.

- You may also decode the `id_token` at https://jwt.io/ . (your my-dev-user-name@gmail.com and Cognito user pool id will be exposed)

- You may test your API using AWS [API Gateway](https://eu-west-2.console.aws.amazon.com/apigateway) (i.e. without authentication), but you will not see here the actual response - only the response code (200, 400, etc.)
  - Navigate to your API Gateway instance `query-files-app-dev`
  - Navigate to `Resources` and find one named `/{proxy+} - ANY `.
  - Open `Test` client. Provide: Method `GET`, Path `/v1/domains`, Query Strings `read_domain_regex=alos`. Click `Test`.


## @TODO

