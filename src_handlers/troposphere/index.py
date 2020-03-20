# pylint: skip-file
'''
This module create CloudFormation stack template for s3 bucket
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('...')))
from troposphere.serverless import S3Event, Function
from config import (BUCKETS, BUCKET_CORS_CONFIG,
                    BUCKET_NAME_SUFFIX, BUCKET_VERSIONING_CONFIG)
from troposphere import Output, Ref, Template, GetAtt, Parameter
from awacs.s3 import ARN as S3_ARN
from awacs.aws import (Statement, Allow, Action, PolicyDocument,
                       Policy)
from troposphere.s3 import (Bucket, PublicReadWrite,
                            BucketPolicy, s3_bucket_name)
from troposphere.glue import (Crawler, Classifier, CsvClassifier,
                              XMLClassifier, JsonClassifier)
# from troposphere.awslambda import Function


T = Template()

T.set_description(
    "AWS CloudFormation Template that create three s3 buckets \
    1)Landing Zone. 2)Work Zone. 3)Gold Zone. Landing Zone is \
    the place where the raw data is entered in the datalake \
    while the Work Zone ist the place where a partially \
    transformed or filtered data is stored and the Gold Zone \
    is the place where the final processesed or transformed data\
    will be placed after passing through ETL pipeline.")


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
        T.add_resource(Function(
            'S3CreateEventTrigger',
            MemorySize=128,
            Timeout='60',
            Handler='index.createEventTrigger',
            Runtime='python3.7',
            CodeUri='s3://'+str(bucket+BUCKET_NAME_SUFFIX).lower()+'/cet.zip',
            Policies='AmazonS3ReadOnlyAccess',
            Events={
                'FileUpload': S3Event(
                    'FileUpload',
                    Bucket=Ref(S3_BUCKET),
                    Events=['s3:ObjectCreated:*']
                )}))

        # T.add_resource(Crawler(
        #     'RawDataCrawler',))

    T.add_output(Output(
        bucket,
        Value=Ref(S3_BUCKET),
        Description="{0} bucket to hold {1} content of datalake".format(
            bucket, dataType)
    ))

# Prints the cf template file to console
print(T.to_json())

# Finally, write the template to a yaml file
with open('src_handlers/temp/cf_stack.yaml', 'w') as f:
    f.write(T.to_yaml())
