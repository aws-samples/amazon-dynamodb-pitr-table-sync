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

import unittest
from botocore.stub import Stubber
import boto3
from src.table_sync import auto_scaling_settings


def test_build_dynamodb_auto_scaling():
    dynamodb_client = boto3.client("dynamodb", "us-east-1")
    dynamodb_stubber = Stubber(dynamodb_client)
    dynamodb_stubber.add_response(
        "describe_table",
        {
            "Table": {
                "GlobalSecondaryIndexes": [
                    {
                        "IndexName": "salary-department-index",
                        "KeySchema": [
                            {"AttributeName": "salary", "KeyType": "HASH"},
                            {"AttributeName": "department", "KeyType": "RANGE"},
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                        "IndexStatus": "ACTIVE",
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 1,
                            "WriteCapacityUnits": 1,
                        },
                        "IndexSizeBytes": 0,
                        "ItemCount": 0,
                        "IndexArn": "arn:aws:dynamodb:us-east-1:123456789012:table/target-table/index/salary"
                        "-department-index",
                    }
                ],
            },
        },
        {"TableName": "target-table"},
    )
    dynamodb_stubber.add_response(
        "describe_table",
        {
            "Table": {
                "GlobalSecondaryIndexes": [
                    {
                        "IndexName": "salary-department-index",
                        "KeySchema": [
                            {"AttributeName": "salary", "KeyType": "HASH"},
                            {"AttributeName": "department", "KeyType": "RANGE"},
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                        "IndexStatus": "ACTIVE",
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 1,
                            "WriteCapacityUnits": 1,
                        },
                        "IndexSizeBytes": 0,
                        "ItemCount": 0,
                        "IndexArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/index/salary"
                        "-department-index",
                    }
                ],
            },
        },
        {"TableName": "source-table"},
    )
    dynamodb_stubber.activate()
    auto_scaling_client = boto3.client("application-autoscaling", "us-east-1")
    auto_scaling_stubber = Stubber(auto_scaling_client)
    auto_scaling_stubber.add_response(
        "describe_scalable_targets",
        {
            "ScalableTargets": [
                {
                    "ServiceNamespace": "dynamodb",
                    "ResourceId": "table/source-table",
                    "ScalableDimension": "dynamodb:table:ReadCapacityUnits",
                    "MinCapacity": 1,
                    "MaxCapacity": 2,
                    "RoleARN": "arn:aws:iam::123456789012:role/aws-service-role/dynamodb.application-autoscaling"
                    ".amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable",
                    "CreationTime": "2022-07-25T10:08:27.719000-04:00",
                    "SuspendedState": {
                        "DynamicScalingInSuspended": False,
                        "DynamicScalingOutSuspended": False,
                        "ScheduledScalingSuspended": False,
                    },
                },
                {
                    "ServiceNamespace": "dynamodb",
                    "ResourceId": "table/source-table",
                    "ScalableDimension": "dynamodb:table:WriteCapacityUnits",
                    "MinCapacity": 1,
                    "MaxCapacity": 2,
                    "RoleARN": "arn:aws:iam::123456789012:role/aws-service-role/dynamodb.application-autoscaling"
                    ".amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable",
                    "CreationTime": "2022-07-25T10:08:30.583000-04:00",
                    "SuspendedState": {
                        "DynamicScalingInSuspended": False,
                        "DynamicScalingOutSuspended": False,
                        "ScheduledScalingSuspended": False,
                    },
                },
            ]
        },
        {"ServiceNamespace": "dynamodb", "ResourceIds": ["table/source-table"]},
    )
    auto_scaling_stubber.add_response(
        "describe_scalable_targets",
        {
            "ScalableTargets": [
                {
                    "ServiceNamespace": "dynamodb",
                    "ResourceId": "table/source-table/index/salary-department-index",
                    "ScalableDimension": "dynamodb:index:ReadCapacityUnits",
                    "MinCapacity": 1,
                    "MaxCapacity": 2,
                    "RoleARN": "arn:aws:iam::123456789012:role/aws-service-role/dynamodb.application-autoscaling"
                    ".amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable",
                    "CreationTime": "2022-08-12T15:29:08.111000-04:00",
                    "SuspendedState": {
                        "DynamicScalingInSuspended": False,
                        "DynamicScalingOutSuspended": False,
                        "ScheduledScalingSuspended": False,
                    },
                },
                {
                    "ServiceNamespace": "dynamodb",
                    "ResourceId": "table/source-table/index/salary-department-index",
                    "ScalableDimension": "dynamodb:index:WriteCapacityUnits",
                    "MinCapacity": 1,
                    "MaxCapacity": 2,
                    "RoleARN": "arn:aws:iam::123456789012:role/aws-service-role/dynamodb.application-autoscaling"
                    ".amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable",
                    "CreationTime": "2022-08-12T15:29:08.859000-04:00",
                    "SuspendedState": {
                        "DynamicScalingInSuspended": False,
                        "DynamicScalingOutSuspended": False,
                        "ScheduledScalingSuspended": False,
                    },
                },
            ]
        },
        {
            "ServiceNamespace": "dynamodb",
            "ResourceIds": ["table/source-table/index/salary-department-index"],
        },
    )
    auto_scaling_stubber.add_response(
        "describe_scaling_policies",
        {
            "ScalingPolicies": [
                {
                    "PolicyARN": "arn:aws:autoscaling:us-east-1:123456789012:scalingPolicy:5d46fa9c-2003-4e37"
                    "-a1d0-51b2def2cb87:resource/dynamodb/table/source-table:policyName/$source"
                    "-table-scaling-policy",
                    "PolicyName": "$source-table-scaling-policy",
                    "ServiceNamespace": "dynamodb",
                    "ResourceId": "table/source-table",
                    "ScalableDimension": "dynamodb:table:ReadCapacityUnits",
                    "PolicyType": "TargetTrackingScaling",
                    "TargetTrackingScalingPolicyConfiguration": {
                        "TargetValue": 70.0,
                        "PredefinedMetricSpecification": {
                            "PredefinedMetricType": "DynamoDBReadCapacityUtilization"
                        },
                    },
                    "Alarms": [
                        {
                            "AlarmName": "TargetTracking-table/source-table-AlarmHigh-d1997c14-9cc5-44c9-8916"
                            "-2101996017de",
                            "AlarmARN": "arn:aws:cloudwatch:us-east-1:123456789012:alarm:TargetTracking-table"
                            "/source-table-AlarmHigh-d1997c14-9cc5-44c9-8916-2101996017de",
                        },
                        {
                            "AlarmName": "TargetTracking-table/source-table-AlarmLow-3f8e4158-deb1-4071-802d"
                            "-d2ad1c1fb754",
                            "AlarmARN": "arn:aws:cloudwatch:us-east-1:123456789012:alarm:TargetTracking-table"
                            "/source-table-AlarmLow-3f8e4158-deb1-4071-802d-d2ad1c1fb754",
                        },
                        {
                            "AlarmName": "TargetTracking-table/source-table-ProvisionedCapacityHigh-01bec74e-6f73"
                            "-4c22-b0d4-afe3dd4f8f9d",
                            "AlarmARN": "arn:aws:cloudwatch:us-east-1:123456789012:alarm:TargetTracking-table"
                            "/source-table-ProvisionedCapacityHigh-01bec74e-6f73-4c22-b0d4-afe3dd4f8f9d",
                        },
                        {
                            "AlarmName": "TargetTracking-table/source-table-ProvisionedCapacityLow-0b7cf273-ad46"
                            "-4a00-b36b-a29e8606b972",
                            "AlarmARN": "arn:aws:cloudwatch:us-east-1:123456789012:alarm:TargetTracking-table"
                            "/source-table-ProvisionedCapacityLow-0b7cf273-ad46-4a00-b36b-a29e8606b972",
                        },
                    ],
                    "CreationTime": "2022-07-25T10:08:27.843000-04:00",
                }
            ]
        },
        {
            "ServiceNamespace": "dynamodb",
            "ResourceId": "table/source-table",
            "ScalableDimension": "dynamodb:table:ReadCapacityUnits",
        },
    )
    auto_scaling_stubber.add_response(
        "describe_scaling_policies",
        {
            "ScalingPolicies": [
                {
                    "PolicyARN": "arn:aws:autoscaling:us-east-1:123456789012:scalingPolicy:722b065b-a3cf-4834"
                    "-86c1-dfd4ed4c3b25:resource/dynamodb/table/source-table:policyName"
                    "/DynamoDBWriteCapacityUtilization:table/source-table",
                    "PolicyName": "DynamoDBWriteCapacityUtilization:table/source-table",
                    "ServiceNamespace": "dynamodb",
                    "ResourceId": "table/source-table",
                    "ScalableDimension": "dynamodb:table:WriteCapacityUnits",
                    "PolicyType": "TargetTrackingScaling",
                    "TargetTrackingScalingPolicyConfiguration": {
                        "TargetValue": 70.0,
                        "PredefinedMetricSpecification": {
                            "PredefinedMetricType": "DynamoDBWriteCapacityUtilization"
                        },
                    },
                    "Alarms": [
                        {
                            "AlarmName": "TargetTracking-table/source-table-AlarmHigh-89c3c36f-bf52-4ec1-9c9c"
                            "-19c370fda167",
                            "AlarmARN": "arn:aws:cloudwatch:us-east-1:123456789012:alarm:TargetTracking-table"
                            "/source-table-AlarmHigh-89c3c36f-bf52-4ec1-9c9c-19c370fda167",
                        },
                        {
                            "AlarmName": "TargetTracking-table/source-table-AlarmLow-abd2f099-ccea-4d03-ae75"
                            "-af8f03173205",
                            "AlarmARN": "arn:aws:cloudwatch:us-east-1:123456789012:alarm:TargetTracking-table"
                            "/source-table-AlarmLow-abd2f099-ccea-4d03-ae75-af8f03173205",
                        },
                        {
                            "AlarmName": "TargetTracking-table/source-table-ProvisionedCapacityHigh-383a284e-239c"
                            "-4977-8a1b-0841fb20e406",
                            "AlarmARN": "arn:aws:cloudwatch:us-east-1:123456789012:alarm:TargetTracking-table"
                            "/source-table-ProvisionedCapacityHigh-383a284e-239c-4977-8a1b-0841fb20e406",
                        },
                        {
                            "AlarmName": "TargetTracking-table/source-table-ProvisionedCapacityLow-8dea331f-10f6"
                            "-449f-be23-366f5bec86e8",
                            "AlarmARN": "arn:aws:cloudwatch:us-east-1:123456789012:alarm:TargetTracking-table"
                            "/source-table-ProvisionedCapacityLow-8dea331f-10f6-449f-be23-366f5bec86e8",
                        },
                    ],
                    "CreationTime": "2022-07-25T10:08:30.613000-04:00",
                }
            ]
        },
        {
            "ServiceNamespace": "dynamodb",
            "ResourceId": "table/source-table",
            "ScalableDimension": "dynamodb:table:WriteCapacityUnits",
        },
    )
    auto_scaling_stubber.add_response(
        "describe_scaling_policies",
        {"ScalingPolicies": []},
        {
            "ServiceNamespace": "dynamodb",
            "ResourceId": "table/source-table/index/salary-department-index",
            "ScalableDimension": "dynamodb:index:ReadCapacityUnits",
        },
    )
    auto_scaling_stubber.add_response(
        "describe_scaling_policies",
        {"ScalingPolicies": []},
        {
            "ServiceNamespace": "dynamodb",
            "ResourceId": "table/source-table/index/salary-department-index",
            "ScalableDimension": "dynamodb:index:WriteCapacityUnits",
        },
    )
    auto_scaling_stubber.activate()
    expected_cfn_resources = {
        "targettableReadCapacityUnitsScalableTarget": {
            "Type": "AWS::ApplicationAutoScaling::ScalableTarget",
            "Properties": {
                "ServiceNamespace": "dynamodb",
                "ResourceId": "table/target-table",
                "ScalableDimension": "dynamodb:table:ReadCapacityUnits",
                "MinCapacity": 1,
                "MaxCapacity": 2,
                "RoleARN": "arn:aws:iam::123456789012:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable",
                "SuspendedState": {
                    "DynamicScalingInSuspended": False,
                    "DynamicScalingOutSuspended": False,
                    "ScheduledScalingSuspended": False,
                },
            },
        },
        "targettableWriteCapacityUnitsScalableTarget": {
            "Type": "AWS::ApplicationAutoScaling::ScalableTarget",
            "Properties": {
                "ServiceNamespace": "dynamodb",
                "ResourceId": "table/target-table",
                "ScalableDimension": "dynamodb:table:WriteCapacityUnits",
                "MinCapacity": 1,
                "MaxCapacity": 2,
                "RoleARN": "arn:aws:iam::123456789012:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable",
                "SuspendedState": {
                    "DynamicScalingInSuspended": False,
                    "DynamicScalingOutSuspended": False,
                    "ScheduledScalingSuspended": False,
                },
            },
        },
        "targettableReadCapacityUnitsScalingPolicy1": {
            "Type": "AWS::ApplicationAutoScaling::ScalingPolicy",
            "Properties": {
                "PolicyName": "$target-table-scaling-policy",
                "PolicyType": "TargetTrackingScaling",
                "TargetTrackingScalingPolicyConfiguration": {
                    "TargetValue": 70.0,
                    "PredefinedMetricSpecification": {
                        "PredefinedMetricType": "DynamoDBReadCapacityUtilization"
                    },
                },
                "ScalingTargetId": {
                    "Ref": "targettableReadCapacityUnitsScalableTarget"
                },
            },
        },
        "targettableWriteCapacityUnitsScalingPolicy1": {
            "Type": "AWS::ApplicationAutoScaling::ScalingPolicy",
            "Properties": {
                "PolicyName": "DynamoDBWriteCapacityUtilization:table/target-table",
                "PolicyType": "TargetTrackingScaling",
                "TargetTrackingScalingPolicyConfiguration": {
                    "TargetValue": 70.0,
                    "PredefinedMetricSpecification": {
                        "PredefinedMetricType": "DynamoDBWriteCapacityUtilization"
                    },
                },
                "ScalingTargetId": {
                    "Ref": "targettableWriteCapacityUnitsScalableTarget"
                },
            },
        },
        "salarydepartmentindexIndexReadCapacityUnitsScalableTarget": {
            "Type": "AWS::ApplicationAutoScaling::ScalableTarget",
            "Properties": {
                "ServiceNamespace": "dynamodb",
                "ResourceId": "table/target-table/index/salary-department-index",
                "ScalableDimension": "dynamodb:index:ReadCapacityUnits",
                "MinCapacity": 1,
                "MaxCapacity": 2,
                "RoleARN": "arn:aws:iam::123456789012:role/aws-service-role/dynamodb.application-autoscaling"
                ".amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable",
                "SuspendedState": {
                    "DynamicScalingInSuspended": False,
                    "DynamicScalingOutSuspended": False,
                    "ScheduledScalingSuspended": False,
                },
            },
        },
        "salarydepartmentindexIndexWriteCapacityUnitsScalableTarget": {
            "Type": "AWS::ApplicationAutoScaling::ScalableTarget",
            "Properties": {
                "ServiceNamespace": "dynamodb",
                "ResourceId": "table/target-table/index/salary-department-index",
                "ScalableDimension": "dynamodb:index:WriteCapacityUnits",
                "MinCapacity": 1,
                "MaxCapacity": 2,
                "RoleARN": "arn:aws:iam::123456789012:role/aws-service-role/dynamodb.application-autoscaling"
                ".amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable",
                "SuspendedState": {
                    "DynamicScalingInSuspended": False,
                    "DynamicScalingOutSuspended": False,
                    "ScheduledScalingSuspended": False,
                },
            },
        },
    }
    cfn_resources = auto_scaling_settings.build_dynamodb_auto_scaling(
        dynamodb_client=dynamodb_client,
        app_auto_scaling_client=auto_scaling_client,
        source_table_name="source-table",
        target_table_name="target-table",
        source_table={
            "Table": {
                "AttributeDefinitions": [
                    {"AttributeName": "department", "AttributeType": "S"},
                    {"AttributeName": "email", "AttributeType": "S"},
                    {"AttributeName": "phone_number", "AttributeType": "S"},
                    {"AttributeName": "salary", "AttributeType": "S"},
                ],
                "TableName": "source-table",
                "KeySchema": [
                    {"AttributeName": "email", "KeyType": "HASH"},
                    {"AttributeName": "phone_number", "KeyType": "RANGE"},
                ],
                "TableStatus": "ACTIVE",
                "CreationDateTime": "2020-10-15T20:21:09.725000-04:00",
                "ProvisionedThroughput": {
                    "NumberOfDecreasesToday": 0,
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1,
                },
                "TableSizeBytes": 79,
                "ItemCount": 1,
                "TableArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table",
                "TableId": "d98ecabe-02e3-45cc-8247-72c2ea152468",
                "BillingModeSummary": {
                    "BillingMode": "PROVISIONED",
                    "LastUpdateToPayPerRequestDateTime": "2022-07-23T20:42:06.471000-04:00",
                },
                "GlobalSecondaryIndexes": [
                    {
                        "IndexName": "salary-department-index",
                        "KeySchema": [
                            {"AttributeName": "salary", "KeyType": "HASH"},
                            {"AttributeName": "department", "KeyType": "RANGE"},
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                        "IndexStatus": "ACTIVE",
                        "ProvisionedThroughput": {
                            "NumberOfDecreasesToday": 0,
                            "ReadCapacityUnits": 1,
                            "WriteCapacityUnits": 1,
                        },
                        "IndexSizeBytes": 0,
                        "ItemCount": 0,
                        "IndexArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/index/salary-department-index",
                    }
                ],
                "StreamSpecification": {
                    "StreamEnabled": True,
                    "StreamViewType": "NEW_AND_OLD_IMAGES",
                },
                "LatestStreamLabel": "2022-05-13T19:00:22.332",
                "LatestStreamArn": "arn:aws:dynamodb:us-east-1:123456789012:table/source-table/stream/2022-05"
                "-13T19:00:22.332",
                "GlobalTableVersion": "2019.11.21",
                "Replicas": [{"RegionName": "ap-south-1", "ReplicaStatus": "ACTIVE"}],
            }
        },
    )
    assert cfn_resources.__eq__(expected_cfn_resources)


if __name__ == "__main__":
    unittest.main()
