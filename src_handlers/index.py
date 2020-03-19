'''
This module create CloudFormation stack template for s3 bucket
'''
import os
import sys
from troposphere.s3 import Bucket, PublicReadWrite
from troposphere import Output, Ref, Template

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from config import (
    init,
    BUCKET_NAME_SUFFIX,
    BUCKETS,
    BUCKET_CORS_CONFIG,
    BUCKET_VERSIONING_CONFIG,
    BUCKET_ACCELERATION_CONFIG
)


init()

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
        AccessControl=PublicReadWrite,
        AccelerateConfiguration=BUCKET_ACCELERATION_CONFIG)
    )

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
