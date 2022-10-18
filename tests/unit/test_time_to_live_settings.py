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
