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

import traceback
from model.aws.dynamodb.aws_event import AWSEvent
import boto3
import botocore.exceptions
from table_sync.cfn_yaml_template import (
    create_basic_cfn_yaml,
    create_basic_dynamodb_cfn,
)
from aws_lambda_powertools import Logger, Tracer
from table_sync.time_to_live_settings import build_dynamodb_ttl
from table_sync.kinesis_stream_settings import build_kinesis_stream_template
from table_sync.pitr_settings import build_point_in_time_recovery_template
from table_sync.dynamodb_stream_settings import (
    build_dynamodb_stream_triggers,
    build_dynamodb_stream_template,
)
from table_sync.auto_scaling_settings import build_dynamodb_auto_scaling
from table_sync.helpers import is_dynamodb_table_available, parse_arn
from table_sync.config import (
    LOG_LEVEL,
    CFN_IMPORT_CHANGE_SET_TYPE,
    CFN_UPDATE_CHANGE_SET_TYPE,
    REGION,
    PARTITION,
    ACCOUNT_ID,
    ENABLE_DYNAMODB_STREAM_SETTINGS,
    ENABLE_TTL_SETTINGS,
    ENABLE_PITR_SETTINGS,
    ENABLE_KINESIS_SETTINGS,
    ENABLE_AUTO_SCALING_SETTINGS,
    ENABLE_TAG_SETTINGS,
    ENABLE_DYNAMODB_LAMBDA_TRIGGERS
)
from table_sync.deploy_cfn_resources import create_and_execute_change_set

LOG: Logger = Logger(service=__name__)
LOG.setLevel(LOG_LEVEL)
TRACER: Tracer = Tracer(service=__name__)
CFN = boto3.client("cloudformation")
DDB = boto3.client("dynamodb")
LAMBDA = boto3.client("lambda")
APP_AUTO_SCALING = boto3.client("application-autoscaling")


@TRACER.capture_lambda_handler
def lambda_handler(event, context):
    """Lambda function to have the restored dynamodb table configuration synced with the source table

    Args
    event: dict, required
        DynamoDB Point In Time Recovery API Call via CloudTrail event Details

        Event doc: https://docs.aws.amazon.com/eventbridge/latest/userguide/event-types.html

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
        bool: True

    Raises:
        ClientError: Boto3 client error.
        TableNotActive: Error indicating DynamoDB table not in ACTIVE state.
    """
    # Log event
    # Deserialize event
    # Retrieve the detail from the event.
    # Log the retry attempt for this particular event.
    LOG.info(f"Event: {event}")
    aws_event = AWSEvent(**event)
    aws_event_detail = aws_event.records[0].body.detail
    if "sqs_dlq_replay_nb" in aws_event.records[0].message_attributes.__fields_set__:
        LOG.info(
            f"Message retry attempt #: {aws_event.records[0].message_attributes.sqs_dlq_replay_nb.string_value}"
        )

    # Retrieve the restored table name.
    # Retrieve the source table name.
    # Create the stack name.
    # Log the table names and CFN stack name.
    target_table_name = aws_event_detail.request_parameters.target_table_name
    source_table_name: str
    if "source_table_name" in aws_event_detail.request_parameters.__fields_set__:
        source_table_name = aws_event_detail.request_parameters.source_table_name
    else:
        source_table_arn = aws_event_detail.request_parameters.source_table_arn
        source_table_name = parse_arn(source_table_arn).resource.split("/")[1]
    cfn_stack_name = f"Restored-DynamoDB-Table-{target_table_name}-Stack"
    LOG.info(f"Source table name: {source_table_name}")
    LOG.info(f"Target table name: {target_table_name}")
    LOG.info(f"CFN stack name: {cfn_stack_name}")

    # Check if the target table is in ACTIVE state.
    # If not active, raise error to send the event to the SQS' DLQ.
    try:
        if not is_dynamodb_table_available(
            dynamodb_client=DDB, target_table_name=target_table_name
        ):
            raise TableNotActive
    except botocore.exceptions.ClientError as error:
        LOG.error(f"AWS Error: {error}")
        raise
    except TableNotActive:
        LOG.error(
            f"{target_table_name} not yet in ACTIVE status. Raising error and sending back to SQS DLQ."
        )
        raise
    except Exception as error:
        LOG.error(f"Unexpected error: {error}")
        raise

    # Get information about the source DynamoDB table.
    # Load the basic CFN yaml template.
    # Update the basic YAML template with a DynamoDB table.
    # Add the table name to the yaml.
    # Add the key schema to the yaml.
    # Remove the non-key attributes from the AttributeDefinitions
    # Add the attributes to the yaml.
    # Add the billing mode to the yaml.
    source_table = DDB.describe_table(TableName=source_table_name)
    template_dict = create_basic_cfn_yaml(
        cfn_template_description=f"{target_table_name} Cloudformation deployment"
    )
    template_dict.get("Resources").update(PITRRestoredTable=create_basic_dynamodb_cfn())
    dynamodb_table_properties = (
        template_dict.get("Resources").get("PITRRestoredTable").get("Properties")
    )
    dynamodb_table_properties["TableName"] = target_table_name
    dynamodb_table_properties["KeySchema"] = source_table.get("Table").get("KeySchema")
    key_attribute_names: [str] = []
    for key in source_table.get("Table").get("KeySchema"):
        key_attribute_names.append(key.get("AttributeName"))
    target_table_attribute_definitions = source_table.get("Table").get(
        "AttributeDefinitions"
    )
    for i, attribute in enumerate(target_table_attribute_definitions):
        if attribute.get("AttributeName") not in key_attribute_names:
            target_table_attribute_definitions.pop(i)
    dynamodb_table_properties[
        "AttributeDefinitions"
    ] = target_table_attribute_definitions
    billing_mode_summary = source_table.get("Table").get("BillingModeSummary", None)
    if billing_mode_summary and billing_mode_summary.get("BillingMode", "") == "PAY_PER_REQUEST":
        dynamodb_table_properties["BillingMode"] = "PAY_PER_REQUEST"
    else:
        dynamodb_table_properties["ProvisionedThroughput"] = {
            "ReadCapacityUnits": source_table.get("Table")
            .get("ProvisionedThroughput")
            .get("ReadCapacityUnits"),
            "WriteCapacityUnits": source_table.get("Table")
            .get("ProvisionedThroughput")
            .get("WriteCapacityUnits"),
        }
    try:
        # Bare minimum template to import the DynamoDB table is now ready.
        # Create and execute the change set.
        create_and_execute_change_set(
            cfn_client=CFN,
            cfn_stack_name=cfn_stack_name,
            cfn_change_set_name=f"Import-DynamoDB-{target_table_name}-Change-Set",
            cfn_template_dict=template_dict,
            cfn_change_set_type=CFN_IMPORT_CHANGE_SET_TYPE,
            cfn_resources_to_import=[
                {
                    "ResourceType": "AWS::DynamoDB::Table",
                    "LogicalResourceId": "PITRRestoredTable",
                    "ResourceIdentifier": {"TableName": target_table_name},
                }
            ],
        )

        # Check if the tag settings need to be copied.
        # Get the tags for the source table.
        # Update the template with the tag list.
        # Define the change set name.
        # Create and execute the CFN change set.
        LOG.info(f"Is tag setting enabled : {ENABLE_TAG_SETTINGS}")
        if ENABLE_TAG_SETTINGS:
            response = DDB.list_tags_of_resource(
                ResourceArn=f"arn:{PARTITION}:dynamodb:{REGION}:{ACCOUNT_ID}:table/{source_table_name}",
            )
            if response.get("Tags", None):
                if len(response.get("Tags")) > 0:
                    dynamodb_table_properties["Tags"] = []
                    for tag in response.get("Tags"):
                        dynamodb_table_properties["Tags"].append(tag)
                    create_and_execute_change_set(
                        cfn_client=CFN,
                        cfn_stack_name=cfn_stack_name,
                        cfn_change_set_type=CFN_UPDATE_CHANGE_SET_TYPE,
                        cfn_change_set_name=f"Update-DynamoDB-{target_table_name}-Tags-Change-Set",
                        cfn_template_dict=template_dict,
                    )

        # Check if the DynamoDB table stream settings need to be copied.
        # Update the DynamoDB table stream settings.
        # Create and execute the change set.
        LOG.info(f"Is DynamoDB stream setting enabled : {ENABLE_DYNAMODB_STREAM_SETTINGS}")
        if ENABLE_DYNAMODB_STREAM_SETTINGS:
            dynamodb_table_stream_settings = build_dynamodb_stream_template(
                source_table_describe_response=source_table
            )
            if dynamodb_table_stream_settings:
                dynamodb_table_properties[
                    "StreamSpecification"
                ] = dynamodb_table_stream_settings
                create_and_execute_change_set(
                    cfn_client=CFN,
                    cfn_stack_name=cfn_stack_name,
                    cfn_change_set_type=CFN_UPDATE_CHANGE_SET_TYPE,
                    cfn_change_set_name=f"Update-DynamoDB-{target_table_name}-Stream-Change-Set",
                    cfn_template_dict=template_dict,
                )

        # Check if the DynamoDB Table AWS Lambda triggers need to be copied.
        # Update the CFN template with the event source mapping resources for the target DynamoDB table.
        # Create and execute the change set.
        LOG.info(f"Is DynamoDB AWS Lambda trigger setting enabled : {ENABLE_DYNAMODB_LAMBDA_TRIGGERS}")
        if ENABLE_DYNAMODB_LAMBDA_TRIGGERS:
            dynamodb_table_stream_trigger_resources = build_dynamodb_stream_triggers(
                lambda_client=LAMBDA,
                source_table_describe_response=source_table,
                restored_table_cfn_logical_name="PITRRestoredTable",
            )
            cfn_resources = template_dict.get("Resources")
            if dynamodb_table_stream_trigger_resources:
                cfn_resources.update(dynamodb_table_stream_trigger_resources)
                create_and_execute_change_set(
                    cfn_client=CFN,
                    cfn_stack_name=cfn_stack_name,
                    cfn_change_set_name=f"Update-DynamoDB-{target_table_name}-Triggers-Change-Set",
                    cfn_change_set_type=CFN_UPDATE_CHANGE_SET_TYPE,
                    cfn_template_dict=template_dict,
                )

        # Check if the Kinesis stream settings need to be copied.
        # Update the Kinesis stream settings for the target table.
        # Create and execute the change set.
        LOG.info(f"Is Kinesis stream setting enabled : {ENABLE_KINESIS_SETTINGS}")
        if ENABLE_KINESIS_SETTINGS:
            dynamodb_table_kinesis_stream_settings = build_kinesis_stream_template(
                dynamodb_client=DDB, source_table_name=source_table_name
            )
            if dynamodb_table_kinesis_stream_settings:
                dynamodb_table_properties.update(
                    KinesisStreamSpecification=dynamodb_table_kinesis_stream_settings
                )
                create_and_execute_change_set(
                    cfn_client=CFN,
                    cfn_stack_name=cfn_stack_name,
                    cfn_change_set_type=CFN_UPDATE_CHANGE_SET_TYPE,
                    cfn_change_set_name=f"Update-DynamoDB-{target_table_name}-Kinesis-Settings-Change-Set",
                    cfn_template_dict=template_dict,
                )

        # Check if the PITR settings need to be copied.
        # Update the PITR settings for the target table.
        # Create and execute the change set.
        LOG.info(f"Is PITR setting enabled : {ENABLE_PITR_SETTINGS}")
        if ENABLE_PITR_SETTINGS:
            dynamodb_table_pitr_settings = build_point_in_time_recovery_template(
                dynamodb_client=DDB, source_table_name=source_table_name
            )
            if dynamodb_table_pitr_settings:
                dynamodb_table_properties.update(
                    PointInTimeRecoverySpecification=dynamodb_table_pitr_settings
                )
                create_and_execute_change_set(
                    cfn_client=CFN,
                    cfn_stack_name=cfn_stack_name,
                    cfn_change_set_type=CFN_UPDATE_CHANGE_SET_TYPE,
                    cfn_change_set_name=f"Update-DynamoDB-{target_table_name}-PITR-Settings-Change-Set",
                    cfn_template_dict=template_dict,
                )

        # Check if the TTL settings need to be copied.
        # Update the TTL settings for the target table.
        # Create and execute the change set.
        LOG.info(f"Is TTL setting enabled : {ENABLE_TTL_SETTINGS}")
        if ENABLE_TTL_SETTINGS:
            dynamodb_table_ttl_settings = build_dynamodb_ttl(
                dynamodb_client=DDB, source_table_name=source_table_name
            )
            if dynamodb_table_ttl_settings:
                dynamodb_table_properties.update(
                    TimeToLiveSpecification=dynamodb_table_ttl_settings
                )
                create_and_execute_change_set(
                    cfn_client=CFN,
                    cfn_stack_name=cfn_stack_name,
                    cfn_change_set_name=f"Update-DynamoDB-{target_table_name}-TTL-Settings-Change-Set",
                    cfn_change_set_type=CFN_UPDATE_CHANGE_SET_TYPE,
                    cfn_template_dict=template_dict,
                )

        # Check if the autoscaling settings need to be copied.
        # Update the Scaling Targets and the Scaling Policies on the DynamoDB target table.
        # Create and execute the change set.
        LOG.info(f"Is auto scaling setting enabled : {ENABLE_AUTO_SCALING_SETTINGS}")
        if ENABLE_AUTO_SCALING_SETTINGS:
            dynamodb_scalable_targets = build_dynamodb_auto_scaling(
                dynamodb_client=DDB,
                app_auto_scaling_client=APP_AUTO_SCALING,
                source_table_name=source_table_name,
                source_table=source_table,
                target_table_name=target_table_name,
            )
            LOG.info(f"Scalable targets CFN resources: {dynamodb_scalable_targets}")
            if dynamodb_scalable_targets:
                cfn_resources = template_dict.get("Resources")
                cfn_resources.update(dynamodb_scalable_targets)
                create_and_execute_change_set(
                    cfn_client=CFN,
                    cfn_stack_name=cfn_stack_name,
                    cfn_change_set_type=CFN_UPDATE_CHANGE_SET_TYPE,
                    cfn_template_dict=template_dict,
                    cfn_change_set_name=f"Update-DynamoDB-{target_table_name}-Scalable-Targets-Settings-Change-Set",
                )
    except botocore.exceptions.ClientError as error:
        LOG.error(f"AWS error: {error}")
        raise
    except Exception as error:
        LOG.error(f"Unexpected error: {error}")
        traceback.print_exc()
        raise

    # All done, return.
    return True


class TableNotActive(Exception):
    pass
