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
from src.table_sync import pitr_settings


def test_build_point_in_time_recovery_template():
    dynamodb_client = boto3.client("dynamodb", "us-east-1")
    dynamodb_stubber = Stubber(dynamodb_client)
    dynamodb_stubber.add_response(
        "describe_continuous_backups",
        {
            "ContinuousBackupsDescription": {
                "ContinuousBackupsStatus": "ENABLED",
                "PointInTimeRecoveryDescription": {
                    "PointInTimeRecoveryStatus": "ENABLED",
                    "EarliestRestorableDateTime": "2022-07-20T14:35:28.111000-04:00",
                    "LatestRestorableDateTime": "2022-08-24T14:30:28.111000-04:00",
                },
            }
        },
        {"TableName": "source-table"},
    )
    dynamodb_stubber.activate()
    expected_cfn_resources = {"PointInTimeRecoveryEnabled": True}
    cfn_resources = pitr_settings.build_point_in_time_recovery_template(
        dynamodb_client=dynamodb_client, source_table_name="source-table"
    )
    assert cfn_resources.__eq__(expected_cfn_resources)


if __name__ == "__main__":
    unittest.main()
