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
from src.table_sync import helpers
import datetime
from dateutil.tz import *


def test_is_dynamodb_table_available_table_active():
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
                "TableName": "RetailTransactionHistory1",
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
                "TableArn": "arn:aws:dynamodb:us-west-2:705472046880:table/RetailTransactionHistory1",
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
        {"TableName": "tgt-table"},
    )
    dynamodb_stubber.activate()
    expected_cfn_resources = True
    cfn_resources = helpers.is_dynamodb_table_available(
        dynamodb_client=dynamodb_client, target_table_name="tgt-table"
    )

    assert cfn_resources == expected_cfn_resources
    dynamodb_stubber.deactivate()


def test_is_dynamodv_table_available_table_not_active():
    dynamodb_client = boto3.client("dynamodb", "us-east-1")
    dynamodb_stubber = Stubber(dynamodb_client)
    dynamodb_stubber.add_response(
        "describe_table",
        {
            "Table": {
                "AttributeDefinitions": [{"AttributeName": "Id", "AttributeType": "N"}],
                "TableName": "ProductCatalog123",
                "KeySchema": [{"AttributeName": "Id", "KeyType": "HASH"}],
                "TableStatus": "CREATING",
                "CreationDateTime": datetime.datetime(
                    2022, 8, 28, 16, 1, 20, 278000, tzinfo=tzlocal()
                ),
                "ProvisionedThroughput": {
                    "NumberOfDecreasesToday": 1,
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1,
                },
                "TableSizeBytes": 0,
                "ItemCount": 0,
                "TableArn": "arn:aws:dynamodb:us-west-2:705472046880:table/ProductCatalog123",
                "TableId": "cefdf94f-7164-4fe6-928f-ae9c283ec081",
                "BillingModeSummary": {"BillingMode": "PROVISIONED"},
                "RestoreSummary": {
                    "SourceTableArn": "arn:aws:dynamodb:us-west-2:705472046880:table/ProductCatalog",
                    "RestoreDateTime": datetime.datetime(
                        2022, 8, 28, 15, 56, 20, 357000, tzinfo=tzlocal()
                    ),
                    "RestoreInProgress": True,
                },
            },
            "ResponseMetadata": {
                "...": "...",
            },
        },
        {"TableName": "tgt-table"},
    )
    dynamodb_stubber.activate()
    expected_cfn_resources = False
    cfn_resources = helpers.is_dynamodb_table_available(
        dynamodb_client=dynamodb_client, target_table_name="tgt-table"
    )
    assert cfn_resources == expected_cfn_resources
    dynamodb_stubber.deactivate()


def test_parse_arn():
    expected_cfn_resources = {
        "partition": "aws",
        "service": "dynamodb",
        "region": "us-west-2",
        "account": "123456789012",
        "resource": "table/ProductCatalog",
    }
    tgt_arn = "arn:aws:dynamodb:us-west-2:123456789012:table/ProductCatalog"
    cfn_resources = helpers.parse_arn(tgt_arn)

    assert cfn_resources.partition == expected_cfn_resources["partition"]
    assert cfn_resources.service == expected_cfn_resources["service"]
    assert cfn_resources.region == expected_cfn_resources["region"]
    assert cfn_resources.account == expected_cfn_resources["account"]
    assert cfn_resources.resource == expected_cfn_resources["resource"]


if __name__ == "__main__":
    unittest.main()
