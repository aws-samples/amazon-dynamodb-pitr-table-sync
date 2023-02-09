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

import unittest
from botocore.stub import Stubber
import boto3
from src.table_sync import time_to_live_settings


def test_build_dynamodb_ttl():
    dynamodb_client = boto3.client("dynamodb", "us-east-1")
    dynamodb_stubber = Stubber(dynamodb_client)
    dynamodb_stubber.add_response(
        "describe_time_to_live",
        {
            "TimeToLiveDescription": {
                "TimeToLiveStatus": "ENABLED",
                "AttributeName": "email",
            }
        },
        {"TableName": "source-table"},
    )
    dynamodb_stubber.activate()
    expected_cfn_resources = {"AttributeName": "email", "Enabled": True}
    cfn_resources = time_to_live_settings.build_dynamodb_ttl(
        dynamodb_client=dynamodb_client, source_table_name="source-table"
    )
    assert cfn_resources.__eq__(expected_cfn_resources)


if __name__ == "__main__":
    unittest.main()
