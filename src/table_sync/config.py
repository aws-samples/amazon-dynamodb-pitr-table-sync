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


#Environment configuration values used by lambda functions.
import os

CFN_IMPORT_CHANGE_SET_TYPE = "IMPORT"
CFN_UPDATE_CHANGE_SET_TYPE = "UPDATE"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
REGION = os.getenv("AWS_REGION")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
PARTITION = os.getenv("PARTITION")
ENABLE_TAG_SETTINGS = os.getenv("ENABLE_TAG_SETTINGS").lower() == "true"
ENABLE_KINESIS_SETTINGS = os.getenv("ENABLE_KINESIS_SETTINGS").lower() == "true"
ENABLE_DYNAMODB_STREAM_SETTINGS = os.getenv("ENABLE_DYNAMODB_STREAM_SETTINGS").lower() == "true"
ENABLE_TTL_SETTINGS = os.getenv("ENABLE_TTL_SETTINGS").lower() == "true"
ENABLE_PITR_SETTINGS = os.getenv("ENABLE_PITR_SETTINGS").lower() == "true"
ENABLE_AUTO_SCALING_SETTINGS = os.getenv("ENABLE_AUTO_SCALING_SETTINGS").lower() == "true"
ENABLE_DYNAMODB_LAMBDA_TRIGGERS = os.getenv("ENABLE_DYNAMODB_LAMBDA_TRIGGERS").lower() == "true"
