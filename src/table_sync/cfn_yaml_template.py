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

def create_basic_cfn_yaml(cfn_template_description: str = "Basic CFN template"):
    """Builds the basic CFN template dict.

    Args:
      cfn_template_description: The template description.

    Returns:
      A dict for the CFN template

    Raises:
    """
    return {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": cfn_template_description,
        "Resources": {},
    }


def create_basic_dynamodb_cfn():
    """Builds the basic CFN template for a DynamoDB table resource.

    Args:

    Returns:

    Raises:
    """
    return {
        "Type": "AWS::DynamoDB::Table",
        "DeletionPolicy": "Retain",
        "Properties": {},
    }


def create_basic_event_source_mapping_cfn():
    """Builds the basic CFN template for an event source mapping resource.

    Args:

    Returns:

    Raises:
    """
    return {"Type": "AWS::Lambda::EventSourceMapping", "Properties": {}}


def create_basic_scalable_target_cfn():
    """Builds the basic CFN template for a scalable target resource.

    Args:

    Returns:

    Raises:
    """
    return {
        "Type": "AWS::ApplicationAutoScaling::ScalableTarget",
        "Properties": {},
    }


def create_basic_scaling_policy_cfn():
    """Builds the basic CFN template for a scaling policy that will be attached to a scalable target.

    Args:

    Returns:

    Raises:
    """
    return {"Type": "AWS::ApplicationAutoScaling::ScalingPolicy", "Properties": {}}
