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
from table_sync.cfn_yaml_template import create_basic_scaling_policy_cfn, create_basic_scalable_target_cfn

LOG: Logger = Logger(service=__name__)


def build_dynamodb_auto_scaling(
    dynamodb_client: object,
    app_auto_scaling_client: object,
    source_table_name: str,
    target_table_name: str,
    source_table: dict,
):
    """Build CFN template for the auto scaling policies to apply to the target table

    Args:
        dynamodb_client: Authenticated DynamoDB boto3 client.
        app_auto_scaling_client: Authenticated Application Autoscaling boto3 client.
        source_table_name: The name of the source DynamoDB table.
        target_table_name: The name of the target DynamoDB table.
        source_table: The describe table API response for the source DynamoDB table.

    Returns:

    Raises:
    """
    # CFN Resources
    resources = {}

    # Get the global secondary indexes for the target DynamoDB table.
    response = dynamodb_client.describe_table(TableName=target_table_name)
    target_table_gsi: [dict] = response.get("Table").get("GlobalSecondaryIndexes")
    target_table_gsi_names: [str] = []
    if target_table_gsi:
        for gsi in target_table_gsi:
            target_table_gsi_names.append(gsi.get("IndexName"))

    # Get the global secondary indexes for the source DynamoDB table.
    source_table_gsi = source_table.get("Table").get("GlobalSecondaryIndexes")
    source_table_gsi_names: [str] = []
    if source_table_gsi:
        for gsi in source_table_gsi:
            source_table_gsi_names.append(gsi.get("IndexName"))

    # Get the common indexes between the two tables. It is likely that some indexes weren't restored on the
    # target table. In that case, we would want to place scaling policy on the indexes that overlap.
    common_index_names = set(source_table_gsi_names).intersection(target_table_gsi_names)
    LOG.info(f"Common GSIs between the source and the target tables: {common_index_names}")

    # Check if the DynamoDB table is a scaling target.
    # If not, return. If yes, retrieve the scaling policies for the target.
    # Get the scaling policies associated with the source table.
    source_table_scalable_targets_response = app_auto_scaling_client.describe_scalable_targets(
        ServiceNamespace="dynamodb",
        ResourceIds=[
            f"table/{source_table_name}",
        ],
    )
    LOG.info(f"Source table scalable targets: {source_table_scalable_targets_response}")
    source_table_scalable_targets: dict = {}
    for target in source_table_scalable_targets_response.get("ScalableTargets", []):
        if target.get("ScalableDimension") == "dynamodb:table:WriteCapacityUnits":
            source_table_scalable_targets.update({target.get("ScalableDimension"): target})
        if target.get("ScalableDimension") == "dynamodb:table:ReadCapacityUnits":
            source_table_scalable_targets.update({target.get("ScalableDimension"): target})

    # Get all the scalable targets for common indexes.
    common_index_scalable_targets = {}
    if common_index_names:
        for index_name in common_index_names:
            response = app_auto_scaling_client.describe_scalable_targets(
                ServiceNamespace="dynamodb",
                ResourceIds=[f"table/{source_table_name}/index/{index_name}"],
            )
            index_scalable_target: dict = {}
            for target in response.get("ScalableTargets", []):
                if target.get("ScalableDimension") == "dynamodb:index:ReadCapacityUnits":
                    index_scalable_target.update({target.get("ScalableDimension"): target})
                if target.get("ScalableDimension") == "dynamodb:index:WriteCapacityUnits":
                    index_scalable_target.update({target.get("ScalableDimension"): target})
            if index_scalable_target:
                common_index_scalable_targets.update({index_name: index_scalable_target})

    LOG.info(f"Common index names scalable targets: {common_index_scalable_targets}")

    # Return if no scalable targets for the table or the common indexes.
    if not source_table_scalable_targets and not common_index_scalable_targets:
        return None

    # Build CFN for the table scalable targets that have been discovered till now.
    for key, value in source_table_scalable_targets.items():
        scalable_target_cfn = create_basic_scalable_target_cfn()
        scalable_target_cfn_properties = scalable_target_cfn.get("Properties")

        # Remove creation date as it is not required in CFN.
        del value["CreationTime"]

        # Add scalable dimension as it is required in CFN.
        value.update(ScalableDimension=key)

        # Replace the table name in the resourceId.
        value.update(ResourceId=value.get("ResourceId").replace(source_table_name, target_table_name))

        # Update the CFN properties.
        scalable_target_cfn_properties.update(value)
        resources.update(
            {
                f"{target_table_name.replace('_','').replace('.','').replace('-','')}"
                f"{key.split(':')[2]}ScalableTarget": scalable_target_cfn
            }
        )

    # Build CFN for the table common indexes scalable targets that have been discovered till now.
    for index_name, index_targets in common_index_scalable_targets.items():
        for scalable_dimension, target_object in index_targets.items():
            scalable_target_cfn = create_basic_scalable_target_cfn()
            scalable_target_cfn_properties = scalable_target_cfn.get("Properties")

            # Remove creation date as it is not required in CFN.
            del target_object["CreationTime"]

            # Add scalable dimension as it is required in CFN.
            target_object.update(ScalableDimension=scalable_dimension)

            # Replace the table name in the resourceId.
            target_object.update(
                ResourceId=target_object.get("ResourceId").replace(source_table_name, target_table_name)
            )

            # Update the CFN properties.
            scalable_target_cfn_properties.update(target_object)
            resources.update(
                {
                    f"{index_name.replace('_','').replace('.','').replace('-','')}"
                    f"Index{scalable_dimension.split(':')[2]}ScalableTarget": scalable_target_cfn
                }
            )

    # Use describe scaling policies API to get the policies and then create CFN for the same.
    source_table_scaling_policies: dict = {}
    for dimension, scaling_target in source_table_scalable_targets.items():
        response = app_auto_scaling_client.describe_scaling_policies(
            ServiceNamespace="dynamodb",
            ResourceId=f"table/{source_table_name}",
            ScalableDimension=dimension,
        )
        source_table_scaling_policies.update({dimension: response.get("ScalingPolicies", [])})
    LOG.info(f"Source table scaling policies: {source_table_scaling_policies}")

    # Build CFN for all the scaling policies on the table read and write capacity.
    for dimension, scaling_policies in source_table_scaling_policies.items():
        for i, policy in enumerate(scaling_policies):
            scaling_policy_cfn = create_basic_scaling_policy_cfn()
            scaling_policy_cfn_properties = scaling_policy_cfn.get("Properties")
            scaling_policy_cfn_properties.update(policy)

            # Remove policy ARN.
            # Remove creation time.
            # Remove alarms.
            # Remove ResourceId.
            # Remove ScalableDimension.
            # Remove ServiceNamespace.
            del scaling_policy_cfn_properties["PolicyARN"]
            del scaling_policy_cfn_properties["CreationTime"]
            del scaling_policy_cfn_properties["Alarms"]
            del scaling_policy_cfn_properties["ResourceId"]
            del scaling_policy_cfn_properties["ScalableDimension"]
            del scaling_policy_cfn_properties["ServiceNamespace"]

            # Update policy name if it contains any references to the source table name.
            scaling_policy_cfn_properties.update(
                PolicyName=scaling_policy_cfn_properties.get("PolicyName").replace(source_table_name, target_table_name)
            )

            # Update the ScalableTargetId property with the CFN logical id of the scalable target.
            scaling_policy_cfn_properties.update(
                ScalingTargetId={
                    "Ref": f"{target_table_name.replace('_','').replace('.','').replace('-','')}"
                    f"{dimension.split(':')[2]}ScalableTarget"
                }
            )

            resources.update(
                {
                    f"{target_table_name.replace('_', '').replace('.', '').replace('-', '')}"
                    f"{dimension.split(':')[2]}ScalingPolicy{i+1}": scaling_policy_cfn
                }
            )

    # Use describe scaling policies API to et the policies.
    common_index_scaling_policies: dict = {}
    for index_name, index_targets in common_index_scalable_targets.items():
        index_policies: dict = {}
        for dimension, target in index_targets.items():
            response = app_auto_scaling_client.describe_scaling_policies(
                ServiceNamespace="dynamodb",
                ResourceId=f"table/{source_table_name}/index/{index_name}",
                ScalableDimension=dimension,
            )
            index_policies.update({dimension: response.get("ScalingPolicies", [])})
        common_index_scaling_policies.update({index_name: index_policies})
    LOG.info(f"Common indexes scaling policies: {common_index_scaling_policies}")

    # Build CFN for all the scaling policies on the table index's read and write capacity.
    for index, scaling_dimension in common_index_scaling_policies.items():
        for dimension, policies in scaling_dimension.items():
            for i, policy in enumerate(policies):
                scaling_policy_cfn = create_basic_scaling_policy_cfn()
                scaling_policy_cfn_properties = scaling_policy_cfn.get("Properties")
                scaling_policy_cfn_properties.update(policy)

                # Remove policy ARN.
                # Remove creation time.
                # Remove alarms.
                # Remove ResourceId.
                # Remove ScalableDimension.
                # Remove ServiceNamespace.
                del scaling_policy_cfn_properties["PolicyARN"]
                del scaling_policy_cfn_properties["CreationTime"]
                del scaling_policy_cfn_properties["Alarms"]
                del scaling_policy_cfn_properties["ResourceId"]
                del scaling_policy_cfn_properties["ScalableDimension"]
                del scaling_policy_cfn_properties["ServiceNamespace"]

                # Update policy name if it contains any references to the source table name.
                scaling_policy_cfn_properties.update(
                    PolicyName=scaling_policy_cfn_properties.get("PolicyName").replace(
                        source_table_name, target_table_name
                    )
                )

                # Update the ScalableTargetId property with the CFN logical id of the scalable target.
                scaling_policy_cfn_properties.update(
                    ScalingTargetId={
                        "Ref": f"{index.replace('_', '').replace('.', '').replace('-', '')}"
                        f"Index{dimension.split(':')[2]}ScalableTarget"
                    }
                )

                resources.update(
                    {
                        f"{index.replace('_', '').replace('.', '').replace('-', '')}"
                        f"Index{dimension.split(':')[2]}ScalingPolicy{i + 1}": scaling_policy_cfn
                    }
                )

    return resources
