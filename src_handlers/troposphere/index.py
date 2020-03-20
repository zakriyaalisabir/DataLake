# pylint: skip-file
'''
This module create CloudFormation stack template for s3 bucket
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('...')))
import inspect
from src_handlers.handlers import index
from troposphere.constants import NUMBER
from troposphere.glue import (Crawler, Classifier, CsvClassifier,
                              XMLClassifier, JsonClassifier)
from troposphere.s3 import (Bucket, PublicReadWrite,
                            BucketPolicy, s3_bucket_name)
from troposphere.serverless import S3Event, Function
from troposphere import (Output, Ref, Template, GetAtt, Parameter,
                         Join)
from config import (BUCKETS, BUCKET_CORS_CONFIG,
                    BUCKET_NAME_SUFFIX, BUCKET_VERSIONING_CONFIG)
from troposphere.iam import Role, Policy
from troposphere.awslambda import Code, MEMORY_VALUES
import troposphere.awslambda as tropo_lambda


T = Template()

T.add_version('2010-09-09')
T.add_transform('AWS::Serverless-2016-10-31')

T.set_description(
    "AWS CloudFormation Template that create three s3 buckets \
    1)Landing Zone. 2)Work Zone. 3)Gold Zone. Landing Zone is \
    the place where the raw data is entered in the datalake \
    while the Work Zone ist the place where a partially \
    transformed or filtered data is stored and the Gold Zone \
    is the place where the final processesed or transformed data\
    will be placed after passing through ETL pipeline.")

MemorySize = T.add_parameter(Parameter(
    'LambdaMemorySize',
    Type=NUMBER,
    Description='Amount of memory to allocate to the Lambda Function',
    Default='128',
))

Timeout = T.add_parameter(Parameter(
    'LambdaTimeout',
    Type=NUMBER,
    Description='Timeout in seconds for the Lambda function',
    Default='60'
))

T.add_resource(Role(
    "LambdaExecutionRole",
    RoleName="LambdaExecutionRole".lower(),
    Path="/",
    Policies=[Policy(
        PolicyName="root",
        PolicyDocument={
            "Version": "2012-10-17",
            "Statement": [{
                "Action": ["logs:*"],
                "Resource": "arn:aws:logs:*:*:*",
                "Effect": "Allow"
            }, {
                "Action": ["lambda:*"],
                "Resource": "*",
                "Effect": "Allow"
            }]
        })],
    AssumeRolePolicyDocument={
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": ["sts:AssumeRole"],
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                        "lambda.amazonaws.com"
                    ]
                }
            }
        ]},
))

# T.add_resource(Crawler(
#     'RawDataCrawler',))


for bucket, dataType in BUCKETS:
    S3_BUCKET = T.add_resource(Bucket(
        bucket+BUCKET_NAME_SUFFIX,
        BucketName=s3_bucket_name(str(bucket+BUCKET_NAME_SUFFIX).lower()),
        CorsConfiguration=BUCKET_CORS_CONFIG,
        VersioningConfiguration=BUCKET_VERSIONING_CONFIG,
        AccessControl=PublicReadWrite,
        # Uncomment below line to add accelerated write
        # AccelerateConfiguration=BUCKET_ACCELERATION_CONFIG
    ))

    if bucket is BUCKETS[0][0]:
        pass
        T.add_resource(Function(
            'S3CreateEventTrigger',
            FunctionName='S3CreateEventTrigger'.lower(),
            Handler='index.createEventTrigger',
            Runtime='python3.7',
            MemorySize=Ref(MemorySize),
            Role=GetAtt("LambdaExecutionRole", "Arn"),
            # Code=Code(
            #     ZipFile=inspect.getsource(index)
            # ),
            InlineCode=inspect.getsource(index),
            Timeout=Ref(Timeout),
            Events={
                'S3ObjectCreateEvent': S3Event(
                    'S3ObjectCreateEvent',
                    Bucket=Ref(S3_BUCKET),
                    Events=['s3:ObjectCreated:*']
                )
            }))

# Prints the cf template file to console
print(T.to_json())

# Finally, write the template to a yaml file
with open('src_handlers/temp/cf_stack.yaml', 'w') as f:
    f.write(T.to_yaml())
