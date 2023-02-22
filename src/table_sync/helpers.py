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

from pydantic import BaseModel
from botocore.utils import ArnParser


def parse_arn(arn: str = None):
    return Arn(**ArnParser.parse_arn(None, arn))


def is_dynamodb_table_available(dynamodb_client, target_table_name: str = ""):
    """Checks if the DynamoDB table is in ACTIVE status.

    Args:
        dynamodb_client: Authenticated DynamoDB boto3 client.
        target_table_name: The name of the table.


    Returns:
      A boolean indicating whether the table is in ACTIVE state.

    Raises:
      ResourceNotFound: If the DynamoDB table doesn't exist/
    """
    try:
        response = dynamodb_client.describe_table(TableName=target_table_name)
        table_status = response.get("Table").get("TableStatus")
        return table_status == "ACTIVE"
    except Exception as error:
        raise error


class Arn(BaseModel):
    partition: str
    service: str
    region: str
    account: str
    resource: str
