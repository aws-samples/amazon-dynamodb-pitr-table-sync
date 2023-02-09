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

from aws_lambda_powertools import Logger

LOG: Logger = Logger(service=__name__)


def build_point_in_time_recovery_template(dynamodb_client: object, source_table_name: str = ""):
    """Build a CFN template for the PITR settings for the DynamoDB table.

    Args:
        dynamodb_client: Authenticated DynamoDB boto3 client.
        source_table_name: The name of the source table.

    Returns:
      A dictionary representing CFN yaml for the PITR settings of a DynamoDB table

    Raises:
    """
    response = dynamodb_client.describe_continuous_backups(TableName=source_table_name)
    pitr_status = (
        response.get("ContinuousBackupsDescription")
        .get("PointInTimeRecoveryDescription")
        .get("PointInTimeRecoveryStatus")
    )
    pitr_specification = {"PointInTimeRecoveryEnabled": pitr_status == "ENABLED"}
    LOG.info(f"PITR settings: {pitr_specification}")
    return pitr_specification
