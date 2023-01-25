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

from pydantic import BaseModel, Field, create_model
from datetime import datetime
from typing import List, Optional


class UserIdentity(BaseModel):
    type: str
    principal_id: str = Field(None, alias="principalId")
    arn: str
    account_id: str = Field(None, alias="accountId")
    access_key_id: str = Field(None, alias="accessKeyId")
    session_context: create_model(
        "SessionContext",
        attributes=(
            create_model(
                "SessionContextAttributes",
                creation_date=(datetime, Field(None, alias="creationDate")),
                mfa_authenticated=(bool, Field(None, alias="mfaAuthenticated")),
            )
        ),
        session_issuer=create_model(
            "SessionIssuer",
            type=(str),
            principal_id=(str, Field(None, alias="principalId")),
            arn=(str),
            account_id=(str, Field(None, alias="accountId")),
            user_name=(str, Field(None, alias="userName")),
        ),
    ) = Field(None, alias="sessionContext")

class SecondaryIndexOverride(BaseModel):
    index_name: str = Field(None, alias="indexName")
    key_schema:  List[dict] = Field(None, alias="keySchema")
    projection: dict = Field(None, alias="projection")
    provisioned_throughput: Optional[dict] = Field(None, alias="provisionedThroughput")
    contributor_insights_specification: Optional[dict] = Field(None, alias="contributorInsightsSpecification")

    def to_dict(self):
        dictionary = {
            "IndexName": self.index_name,
            "KeySchema": self.key_schema,
            "Projection": self.projection,
            "ProvisionedThroughput": self.provisioned_throughput,
            "ContributorInsightsSpecification": self.contributor_insights_specification
        }
        print(f"This is the dict before anything: {dictionary}")
        for key in dictionary["KeySchema"]:
            key["AttributeName"] = key.pop("attributeName")
            key["KeyType"] = key.pop("keyType")

        if "nonKeyAttributes" in dictionary["Projection"].keys():
            dictionary["Projection"]["NonKeyAttributes"] = dictionary["Projection"].pop("nonKeyAttributes")
        if "projectionType" in dictionary["Projection"].keys():
            dictionary["Projection"]["ProjectionType"] = dictionary["Projection"].pop("projectionType")
        if 'provisioned_throughput' in self.__fields_set__:
            dictionary["ProvisionedThroughput"]["ReadCapacityUnits"] = int(dictionary["ProvisionedThroughput"].pop("readCapacityUnits"))
            dictionary["ProvisionedThroughput"]["WriteCapacityUnits"] = int(dictionary["ProvisionedThroughput"].pop("writeCapacityUnits"))
        if self.provisioned_throughput is None:
            del dictionary["ProvisionedThroughput"]
        if 'contributor_insights_specification' in self.__fields_set__ and self.contributor_insights_specification is not None:
            if "enabled" in dictionary["ContributorInsightsSpecification"].keys():
                dictionary["ContributorInsightsSpecification"]["Enabled"] = dictionary["ContributorInsightsSpecification"].pop("enabled")
        if self.contributor_insights_specification is None:
            del dictionary["ContributorInsightsSpecification"]
        return dictionary



class DynamoDBPitrRequestParameters(BaseModel):
    source_table_arn: Optional[str] = Field(None, alias="sourceTableArn")
    source_table_name: Optional[str] = Field(None, alias="sourceTableName")
    target_table_name: str = Field(None, alias="targetTableName")
    use_latest_restorable_time: bool = Field(None, alias="useLatestRestorableTime")
    global_secondary_index_override: List[SecondaryIndexOverride] = Field(
        None, alias="globalSecondaryIndexOverride"
    )
    local_secondary_index_override: List[SecondaryIndexOverride] = Field(
        None, alias="localSecondaryIndexOverride"
    )
    sse_specification_override: create_model(
        "SSESpecificationOverride", enabled=(bool, Field(None))
    ) = Field(None, alias="sSESpecificationOverride")


class DynamoDBPitrNotificationDetail(BaseModel):
    event_version: str = Field(None, alias="eventVersion")
    user_identity: UserIdentity = Field(None, alias="userIdentity")
    event_time: datetime = Field(None, alias="eventTime")
    event_source: str = Field(None, alias="eventSource")
    event_name: str = Field(None, alias="eventName")
    aws_region: str = Field(None, alias="awsRegion")
    source_ip_address: str = Field(None, alias="sourceIPAddress")
    user_agent: str = Field(None, alias="userAgent")
    request_parameters: DynamoDBPitrRequestParameters = Field(
        None, alias="requestParameters"
    )
    response_elements: str = Field(None, alias="responseElements")
    request_id: str = Field(None, alias="requestID")
    event_id: str = Field(None, alias="eventID")
    read_only: bool = Field(None, alias="readOnly")
    resources: List[
        create_model(
            "Resources",
            account_id=(str, Field(None, alias="account_id")),
            type=(str),
            arn=(str, Field(None, alias="ARN")),
        )
    ]
    event_type: str = Field(None, alias="eventType")
    api_version: str = Field(None, alias="apiVersion")
    management_event: bool = Field(None, alias="managementEvent")
    recipient_account_id: str = Field(None, alias="recipientAccountId")
    event_category: str = Field(None, alias="eventCategory")
    session_credential_from_console: bool = Field(
        None, alias="sessionCredentialFromConsole"
    )
