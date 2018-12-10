# aws-domain-ip-updater

This is a script that will update a given domain/subdomain for a Route53 managed zone host with the public IP from 
the machine where it is run.

> NOTE: A user/role needs to be created in order to allow the script to perform the operation

# AWS User and Permissions

Create the user:


## Single Account

1. Apply '' policy to user

## Multi-Account 

In a multi-account configuration where users are configured in one account and resources are accessed in a separate account through Roles the following needs to be performed.

1. Create Role in *remote* account here hosted zone exists, apply the "AmazonRoute53FullAccess" Policy allowing the source account wher user exists.

2. Create AssumeRole policy to allow the created user to access the remote account role.


## Configure boto3


# Usage

```
# set boto3 required 
export AWS_PROFILE={}
```