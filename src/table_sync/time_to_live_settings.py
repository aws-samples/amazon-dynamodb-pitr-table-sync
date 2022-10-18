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

from aws_lambda_powertools import Logger

LOG: Logger = Logger(service=__name__)


def build_dynamodb_ttl(dynamodb_client: object, source_table_name: str):
    """Builds CFN template for the DynamoDB TTL settings.

    Args:
        dynamodb_client: Authenticated DynamoDB boto3 client.
        source_table_name: The source table name.

    Returns:
      A valid dict for the CFN template YAML for the DynamoDB Table TTL settings.

    Raises:
    """
    response = dynamodb_client.describe_time_to_live(TableName=source_table_name)
    time_to_live_status: str
    attribute_name: str
    if response.get("TimeToLiveDescription"):
        time_to_live_status = response.get("TimeToLiveDescription").get("TimeToLiveStatus", None)
        attribute_name = response.get("TimeToLiveDescription").get("AttributeName", None)

        LOG.info(f"Source table TTL settings: {response.get('TimeToLiveDescription')}")
        if time_to_live_status == "ENABLED" or time_to_live_status == "ENABLING":
            return {"AttributeName": attribute_name, "Enabled": True}

    return None
