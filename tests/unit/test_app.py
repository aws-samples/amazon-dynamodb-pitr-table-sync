# © 2023 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
# This AWS Content is provided subject to the terms of the AWS Customer Agreement
# available at http://aws.amazon.com/agreement or other written agreement between
# Customer and either Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
#
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import json
import os
import unittest
from unittest import mock
from botocore.stub import Stubber
import boto3
import datetime
from dateutil.tz import *

# Event
event = {
    "Records": [{
        "messageId": "c28d8016-d08e-430c-acfd-c56a60cc0f59",
        "receiptHandle": "AQEBOMbWxzzUutONoLpOzOZDDWSI/bEBHHVse7WuHA/65U9tOnmZ6y+50p"
                         "/uNgJ0mBWXaEiiwFB9e84HOvMgEp2bQ4AKB558Pedhb6Ol3In4nbJ1oIUcSbCKgIHrzf"
                         "/qR3hNwnVB5aEhfzuNZsJOJl6E0blcr/ewGpeMVHtR0sV8"
                         "+DOTLXnBxwOT8hCTU8Hxr4jWjA93s8twewt8GiKkTfhLCOM8nbQPPQ9U40b0gzNAdiMmy1BLHs8poISkuGnszFKxegq"
                         "/BiYTVyQAxZyfYWwCbL2vNy2O8ULCZVoK9+NqgBHh9KWQZ+jQBq0O4Rwq5hLo3MxjootdhIc9MjPsDVdEeXOvXi4b9"
                         "+GNG3DeKFEAl7NbPgj+bjbR0W4OHVww1AtS4EslduCxxZ96bJIbHLrvdg==",
        "body": "{\"version\":\"0\",\"id\":\"8cd6098a-3047-5b72-b786-e7bc72adce04\",\"detail-type\":\"AWS API Call "
                "via CloudTrail\",\"source\":\"aws.dynamodb\",\"account\":\"123456789012\","
                "\"time\":\"2023-02-08T18:01:08Z\",\"region\":\"us-east-1\",\"resources\":[],\"detail\":{"
                "\"eventVersion\":\"1.08\",\"userIdentity\":{\"type\":\"AssumedRole\","
                "\"principalId\":\"AROAID32STDPBXLUODI4U:user\","
                "\"arn\":\"arn:aws:sts::123456789012:assumed-role/user/user-1234\","
                "\"accountId\":\"123456789012\",\"accessKeyId\":\"ASIAYVA662W2KDLAERPC\",\"sessionContext\":{"
                "\"sessionIssuer\":{\"type\":\"Role\",\"principalId\":\"AROAID32STDPBXLUODI4U\","
                "\"arn\":\"arn:aws:iam::123456789012:role/sample-role\",\"accountId\":\"123456789012\","
                "\"userName\":\"sample-role\"},\"attributes\":{\"creationDate\":\"2023-02-08T17:25:03Z\","
                "\"mfaAuthenticated\":\"false\"}}},\"eventTime\":\"2023-02-08T18:01:08Z\","
                "\"eventSource\":\"dynamodb.amazonaws.com\",\"eventName\":\"RestoreTableToPointInTime\","
                "\"awsRegion\":\"us-east-1\",\"sourceIPAddress\":\"72.21.198.66\",\"userAgent\":\"Mozilla/5.0 ("
                "Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 "
                "Safari/537.36\",\"requestParameters\":{"
                "\"sourceTableArn\":\"arn:aws:dynamodb:us-east-1:123456789012:table/source-table\","
                "\"targetTableName\":\"target-table\",\"useLatestRestorableTime\":true,"
                "\"sSESpecificationOverride\":{\"enabled\":false}},\"responseElements\":null,"
                "\"requestID\":\"R6DE9U361P8HP2ODLOEKL70THJVV4KQNSO5AEMVJF66Q9ASUAAJG\","
                "\"eventID\":\"e3545ad4-733b-4b21-82c7-0c2d25922ccd\",\"readOnly\":false,\"resources\":[{"
                "\"accountId\":\"123456789012\",\"type\":\"AWS::DynamoDB::Table\","
                "\"ARN\":\"arn:aws:dynamodb:us-east-1:123456789012:table/target-table"
                "\"},{\"accountId\":\"123456789012\",\"type\":\"AWS::DynamoDB::Table\","
                "\"ARN\":\"arn:aws:dynamodb:us-east-1:123456789012:table/source-table\"}],"
                "\"eventType\":\"AwsApiCall\",\"apiVersion\":\"2012-08-10\",\"managementEvent\":true,"
                "\"recipientAccountId\":\"123456789012\",\"eventCategory\":\"Management\",\"tlsDetails\":{"
                "\"tlsVersion\":\"TLSv1.2\",\"cipherSuite\":\"ECDHE-RSA-AES128-GCM-SHA256\","
                "\"clientProvidedHostHeader\":\"dynamodb.us-east-1.amazonaws.com\"},"
                "\"sessionCredentialFromConsole\":\"true\"}}",
        "attributes": {
            "ApproximateReceiveCount": "1",
            "SentTimestamp": "1675879891729",
            "SenderId": "AROAYVA662W2B6N3KG6RK:amazon-dynamodb-pitr-table-sync-Ama-ReplayFunction-IAeaCAPbPBHc",
            "ApproximateFirstReceiveTimestamp": "1675879898729"
        },
        "messageAttributes": {
            "sqs-dlq-replay-nb": {
                "stringValue": "2",
                "stringListValues": [],
                "binaryListValues": [],
                "dataType": "Number"
            }
        },
        "md5OfMessageAttributes": "bd6a69131cb49cb3c32a5c965e292e55",
        "md5OfBody": "d6dbaaf50e5ded84a3bc0b46f5154076",
        "eventSource": "aws:sqs",
        "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:PITR-Event-Queue",
        "awsRegion": "us-east-1"
    }]
}

# DynamoDB stubber
dynamodb_client = boto3.client("dynamodb", "us-east-1")
dynamodb_stubber = Stubber(dynamodb_client)
dynamodb_stubber.add_response(
    "describe_table",
    {
        "Table": {
            "AttributeDefinitions": [
                {"AttributeName": "accountId", "AttributeType": "S"},
                {"AttributeName": "positionKey", "AttributeType": "S"},
            ],
            "TableName": "source-table",
            "KeySchema": [
                {"AttributeName": "accountId", "KeyType": "HASH"},
                {"AttributeName": "positionKey", "KeyType": "RANGE"},
            ],
            "TableStatus": "ACTIVE",
            "CreationDateTime": datetime.datetime(
                2022, 8, 24, 15, 7, 8, 276000, tzinfo=tzlocal()
            ),
            "ProvisionedThroughput": {
                "NumberOfDecreasesToday": 1,
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
            "TableSizeBytes": 565,
            "ItemCount": 5,
            "TableArn": "arn:aws:dynamodb:us-west-2:123456789012:table/source-table",
            "TableId": "d304ffce-516c-4141-8150-45271c748af0",
            "BillingModeSummary": {
                "BillingMode": "PAY_PER_REQUEST",
                "LastUpdateToPayPerRequestDateTime": datetime.datetime(
                    2022, 8, 24, 15, 7, 8, 276000, tzinfo=tzlocal()
                ),
            },
        },
        "ResponseMetadata": {
            "...": "...",
        },
    },
    {
        "TableName": "target-table"
    },
)

dynamodb_stubber.add_response(
    "describe_table",
    {
        "Table": {
            "AttributeDefinitions": [
                {"AttributeName": "accountId", "AttributeType": "S"},
                {"AttributeName": "positionKey", "AttributeType": "S"},
            ],
            "TableName": "target-table",
            "KeySchema": [
                {"AttributeName": "accountId", "KeyType": "HASH"},
                {"AttributeName": "positionKey", "KeyType": "RANGE"},
            ],
            "TableStatus": "ACTIVE",
            "CreationDateTime": datetime.datetime(
                2022, 8, 24, 15, 7, 8, 276000, tzinfo=tzlocal()
            ),
            "ProvisionedThroughput": {
                "NumberOfDecreasesToday": 1,
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
            "TableSizeBytes": 565,
            "ItemCount": 5,
            "TableArn": "arn:aws:dynamodb:us-west-2:123456789012:table/target-table",
            "TableId": "d304ffce-516c-4141-8150-45271c748af0",
            "BillingModeSummary": {
                "BillingMode": "PAY_PER_REQUEST",
                "LastUpdateToPayPerRequestDateTime": datetime.datetime(
                    2022, 8, 24, 15, 7, 8, 276000, tzinfo=tzlocal()
                ),
            },
            "StreamSpecification": {
                "StreamEnabled": True,
                "StreamViewType": "KEYS_ONLY"
            },
        },
        "ResponseMetadata": {
            "...": "...",
        },
    },
    {
        "TableName": "source-table"
    },
)

dynamodb_stubber.add_response(
    "list_tags_of_resource",
    {
        'Tags': [
            {
                'Key': 'sample-tag-key',
                'Value': 'sample-tag-value'
            },
        ]
    },
    {
        'ResourceArn':'arn:aws:dynamodb:us-east-1:123456789012:table/source-table'
    }
)
dynamodb_stubber.add_response(
    "describe_kinesis_streaming_destination",
    {
        "TableName": "source-table",
        "KinesisDataStreamDestinations": [
            {
                "StreamArn": "arn:aws:kinesis:us-east-1:123456789012:stream/DynamoDB-Test-Stream",
                "DestinationStatus": "ACTIVE"
            }
        ]
    },
    {
        'TableName': 'source-table'
    }
)
dynamodb_stubber.add_response(
    "describe_continuous_backups",
    {
        "ContinuousBackupsDescription": {
            "ContinuousBackupsStatus": "ENABLED",
            "PointInTimeRecoveryDescription": {
                "PointInTimeRecoveryStatus": "ENABLED",
                "EarliestRestorableDateTime": "2023-02-08T12:44:54-05:00",
                "LatestRestorableDateTime": "2023-02-14T09:20:20.997000-05:00"
            }
        }
    },
    {
        'TableName': 'source-table'
    }
)
dynamodb_stubber.add_response(
    "describe_time_to_live",
    {
        "TimeToLiveDescription": {
            "TimeToLiveStatus": "ENABLED",
            "AttributeName": "last_working_day"
        }
    },
    {
        'TableName': 'source-table'
    }
)

# CloudFormation stubber.
cfn_client = boto3.client("cloudformation", "us-east-1")
cfn_stubber = Stubber(cfn_client)

# Line 241
cfn_stubber.add_response(
    'create_change_set',
    {
        'Id': 'test-id',
        'StackId': 'test-stack-id'
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack', 'TemplateBody': '{"AWSTemplateFormatVersion": '
                                                                                '"2010-09-09", "Description": '
                                                                                '"target-table Cloudformation '
                                                                                'deployment", "Resources": {'
                                                                                '"PITRRestoredTable": {"Type": '
                                                                                '"AWS::DynamoDB::Table", '
                                                                                '"DeletionPolicy": "Retain", '
                                                                                '"Properties": {"TableName": '
                                                                                '"target-table", "KeySchema": [{'
                                                                                '"AttributeName": "accountId", '
                                                                                '"KeyType": "HASH"}, '
                                                                                '{"AttributeName": "positionKey", '
                                                                                '"KeyType": "RANGE"}], '
                                                                                '"AttributeDefinitions": [{'
                                                                                '"AttributeName": "accountId", '
                                                                                '"AttributeType": "S"}, '
                                                                                '{"AttributeName": "positionKey", '
                                                                                '"AttributeType": "S"}], '
                                                                                '"BillingMode": '
                                                                                '"PAY_PER_REQUEST"}}}}',
     'ChangeSetName': 'Import-DynamoDB-target-table-Change-Set', 'Description': 'Change set to update the PITR '
                                                                                'restored DynamoDB table',
     'ChangeSetType': 'IMPORT', 'ResourcesToImport': [{'ResourceType': 'AWS::DynamoDB::Table', 'LogicalResourceId':
        'PITRRestoredTable', 'ResourceIdentifier': {'TableName': 'target-table'}}]
     }
)

cfn_stubber.add_response(
    'describe_change_set',
    {
        'ChangeSetName': 'test-id',
        'ChangeSetId': '1234',
        'StackId': 'arn:aws:cloudformation:us-east-1:123456789012:stack/Restored-DynamoDB-Table-target-table-Stack'
                   '-Stack/091bbd50-a7dc-11ed-8b5f-0a2f7ac75f6f',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'Description': 'string',
        'CreationTime': datetime.datetime(2015, 1, 1),
        'Status': 'CREATE_COMPLETE',
        'StatusReason': 'string',
        'Capabilities': [
            'CAPABILITY_IAM',
        ],
    },
    {
        'ChangeSetName': 'test-id',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)

cfn_stubber.add_response(
    'execute_change_set',
    {},
    {
        'ChangeSetName': 'test-id',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)

cfn_stubber.add_response(
    'describe_stacks',
    {
        'Stacks': [
            {
                'StackId': 'string',
                'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
                'ChangeSetId': 'string',
                'Description': 'string',
                'CreationTime': datetime.datetime(2015, 1, 1),
                'DeletionTime': datetime.datetime(2015, 1, 1),
                'LastUpdatedTime': datetime.datetime(2015, 1, 1),
                'StackStatus': 'IMPORT_COMPLETE',
                'StackStatusReason': 'string',
                'DisableRollback': False,
                'TimeoutInMinutes': 123,
                'Capabilities': [
                   'CAPABILITY_NAMED_IAM',
                ],
            },
        ],
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)

# Line 271
cfn_stubber.add_response(
    'create_change_set',
    {
        'Id': 'Update-DynamoDB-target-table-Tags-Change-Set',
        'StackId': 'Restored-DynamoDB-Table-target-table-Stack'
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'TemplateBody': json.dumps({
            'AWSTemplateFormatVersion': '2010-09-09',
            'Description': 'target-table Cloudformation deployment',
            'Resources': {
                'PITRRestoredTable': {
                    'Type': 'AWS::DynamoDB::Table',
                    'DeletionPolicy': 'Retain',
                    'Properties': {
                        'TableName': 'target-table',
                        'KeySchema': [{
                            'AttributeName': 'accountId',
                            'KeyType': 'HASH'
                        }, {
                            'AttributeName': 'positionKey',
                            'KeyType': 'RANGE'
                        }],
                        'AttributeDefinitions': [{
                            'AttributeName': 'accountId',
                            'AttributeType': 'S'
                        }, {
                            'AttributeName': 'positionKey',
                            'AttributeType': 'S'
                        }],
                        'BillingMode': 'PAY_PER_REQUEST',
                        'Tags': [{
                            'Key': 'sample-tag-key',
                            'Value': 'sample-tag-value'
                        }]
                    }
                }
            }
        }),
        'ChangeSetName': 'Update-DynamoDB-target-table-Tags-Change-Set',
        'Description': 'Change set to update the PITR restored DynamoDB table',
        'ChangeSetType': 'UPDATE',
     }
)
cfn_stubber.add_response(
    'describe_change_set',
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-Tags-Change-Set',
        'ChangeSetId': '1234',
        'StackId': 'arn:aws:cloudformation:us-east-1:123456789012:stack/Restored-DynamoDB-Table-target-table-Stack'
                   '-Stack/091bbd50-a7dc-11ed-8b5f-0a2f7ac75f6f',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'Description': 'string',
        'CreationTime': datetime.datetime(2015, 1, 1),
        'Status': 'CREATE_COMPLETE',
        'StatusReason': 'string',
        'Capabilities': [
            'CAPABILITY_IAM',
        ],
    },
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-Tags-Change-Set',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
cfn_stubber.add_response(
    'execute_change_set',
    {},
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-Tags-Change-Set',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
cfn_stubber.add_response(
    'describe_stacks',
    {
        'Stacks': [
            {
                'StackId': 'string',
                'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
                'ChangeSetId': 'string',
                'Description': 'string',
                'CreationTime': datetime.datetime(2015, 1, 1),
                'DeletionTime': datetime.datetime(2015, 1, 1),
                'LastUpdatedTime': datetime.datetime(2015, 1, 1),
                'StackStatus': 'UPDATE_COMPLETE',
                'StackStatusReason': 'string',
                'DisableRollback': False,
                'TimeoutInMinutes': 123,
                'Capabilities': [
                   'CAPABILITY_NAMED_IAM',
                ],
            },
        ],
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)

# Line 291
cfn_stubber.add_response(
    'create_change_set',
    {
        'Id': 'Update-DynamoDB-target-table-Stream-Change-Set',
        'StackId': 'Restored-DynamoDB-Table-target-table-Stack'
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'TemplateBody': json.dumps({
            'AWSTemplateFormatVersion': '2010-09-09',
            'Description': 'target-table Cloudformation deployment',
            'Resources': {
                'PITRRestoredTable': {
                    'Type': 'AWS::DynamoDB::Table',
                    'DeletionPolicy': 'Retain',
                    'Properties': {
                        'TableName': 'target-table',
                        'KeySchema': [{
                            'AttributeName': 'accountId',
                            'KeyType': 'HASH'
                        }, {
                            'AttributeName': 'positionKey',
                            'KeyType': 'RANGE'
                        }],
                        'AttributeDefinitions': [{
                            'AttributeName': 'accountId',
                            'AttributeType': 'S'
                        }, {
                            'AttributeName': 'positionKey',
                            'AttributeType': 'S'
                        }],
                        'BillingMode': 'PAY_PER_REQUEST',
                        'Tags': [{
                            'Key': 'sample-tag-key',
                            'Value': 'sample-tag-value'
                        }],
                        'StreamSpecification': {
                            'StreamViewType': 'KEYS_ONLY',
                        },
                    }
                }
            }
        }),
        'ChangeSetName': 'Update-DynamoDB-target-table-Stream-Change-Set',
        'Description': 'Change set to update the PITR restored DynamoDB table',
        'ChangeSetType': 'UPDATE',
     }
)
cfn_stubber.add_response(
    'describe_change_set',
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-Stream-Change-Set',
        'ChangeSetId': '1234',
        'StackId': 'arn:aws:cloudformation:us-east-1:123456789012:stack/Restored-DynamoDB-Table-target-table-Stack'
                   '-Stack/091bbd50-a7dc-11ed-8b5f-0a2f7ac75f6f',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'Description': 'string',
        'CreationTime': datetime.datetime(2015, 1, 1),
        'Status': 'CREATE_COMPLETE',
        'StatusReason': 'string',
        'Capabilities': [
            'CAPABILITY_IAM',
        ],
    },
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-Stream-Change-Set',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
cfn_stubber.add_response(
    'execute_change_set',
    {},
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-Stream-Change-Set',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
cfn_stubber.add_response(
    'describe_stacks',
    {
        'Stacks': [
            {
                'StackId': 'string',
                'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
                'ChangeSetId': 'string',
                'Description': 'string',
                'CreationTime': datetime.datetime(2015, 1, 1),
                'DeletionTime': datetime.datetime(2015, 1, 1),
                'LastUpdatedTime': datetime.datetime(2015, 1, 1),
                'StackStatus': 'UPDATE_COMPLETE',
                'StackStatusReason': 'string',
                'DisableRollback': False,
                'TimeoutInMinutes': 123,
                'Capabilities': [
                   'CAPABILITY_NAMED_IAM',
                ],
            },
        ],
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)

# Line 332
cfn_stubber.add_response(
    'create_change_set',
    {
        'Id': 'Update-DynamoDB-target-table-Kinesis-Settings-Change-Set',
        'StackId': 'Restored-DynamoDB-Table-target-table-Stack'
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'TemplateBody': json.dumps({
            'AWSTemplateFormatVersion': '2010-09-09',
            'Description': 'target-table Cloudformation deployment',
            'Resources': {
                'PITRRestoredTable': {
                    'Type': 'AWS::DynamoDB::Table',
                    'DeletionPolicy': 'Retain',
                    'Properties': {
                        'TableName': 'target-table',
                        'KeySchema': [{
                            'AttributeName': 'accountId',
                            'KeyType': 'HASH'
                        }, {
                            'AttributeName': 'positionKey',
                            'KeyType': 'RANGE'
                        }],
                        'AttributeDefinitions': [{
                            'AttributeName': 'accountId',
                            'AttributeType': 'S'
                        }, {
                            'AttributeName': 'positionKey',
                            'AttributeType': 'S'
                        }],
                        'BillingMode': 'PAY_PER_REQUEST',
                        'Tags': [{
                            'Key': 'sample-tag-key',
                            'Value': 'sample-tag-value'
                        }],
                        'StreamSpecification': {
                            'StreamViewType': 'KEYS_ONLY',
                        },
                        'KinesisStreamSpecification': {
                            'StreamArn': 'arn:aws:kinesis:us-east-1:123456789012:stream/DynamoDB-Test-Stream',
                        }
                    }
                }
            }
        }),
        'ChangeSetName': 'Update-DynamoDB-target-table-Kinesis-Settings-Change-Set',
        'Description': 'Change set to update the PITR restored DynamoDB table',
        'ChangeSetType': 'UPDATE',
     }
)
cfn_stubber.add_response(
    'describe_change_set',
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-Kinesis-Settings-Change-Set',
        'ChangeSetId': '1234',
        'StackId': 'arn:aws:cloudformation:us-east-1:123456789012:stack/Restored-DynamoDB-Table-target-table-Stack'
                   '-Stack/091bbd50-a7dc-11ed-8b5f-0a2f7ac75f6f',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'Description': 'string',
        'CreationTime': datetime.datetime(2015, 1, 1),
        'Status': 'CREATE_COMPLETE',
        'StatusReason': 'string',
        'Capabilities': [
            'CAPABILITY_IAM',
        ],
    },
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-Kinesis-Settings-Change-Set',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
cfn_stubber.add_response(
    'execute_change_set',
    {},
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-Kinesis-Settings-Change-Set',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
cfn_stubber.add_response(
    'describe_stacks',
    {
        'Stacks': [
            {
                'StackId': 'string',
                'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
                'ChangeSetId': 'string',
                'Description': 'string',
                'CreationTime': datetime.datetime(2015, 1, 1),
                'DeletionTime': datetime.datetime(2015, 1, 1),
                'LastUpdatedTime': datetime.datetime(2015, 1, 1),
                'StackStatus': 'UPDATE_COMPLETE',
                'StackStatusReason': 'string',
                'DisableRollback': False,
                'TimeoutInMinutes': 123,
                'Capabilities': [
                   'CAPABILITY_NAMED_IAM',
                ],
            },
        ],
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)

# Line 352
cfn_stubber.add_response(
    'create_change_set',
    {
        'Id': 'Update-DynamoDB-target-table-PITR-Settings-Change-Set',
        'StackId': 'Restored-DynamoDB-Table-target-table-Stack'
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'TemplateBody': json.dumps({
            'AWSTemplateFormatVersion': '2010-09-09',
            'Description': 'target-table Cloudformation deployment',
            'Resources': {
                'PITRRestoredTable': {
                    'Type': 'AWS::DynamoDB::Table',
                    'DeletionPolicy': 'Retain',
                    'Properties': {
                        'TableName': 'target-table',
                        'KeySchema': [{
                            'AttributeName': 'accountId',
                            'KeyType': 'HASH'
                        }, {
                            'AttributeName': 'positionKey',
                            'KeyType': 'RANGE'
                        }],
                        'AttributeDefinitions': [{
                            'AttributeName': 'accountId',
                            'AttributeType': 'S'
                        }, {
                            'AttributeName': 'positionKey',
                            'AttributeType': 'S'
                        }],
                        'BillingMode': 'PAY_PER_REQUEST',
                        'Tags': [{
                            'Key': 'sample-tag-key',
                            'Value': 'sample-tag-value'
                        }],
                        'StreamSpecification': {
                            'StreamViewType': 'KEYS_ONLY',
                        },
                        'KinesisStreamSpecification': {
                            'StreamArn': 'arn:aws:kinesis:us-east-1:123456789012:stream/DynamoDB-Test-Stream',
                        },
                        'PointInTimeRecoverySpecification': {
                            'PointInTimeRecoveryEnabled': True
                        }
                    }
                }
            }
        }),
        'ChangeSetName': 'Update-DynamoDB-target-table-PITR-Settings-Change-Set',
        'Description': 'Change set to update the PITR restored DynamoDB table',
        'ChangeSetType': 'UPDATE',
     }
)
cfn_stubber.add_response(
    'describe_change_set',
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-PITR-Settings-Change-Set',
        'ChangeSetId': '1234',
        'StackId': 'arn:aws:cloudformation:us-east-1:123456789012:stack/Restored-DynamoDB-Table-target-table-Stack'
                   '-Stack/091bbd50-a7dc-11ed-8b5f-0a2f7ac75f6f',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'Description': 'string',
        'CreationTime': datetime.datetime(2015, 1, 1),
        'Status': 'CREATE_COMPLETE',
        'StatusReason': 'string',
        'Capabilities': [
            'CAPABILITY_IAM',
        ],
    },
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-PITR-Settings-Change-Set',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
cfn_stubber.add_response(
    'execute_change_set',
    {},
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-PITR-Settings-Change-Set',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
cfn_stubber.add_response(
    'describe_stacks',
    {
        'Stacks': [
            {
                'StackId': 'string',
                'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
                'ChangeSetId': 'string',
                'Description': 'string',
                'CreationTime': datetime.datetime(2015, 1, 1),
                'DeletionTime': datetime.datetime(2015, 1, 1),
                'LastUpdatedTime': datetime.datetime(2015, 1, 1),
                'StackStatus': 'UPDATE_COMPLETE',
                'StackStatusReason': 'string',
                'DisableRollback': False,
                'TimeoutInMinutes': 123,
                'Capabilities': [
                   'CAPABILITY_NAMED_IAM',
                ],
            },
        ],
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)

# Line 372
cfn_stubber.add_response(
    'create_change_set',
    {
        'Id': 'Update-DynamoDB-target-table-TTL-Settings-Change-Set',
        'StackId': 'Restored-DynamoDB-Table-target-table-Stack'
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'TemplateBody': json.dumps({
            'AWSTemplateFormatVersion': '2010-09-09',
            'Description': 'target-table Cloudformation deployment',
            'Resources': {
                'PITRRestoredTable': {
                    'Type': 'AWS::DynamoDB::Table',
                    'DeletionPolicy': 'Retain',
                    'Properties': {
                        'TableName': 'target-table',
                        'KeySchema': [{
                            'AttributeName': 'accountId',
                            'KeyType': 'HASH'
                        }, {
                            'AttributeName': 'positionKey',
                            'KeyType': 'RANGE'
                        }],
                        'AttributeDefinitions': [{
                            'AttributeName': 'accountId',
                            'AttributeType': 'S'
                        }, {
                            'AttributeName': 'positionKey',
                            'AttributeType': 'S'
                        }],
                        'BillingMode': 'PAY_PER_REQUEST',
                        'Tags': [{
                            'Key': 'sample-tag-key',
                            'Value': 'sample-tag-value'
                        }],
                        'StreamSpecification': {
                            'StreamViewType': 'KEYS_ONLY',
                        },
                        'KinesisStreamSpecification': {
                            'StreamArn': 'arn:aws:kinesis:us-east-1:123456789012:stream/DynamoDB-Test-Stream',
                        },
                        'PointInTimeRecoverySpecification': {
                            'PointInTimeRecoveryEnabled': True
                        },
                        'TimeToLiveSpecification': {
                            'AttributeName': 'last_working_day',
                            'Enabled': True
                        }
                    }
                }
            }
        }),
        'ChangeSetName': 'Update-DynamoDB-target-table-TTL-Settings-Change-Set',
        'Description': 'Change set to update the PITR restored DynamoDB table',
        'ChangeSetType': 'UPDATE',
     }
)
cfn_stubber.add_response(
    'describe_change_set',
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-TTL-Settings-Change-Set',
        'ChangeSetId': '1234',
        'StackId': 'arn:aws:cloudformation:us-east-1:123456789012:stack/Restored-DynamoDB-Table-target-table-Stack'
                   '-Stack/091bbd50-a7dc-11ed-8b5f-0a2f7ac75f6f',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
        'Description': 'string',
        'CreationTime': datetime.datetime(2015, 1, 1),
        'Status': 'CREATE_COMPLETE',
        'StatusReason': 'string',
        'Capabilities': [
            'CAPABILITY_IAM',
        ],
    },
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-TTL-Settings-Change-Set',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
cfn_stubber.add_response(
    'execute_change_set',
    {},
    {
        'ChangeSetName': 'Update-DynamoDB-target-table-TTL-Settings-Change-Set',
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
cfn_stubber.add_response(
    'describe_stacks',
    {
        'Stacks': [
            {
                'StackId': 'string',
                'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
                'ChangeSetId': 'string',
                'Description': 'string',
                'CreationTime': datetime.datetime(2015, 1, 1),
                'DeletionTime': datetime.datetime(2015, 1, 1),
                'LastUpdatedTime': datetime.datetime(2015, 1, 1),
                'StackStatus': 'UPDATE_COMPLETE',
                'StackStatusReason': 'string',
                'DisableRollback': False,
                'TimeoutInMinutes': 123,
                'Capabilities': [
                   'CAPABILITY_NAMED_IAM',
                ],
            },
        ],
    },
    {
        'StackName': 'Restored-DynamoDB-Table-target-table-Stack',
    }
)
# Lambda stubber.
lambda_client = boto3.client("lambda", "us-east-1")
lambda_stubber = Stubber(lambda_client)

# Application Autoscaling stubber.
app_autoscaling_client = boto3.client("application-autoscaling", "us-east-1")
app_autoscaling_stubber = Stubber(app_autoscaling_client)


def test_app():
    with mock.patch.dict(os.environ, {
                         "LOG_LEVEL": "INFO",
                         "AWS_REGION": "us-east-1",
                         "ACCOUNT_ID": "123456789012",
                         "PARTITION": "aws",
                         "ENABLE_TAG_SETTINGS": "true",
                         "ENABLE_KINESIS_SETTINGS": "true",
                         "ENABLE_DYNAMODB_STREAM_SETTINGS": "true",
                         "ENABLE_TTL_SETTINGS": "true",
                         "ENABLE_PITR_SETTINGS": "true",
                         "ENABLE_AUTO_SCALING_SETTINGS": "false",
                         "ENABLE_DYNAMODB_LAMBDA_TRIGGERS": "true",
                         "AWS_DEFAULT_REGION": "us-east-1"}):
        from table_sync import app
        with mock.patch('table_sync.app.CFN', cfn_client):
            with mock.patch('table_sync.app.LAMBDA', lambda_client):
                with mock.patch('table_sync.app.DDB', dynamodb_client):
                    with mock.patch('table_sync.app.APP_AUTO_SCALING', app_autoscaling_client):
                        # Activate all stubber.
                        dynamodb_stubber.activate()
                        cfn_stubber.activate()
                        lambda_stubber.activate()
                        app_autoscaling_stubber.activate()
                        handler_return = app.lambda_handler(event, None)
                        assert handler_return == True

                        # Deactivate all stubber.
                        dynamodb_stubber.deactivate()
                        cfn_stubber.deactivate()
                        lambda_stubber.deactivate()
                        app_autoscaling_stubber.deactivate()


if __name__ == "__main__":
    unittest.main()
