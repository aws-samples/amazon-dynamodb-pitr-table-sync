# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import unittest
from botocore.stub import Stubber
import boto3
from src.table_sync import dynamodb_stream_settings


def test_build_dynamodb_stream_triggers():
    lambda_client = boto3.client("lambda", "us-east-1")
    lambda_stubber = Stubber(lambda_client)
    lambda_stubber.activate()
    source_table_describe_response = {
        "Table": {
            "AttributeDefinitions": [
                {"AttributeName": "department", "AttributeType": "S"},
                {"AttributeName": "email", "AttributeType": "S"},
                {"AttributeName": "phone_number", "AttributeType": "S"},
                {"AttributeName": "salary", "AttributeType": "S"},
            ],
            "TableName": "sample-table",
            "KeySchema": [
                {"AttributeName": "email", "KeyType": "HASH"},
                {"AttributeName": "phone_number", "KeyType": "RANGE"},
            ],
            "TableStatus": "ACTIVE",
            "CreationDateTime": "2020-10-15T20:21:09.725000-04:00",
            "ProvisionedThroughput": {
                "NumberOfDecreasesToday": 0,
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
            "TableSizeBytes": 79,
            "ItemCount": 1,
            "TableArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table",
            "TableId": "d98ecabe-02e3-45cc-8247-72c2ea152468",
            "BillingModeSummary": {
                "BillingMode": "PROVISIONED",
                "LastUpdateToPayPerRequestDateTime": "2022-07-23T20:42:06.471000-04:00",
            },
            "GlobalSecondaryIndexes": [
                {
                    "IndexName": "salary-department-index",
                    "KeySchema": [
                        {"AttributeName": "salary", "KeyType": "HASH"},
                        {"AttributeName": "department", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "IndexStatus": "ACTIVE",
                    "ProvisionedThroughput": {
                        "NumberOfDecreasesToday": 0,
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1,
                    },
                    "IndexSizeBytes": 0,
                    "ItemCount": 0,
                    "IndexArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/index/salary-department"
                    "-index ",
                }
            ],
            "StreamSpecification": {
                "StreamEnabled": True,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "LatestStreamLabel": "2022-05-13T19:00:22.332",
            "LatestStreamArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/stream/2022-05-13T19:00:22"
            ".332",
            "GlobalTableVersion": "2019.11.21",
            "Replicas": [{"RegionName": "ap-south-1", "ReplicaStatus": "ACTIVE"}],
        }
    }
    lambda_stubber.add_response(
        "list_event_source_mappings",
        {
            "EventSourceMappings": [
                {
                    "UUID": "a73e82f9-d895-45db-b836-108516b49644",
                    "StartingPosition": "LATEST",
                    "BatchSize": 1,
                    "MaximumBatchingWindowInSeconds": 0,
                    "ParallelizationFactor": 1,
                    "EventSourceArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/stream/2022-05"
                    "-13T19:00:22 "
                    ".332",
                    "FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:print-event-paylaod",
                    "LastModified": "2022-08-23T19:50:00-04:00",
                    "LastProcessingResult": "No records processed",
                    "State": "Enabled",
                    "StateTransitionReason": "User action",
                    "DestinationConfig": {"OnFailure": {}},
                    "MaximumRecordAgeInSeconds": -1,
                    "BisectBatchOnFunctionError": False,
                    "MaximumRetryAttempts": -1,
                    "TumblingWindowInSeconds": 0,
                    "FunctionResponseTypes": [],
                }
            ]
        },
        {
            "EventSourceArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/stream/2022-05-13T19:00:22"
            ".332"
        },
    )
    expected_cfn_resources = {
        "EventSourceMapping1": {
            "Type": "AWS::Lambda::EventSourceMapping",
            "Properties": {
                "BatchSize": 1,
                "EventSourceArn": {"Fn::GetAtt": ["RestoredTable", "StreamArn"]},
                "MaximumRecordAgeInSeconds": -1,
                "MaximumRetryAttempts": -1,
                "ParallelizationFactor": 1,
                "StartingPosition": "LATEST",
                "FunctionName": "arn:aws:lambda:us-east-1:123456789012:function:print-event-paylaod",
            },
        }
    }
    actual_cfn_resources = dynamodb_stream_settings.build_dynamodb_stream_triggers(
        source_table_describe_response=source_table_describe_response,
        lambda_client=lambda_client,
        restored_table_cfn_logical_name="RestoredTable",
    )
    assert actual_cfn_resources == expected_cfn_resources
    return


def test_build_dynamodb_stream_template_stream_enabled():
    source_table_describe_response = {
        "Table": {
            "AttributeDefinitions": [
                {"AttributeName": "department", "AttributeType": "S"},
                {"AttributeName": "email", "AttributeType": "S"},
                {"AttributeName": "phone_number", "AttributeType": "S"},
                {"AttributeName": "salary", "AttributeType": "S"},
            ],
            "TableName": "sample-table",
            "KeySchema": [
                {"AttributeName": "email", "KeyType": "HASH"},
                {"AttributeName": "phone_number", "KeyType": "RANGE"},
            ],
            "TableStatus": "ACTIVE",
            "CreationDateTime": "2020-10-15T20:21:09.725000-04:00",
            "ProvisionedThroughput": {
                "NumberOfDecreasesToday": 0,
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
            "TableSizeBytes": 79,
            "ItemCount": 1,
            "TableArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table",
            "TableId": "d98ecabe-02e3-45cc-8247-72c2ea152468",
            "BillingModeSummary": {
                "BillingMode": "PROVISIONED",
                "LastUpdateToPayPerRequestDateTime": "2022-07-23T20:42:06.471000-04:00",
            },
            "GlobalSecondaryIndexes": [
                {
                    "IndexName": "salary-department-index",
                    "KeySchema": [
                        {"AttributeName": "salary", "KeyType": "HASH"},
                        {"AttributeName": "department", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "IndexStatus": "ACTIVE",
                    "ProvisionedThroughput": {
                        "NumberOfDecreasesToday": 0,
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1,
                    },
                    "IndexSizeBytes": 0,
                    "ItemCount": 0,
                    "IndexArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/index/salary-department"
                    "-index ",
                }
            ],
            "StreamSpecification": {
                "StreamEnabled": True,
                "StreamViewType": "NEW_AND_OLD_IMAGES",
            },
            "LatestStreamLabel": "2022-05-13T19:00:22.332",
            "LatestStreamArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/stream/2022-05-13T19:00:22"
            ".332",
            "GlobalTableVersion": "2019.11.21",
            "Replicas": [{"RegionName": "ap-south-1", "ReplicaStatus": "ACTIVE"}],
        }
    }
    expected_stream_template = {"StreamViewType": "NEW_AND_OLD_IMAGES"}
    actual_stream_template = dynamodb_stream_settings.build_dynamodb_stream_template(
        source_table_describe_response=source_table_describe_response
    )
    assert expected_stream_template == actual_stream_template


def test_build_dynamodb_stream_template_stream_disabled():
    source_table_describe_response = {
        "Table": {
            "AttributeDefinitions": [
                {"AttributeName": "department", "AttributeType": "S"},
                {"AttributeName": "email", "AttributeType": "S"},
                {"AttributeName": "phone_number", "AttributeType": "S"},
                {"AttributeName": "salary", "AttributeType": "S"},
            ],
            "TableName": "sample-table",
            "KeySchema": [
                {"AttributeName": "email", "KeyType": "HASH"},
                {"AttributeName": "phone_number", "KeyType": "RANGE"},
            ],
            "TableStatus": "ACTIVE",
            "CreationDateTime": "2020-10-15T20:21:09.725000-04:00",
            "ProvisionedThroughput": {
                "NumberOfDecreasesToday": 0,
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
            "TableSizeBytes": 79,
            "ItemCount": 1,
            "TableArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table",
            "TableId": "d98ecabe-02e3-45cc-8247-72c2ea152468",
            "BillingModeSummary": {
                "BillingMode": "PROVISIONED",
                "LastUpdateToPayPerRequestDateTime": "2022-07-23T20:42:06.471000-04:00",
            },
            "GlobalSecondaryIndexes": [
                {
                    "IndexName": "salary-department-index",
                    "KeySchema": [
                        {"AttributeName": "salary", "KeyType": "HASH"},
                        {"AttributeName": "department", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "IndexStatus": "ACTIVE",
                    "ProvisionedThroughput": {
                        "NumberOfDecreasesToday": 0,
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1,
                    },
                    "IndexSizeBytes": 0,
                    "ItemCount": 0,
                    "IndexArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/index/salary-department"
                    "-index ",
                }
            ],
            "LatestStreamLabel": "2022-05-13T19:00:22.332",
            "LatestStreamArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/stream/2022-05-13T19:00:22"
            ".332",
            "GlobalTableVersion": "2019.11.21",
            "Replicas": [{"RegionName": "ap-south-1", "ReplicaStatus": "ACTIVE"}],
        }
    }
    expected_stream_template = None
    actual_stream_template = dynamodb_stream_settings.build_dynamodb_stream_template(
        source_table_describe_response=source_table_describe_response
    )
    assert expected_stream_template == actual_stream_template


if __name__ == "__main__":
    unittest.main()
