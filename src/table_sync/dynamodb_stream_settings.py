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
from table_sync.cfn_yaml_template import create_basic_event_source_mapping_cfn

LOG: Logger = Logger(service=__name__)


def build_dynamodb_stream_triggers(
    lambda_client: object, source_table_describe_response: dict, restored_table_cfn_logical_name: str = ""
):
    """Builds CFN template for the DynamoDB table stream triggers.

    Args:
        lambda_client: Authenticated AWS Lambda boto3 client.
        source_table_describe_response: The DynamoDB describe_table API response for the source table.
        restored_table_cfn_logical_name: The logical name of the restored DynamoDB table in the CFN template.

    Returns:
      A yaml for the valid CFN template for DynamoDB stream triggers.

    Raises:
    """
    resources = {}
    # Get the latest stream arn.
    # List the event source mappings for the source table stream using the latest stream arn.
    latest_stream_arn = source_table_describe_response.get("Table").get("LatestStreamArn", "")
    if not latest_stream_arn:
        return None

    # Define all the event source mappings properties.
    event_source_properties = [
        "BatchSize",
        "BisectBatchOnFunctionError",
        "DestinationConfig",
        "Enabled",
        "EventSourceArn",
        "FilterCriteria",
        "FunctionResponseTypes",
        "MaximumBatchingWindowInSeconds",
        "MaximumRecordAgeInSeconds",
        "MaximumRetryAttempts",
        "ParallelizationFactor",
        "Queues",
        "SelfManagedEventSource",
        "SourceAccessConfigurations",
        "StartingPosition",
        "StartingPositionTimestamp",
        "Topics",
        "TumblingWindowInSeconds",
    ]

    # Create list of all the event source mappings for the DynamoDB stream.
    # Retrieve all the event source mappings.
    event_source_mappings: list = []
    if latest_stream_arn:
        response = lambda_client.list_event_source_mappings(
            EventSourceArn=latest_stream_arn,
        )
        event_source_mappings = response.get("EventSourceMappings", [])

    if not event_source_mappings:
        return None

    # Create CFN resources for all the event source mappings.
    LOG.info(f"Source table DynamoDB stream triggers: {event_source_mappings}")
    for i, event_source in enumerate(event_source_mappings):
        # Create CFN resource for each event source.
        basic_cfn = create_basic_event_source_mapping_cfn()
        properties = basic_cfn.get("Properties")
        for cfn_property in event_source_properties:
            if event_source.get(cfn_property):
                properties.update({cfn_property: event_source.get(cfn_property)})

        # Replace the event source arn as it will be the target table stream.
        properties.update(EventSourceArn={"Fn::GetAtt": [restored_table_cfn_logical_name, "StreamArn"]})

        # Add the function name.
        properties.update(FunctionName=event_source.get("FunctionArn"))

        # Destination config (even if empty) is included in the boto3 response but empty values aren't allowed in CFN.
        if not properties.get("DestinationConfig").get("OnFailure"):
            del properties["DestinationConfig"]

        # Add the resource.
        resources.update({f"EventSourceMapping{i+1}": basic_cfn})
    return resources


def build_dynamodb_stream_template(
    source_table_describe_response=None,
):
    """Builds CFN template for the DynamoDB stream settings.

    Args:
      source_table_describe_response: The DynamoDB describe_table API response for source DynamoDB table.

    Returns:
      A valid dict for the CFN template YAML for the DynamoDB Table stream settings.

    Raises:
    """
    # Get the StreamSpecification from the describe table response.
    if source_table_describe_response is None:
        source_table_describe_response = {}
    stream_enabled: bool = False
    stream_view_type: str = ""
    stream_specification = source_table_describe_response.get("Table").get("StreamSpecification", {})
    LOG.info(f"Source table stream settings: {stream_specification}")
    if stream_specification:
        stream_enabled = stream_specification.get("StreamEnabled")
        stream_view_type = stream_specification.get("StreamViewType")

    # If present, use the view type to enable DDB streams in CFN
    if stream_enabled and stream_view_type:
        return {"StreamViewType": stream_view_type}
    else:
        return None
