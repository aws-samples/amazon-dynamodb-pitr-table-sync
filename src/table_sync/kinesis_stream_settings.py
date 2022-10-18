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


def build_kinesis_stream_template(dynamodb_client: object, source_table_name: str = ""):
    """Builds a CFN template for the DynamoDB table kinesis stream settings.

    Args:
        dynamodb_client: Authenticated DynamoDB boto3 client.
        source_table_name: The name of the source table.

    Returns:
      A dictionary representing CFN yaml for the Kinesis Stream settings of a DynamoDB table

    Raises:
    """
    kinesis_stream_arn = ""
    kinesis_stream_specification = {}
    response = dynamodb_client.describe_kinesis_streaming_destination(
        TableName=source_table_name
    )
    kinesis_stream_destinations = response.get("KinesisDataStreamDestinations", [])
    LOG.info(f"Source table kinesis stream destinations: {kinesis_stream_destinations}")

    if kinesis_stream_destinations:
        kinesis_stream_arn = kinesis_stream_destinations[0].get("StreamArn", None)
    LOG.info(f"Kinesis stream ARN: {kinesis_stream_arn}")

    if kinesis_stream_arn:
        kinesis_stream_specification.update(StreamArn=kinesis_stream_arn)
    LOG.info(f"Kinesis stream specification: {kinesis_stream_specification}")

    return kinesis_stream_specification
