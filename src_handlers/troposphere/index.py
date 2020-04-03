# pylint: disable=W,C,R
'''
This module create CloudFormation stack template for s3 bucket
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('...')))
import json
import inspect
from src_handlers.handlers import index, post_crawler
from troposphere.constants import NUMBER
from troposphere.glue import (Crawler, Classifier, CsvClassifier,
                              XMLClassifier, JsonClassifier,
                              SchemaChangePolicy, Database, Table,
                              CatalogTarget, Targets, Database,
                              S3Target)
from troposphere.s3 import (Bucket, PublicReadWrite,
                            BucketPolicy, s3_bucket_name)
from troposphere.serverless import S3Event, Function
from troposphere import (Output, Ref, Template, GetAtt, Parameter,
                         Join)
from config import (BUCKETS, BUCKET_CORS_CONFIG,
                    BUCKET_NAME_SUFFIX, BUCKET_VERSIONING_CONFIG)
from troposphere.iam import Role, Policy
from troposphere.awslambda import Code, MEMORY_VALUES
from troposphere.events import Rule, Target
import troposphere.awslambda as tropo_lambda


CRAWLER_DB_NAME = 'RawDataCrawlerDB'.lower()
CRAWLER_TABLES_NAME_PREFIX = 'MockDatalakeTable_'.lower()
CRAWLER_NAME = 'RawDataCrawler'.lower()


T = Template()

T.set_version('2010-09-09')
T.set_transform('AWS::Serverless-2016-10-31')

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
                "Action": ["lambda:*", "glue:*", "s3:*"],
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
                        "lambda.amazonaws.com",
                        "glue.amazonaws.com"
                    ]
                }
            }
        ]},
))


for bucket, dataType in BUCKETS:
    S3_BUCKET = T.add_resource(Bucket(
        bucket+BUCKET_NAME_SUFFIX,
        BucketName=s3_bucket_name(str(bucket+BUCKET_NAME_SUFFIX).lower()),
        AccessControl=PublicReadWrite,
        CorsConfiguration=BUCKET_CORS_CONFIG,
        VersioningConfiguration=BUCKET_VERSIONING_CONFIG,
        # Uncomment below line to add accelerated write
        # AccelerateConfiguration=BUCKET_ACCELERATION_CONFIG
    ))

    if bucket is BUCKETS[0][0]:
        T.add_resource(Function(
            'S3CreateEventTrigger',
            FunctionName='S3CreateEventTrigger'.lower(),
            Handler='index.createEventTrigger',
            Runtime='python3.7',
            MemorySize=Ref(MemorySize),
            Role=GetAtt("LambdaExecutionRole", "Arn"),
            InlineCode=inspect.getsource(index),
            Timeout=Ref(Timeout),
            Events={
                'S3ObjectCreateEvent': S3Event(
                    'S3ObjectCreateEvent',
                    Bucket=Ref(S3_BUCKET),
                    Events=['s3:ObjectCreated:*']
                )
            })
        )

        T.add_resource(
            Crawler(
                CRAWLER_NAME,
                Name=CRAWLER_NAME,
                Role=GetAtt("LambdaExecutionRole", "Arn"),
                DatabaseName=CRAWLER_DB_NAME,
                TablePrefix=CRAWLER_TABLES_NAME_PREFIX,
                SchemaChangePolicy=SchemaChangePolicy(
                    UpdateBehavior="UPDATE_IN_DATABASE",
                    DeleteBehavior="LOG"
                ),
                Configuration=json.dumps({
                    "Version": 1.0,
                    "CrawlerOutput": {
                        "Partitions": {
                            "AddOrUpdateBehavior": "InheritFromTable"
                        },
                        "Tables": {
                            "AddOrUpdateBehavior": "MergeNewColumns"
                        }
                    }
                }),
                Targets=Targets(
                    'MyS3Targets',
                    S3Targets=[
                        S3Target(
                            'MyS3RawDataTarget',
                            Path='s3://' +
                            (bucket+BUCKET_NAME_SUFFIX).lower()+'/json/file.json'
                        ),
                        S3Target(
                            'MyS3RawDataTarget',
                            Path='s3://' +
                            (bucket+BUCKET_NAME_SUFFIX).lower()+'/csv/file.csv'
                        ),
                        S3Target(
                            'MyS3RawDataTarget',
                            Path='s3://' +
                            (bucket+BUCKET_NAME_SUFFIX).lower()+'/xml/file.xml'
                        )
                    ]
                )
            )
        )

    if bucket is BUCKETS[1][0]:
        PostCrawlerFnForGlueJob = T.add_resource(
            Function(
                'PostCrawlerFnForGlueJob',
                FunctionName='PostCrawlerFnForGlueJob'.lower(),
                Handler='index.initiateGlueJob',
                Runtime='python3.7',
                MemorySize=Ref(MemorySize),
                Role=GetAtt("LambdaExecutionRole", "Arn"),
                InlineCode=inspect.getsource(post_crawler),
                Timeout=Ref(Timeout),
            )
        )

        Rule = T.add_resource(Rule(
            'PostCrawlerRuleForETL',
            Name='PostCrawlerRuleForETL'.lower(),
            EventPattern={
                "source": ["aws.glue"],
                "detail-type": ["Glue Crawler State Change"],
                "detail": {
                    "state": [
                        "Succeeded"
                    ]
                }
            },
            Description="Post Crawler Rule for CloudWatch Event",
            State="ENABLED",
            Targets=[
                Target(
                    "PostCrawlerTarget",
                    Arn= GetAtt("PostCrawlerFnForGlueJob", "Arn"),
                    Id= "PostCrawlerTargetFunction1"
                )
            ]
        ))


# Prints the cf template file to console
print(T.to_json())

# Finally, write the template to a yaml file
with open('src_handlers/temp/cf_stack.yaml', 'w') as f:
    f.write(T.to_yaml())
