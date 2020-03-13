'''
This module create CloudFormation stack template for s3 bucket
'''

from troposphere import Output, Ref, Template
from troposphere.s3 import Bucket, PublicRead


T = Template()

T.set_description(
    "AWS CloudFormation Sample Template S3_Bucket: Sample template showing "
    "how to create a publicly accessible S3 bucket. "
    "**WARNING** This template creates an Amazon S3 Bucket. "
    "You will be billed for the AWS resources used if you create "
    "a stack from this template.")

S3_BUCKET = T.add_resource(Bucket("S3Bucket", AccessControl=PublicRead,))

T.add_output(Output(
    "BucketName",
    Value=Ref(S3_BUCKET),
    Description="Name of S3 bucket to hold website content"
))

print(T.to_json())

# Finally, write the template to a file
with open('src/temp/cf_stack.yaml', 'w') as f:
    f.write(T.to_yaml())
