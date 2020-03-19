# pylint: skip-file
'''
This module create CloudFormation stack template for s3 bucket
'''
from troposphere.s3 import Bucket, Private, BucketPolicy
from troposphere.iam import Policy
from config import (BUCKETS,
                    BUCKET_CORS_CONFIG,
                    BUCKET_NAME_SUFFIX,
                    BUCKET_VERSIONING_CONFIG)
from troposphere import Output, Ref, Template
import awacs.
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath('...')))


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
        CorsConfiguration=BUCKET_CORS_CONFIG,
        VersioningConfiguration=BUCKET_VERSIONING_CONFIG,
        AccessControl=Private,
        # Uncomment below line to add accelerated write
        # AccelerateConfiguration=BUCKET_ACCELERATION_CONFIG

    ))

    T.add_resource(BucketPolicy(
        bucket+'Policy', 
        Bucket=Ref(S3_BUCKET), 
        PolicyDocument=Policy(
            Version='20-March-2020',
            Statement=[Statement()])
    ))

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
