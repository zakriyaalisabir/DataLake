'''
This module create CloudFormation stack template for s3 bucket
'''

from troposphere import Output, Ref, Template
from troposphere.s3 import Bucket, Private, VersioningConfiguration, AccelerateConfiguration


T = Template()

T.set_description(
    "AWS CloudFormation Template that create three s3 buckets 1)Landing Zone. 2)Work Zone\
    3)Gold Zone.Landing Zone is the place where the raw data is entered in the datalake \
    while the Work Zone ist the place where a partially transformed or filtered data is \
    stored and the Gold Zone is the place where the final processesed or transformed data\
    will be placed after passing through ETL pipeline.")

BUCKETS = [["LandingZone", "Raw"],
           ["WorkZone", "Partially Processed"],
           ["GoldZone", "Final Processed"]]

BUCKET_NAME_SUFFIX = 'DataLakeMockProjectPreBetaRelease'

for bucket, dataType in BUCKETS:
    S3_BUCKET = T.add_resource(Bucket
                               (
                                   bucket+BUCKET_NAME_SUFFIX,
                                   VersioningConfiguration=VersioningConfiguration(
                                       Status="Enabled"),
                                   AccessControl=Private,
                                   AccelerateConfiguration=AccelerateConfiguration(
                                       AccelerationStatus="Enabled")
                               )
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
with open('src/temp/cf_stack.yaml', 'w') as f:
    f.write(T.to_yaml())
