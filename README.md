# AWS Incident Response Kit (AIRK)

The idea of this is to have a module (plugin) based AWS response tool.

# Using

### Help

```
python .\aws_respond.py -h

usage: aws_respond.py [-h] [--module MODULE] [--listmodules LISTMODULES]
                      [--moduledetails MODULEDETAILS] [--dryrun DRYRUN]
                      [--instanceids INSTANCEIDS [INSTANCEIDS ...]]
                      [--sgids SGIDS [SGIDS ...]]
                      [--vpcids VPCIDS [VPCIDS ...]]
                      [--usernames USERNAMES [USERNAMES ...]]
                      [--accesskeyids ACCESSKEYIDS [ACCESSKEYIDS ...]]
                      [--values VALUES [VALUES ...]]

AWS Incident Response Kit (AIRK).

optional arguments:
  -h, --help            show this help message and exit
  --module MODULE       Specify the module (action) you want to run.
  --listmodules LISTMODULES
                        Lists all of the available modules (actions).
  --moduledetails MODULEDETAILS
                        Lists descriptions of the available modules.
  --dryrun DRYRUN       If you want to run a dryrun first before going live
                        with a module.
  --instanceids INSTANCEIDS [INSTANCEIDS ...]
                        Instance ID(s).
  --sgids SGIDS [SGIDS ...]
                        Security Group ID(s).
  --vpcids VPCIDS [VPCIDS ...]
                        VPC ID(s).
  --usernames USERNAMES [USERNAMES ...]
                        Username(s)
  --accesskeyids ACCESSKEYIDS [ACCESSKEYIDS ...]
                        Access key(s) ID.
  --values VALUES [VALUES ...]
                        These are values that are needed for modules to work
                        properly. This can be anything.
```

### List Modules

```
python .\aws_respond.py --listmodules

userlogins
```

### Get Module Details

```
python .\aws_respond.py --moduledetails

USERLOGINS
    Module:      userlogins
    Author:      Patrick Olsen
    Version:     0.1
    Date:        2018-09-13
    Description: Lists the user logins. Includes username, userid, created date and password last used date.
```

### Running a module:

This is an example of running the userlogins module. The modules can be anything you create and then just pass them as --module <module_name>

Each module should have a .module description file as well. This gives information about the module.

I will develop more as time goes on. Feel free to add any you find interesting.

```
python .\aws_respond.py --module userlogins --dryrun False

[
    {
        "UserName": "dfir",
        "UserId": "AID<snip>HKW",
        "CreateDate": "2018-08-13T20:47:17+00:00",
        "PasswordLastUsed": null
    },
    {
        "UserName": "polsen",
        "UserId": "AID<snip>KWUY",
        "CreateDate": "2017-10-12T18:38:32+00:00",
        "PasswordLastUsed": "2018-09-17T11:23:22+00:00"
    }
]
```

It's possible to disable all of the access keys for one or more users using the disableaccesskeys module.

```
python .\aws_respond.py --module disableaccesskeys --usernames dfirtest polsen

[
    {
        "UserName": "dfirtest",
        "AccessKeyId": "AK<snip>DQ",
        "Result": "Successful"
    },
    {
        "UserName": "dfirtest",
        "AccessKeyId": "AK<snip>7A",
        "Result": "Successful"
    },
    {
        "UserName": "polsen",
        "AccessKeyId": "AK<snip>CA",
        "Result": "Successful"
    },
    {
        "UserName": "polsen",
        "AccessKeyId": "AK<snip>DQ",
        "Result": "Successful"
    }
]
```