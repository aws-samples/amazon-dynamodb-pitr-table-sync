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

from model.aws.dynamodb.dynamodb_pitr_notification import DynamoDBPitrNotificationDetail
from typing import List, Optional
from pydantic import BaseModel, Field, create_model
import json


class EventBridgeEvent(BaseModel):
    version: str
    id: str
    detail_type: str = Field(None, alias="detail-type")
    source: str
    account: str
    time: str
    region: str
    resources: List[str]
    detail: DynamoDBPitrNotificationDetail


class SQSMessage(BaseModel):
    message_id: str = Field(None, alias="messageId")
    receipt_handle: str = Field(None, alias="receiptHandle")
    body: EventBridgeEvent
    attributes: create_model(
        "SQSAttributes",
        approximate_receive_count=(int, Field(None, alias="ApproximateReceiveCount")),
        sent_timestamp=(str, Field(None, alias="SentTimestamp")),
        sender_id=(str, Field(None, alias="SenderId")),
        approximate_first_receive_timestamp=(
            str,
            Field(None, alias="ApproximateFirstReceiveTimestamp"),
        ),
    )
    message_attributes: Optional[
        create_model(
            "SQSMessageAttributes",
            sqs_dlq_replay_nb=(
                create_model(
                    "SQSDLQReplayNbMessageAttribute",
                    string_value=(str, Field(None, alias="stringValue")),
                    string_list_values=(List, Field(None, alias="stringListValues")),
                    binary_list_values=(List, Field(None, alias="binaryListValues")),
                    data_type=(str, Field(None, alias="dataType")),
                ),
                Field(None, alias="sqs-dlq-replay-nb"),
            ),
        )
    ] = Field(None, alias="messageAttributes")
    md5_of_body: str = Field(None, alias="md5OfBody")
    event_source: str = Field(None, alias="EventSource")
    event_source_arn: str = Field(None, alias="eventSourceARN")
    aws_region: str = Field(None, alias="awsRegion")

    def __init__(self, **kwargs):
        kwargs["body"] = json.loads(kwargs["body"])
        super().__init__(**kwargs)


class AWSEvent(BaseModel):
    records: List[SQSMessage] = Field(None, alias="Records")
