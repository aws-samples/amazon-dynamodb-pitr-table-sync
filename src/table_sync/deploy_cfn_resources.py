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

import json
import botocore
from aws_lambda_powertools import Logger
from table_sync.config import CFN_IMPORT_CHANGE_SET_TYPE, CFN_UPDATE_CHANGE_SET_TYPE

LOG: Logger = Logger(service=__name__)


def create_and_execute_change_set(
    cfn_client: object,
    cfn_stack_name: str,
    cfn_change_set_name: str = "",
    cfn_template_dict=None,
    cfn_change_set_type: str = "",
    cfn_resources_to_import=None,
):
    """Creates and executes a change set for a given CFN stack.

    Args:
        cfn_client: Authenticated CloudFormation boto3 client.
        cfn_change_set_name: The name of the change set.
        cfn_template_dict: The updated CFN template for the change set.
        cfn_change_set_type: The type of change set. Can be UPDATE or IMPORT.
        cfn_resources_to_import: If the type of the change set is IMPORT, then a list of resources to be imported.
        cfn_stack_name: The name of the CloudFormation stack.

    Returns:

    Raises:
      ClientError: Boto3 error
    """
    LOG.info(
        f"Change set type: {cfn_change_set_type}\n"
        f"Change set name: {cfn_change_set_name}\n"
        f"Change set template: {cfn_template_dict}\n"
        f"Change set resource import (if applicable): {cfn_resources_to_import}"
    )
    if cfn_resources_to_import is None:
        cfn_resources_to_import = []
    if cfn_template_dict is None:
        cfn_template_dict = {}
    change_set_type_waiter_dict = {
        CFN_IMPORT_CHANGE_SET_TYPE: "stack_import_complete",
        CFN_UPDATE_CHANGE_SET_TYPE: "stack_update_complete",
    }

    # Create a CFN change set.
    try:
        create_change_set_params = {
            "StackName": cfn_stack_name,
            "TemplateBody": json.dumps(cfn_template_dict),
            "ChangeSetName": cfn_change_set_name,
            "Description": "Change set to update the PITR restored DynamoDB table",
            "ChangeSetType": cfn_change_set_type,
        }
        if cfn_resources_to_import:
            create_change_set_params.update(ResourcesToImport=cfn_resources_to_import)
        import_change_set_response = cfn_client.create_change_set(**create_change_set_params)
        import_change_set_arn = import_change_set_response.get("Id")

        # Wait for the change set to be in the CREATE_COMPLETE state.
        LOG.info(f"Change set creation successful. Waiting for change set to be in CREATE_COMPLETE state.")
        waiter = cfn_client.get_waiter("change_set_create_complete")
        waiter.wait(
            ChangeSetName=import_change_set_arn,
            StackName=cfn_stack_name,
            WaiterConfig={"Delay": 6, "MaxAttempts": 10},  # 1 minute wait.
        )

        # Execute the change set.
        cfn_client.execute_change_set(
            ChangeSetName=import_change_set_arn,
            StackName=cfn_stack_name,
        )

        # Wait for the stack to be in the IMPORT_COMPLETE / UPDATE_COMPLETE state.
        LOG.info(f"Change set execution successful. Waiting for stack in the UPDATE / IMPORT COMPLETE state.")
        waiter = cfn_client.get_waiter(change_set_type_waiter_dict.get(cfn_change_set_type))
        waiter.wait(StackName=cfn_stack_name, WaiterConfig={"Delay": 6, "MaxAttempts": 30})  # 3 minute wait.
    except botocore.exceptions.ClientError as error:
        raise error
    except Exception as error:
        raise error
