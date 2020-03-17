import os
import boto3

print(os.getenv('aws_secret_access_key'))

BUCKETS = [["LandingZone", "Raw"],
           ["WorkZone", "Partially Processed"],
           ["GoldZone", "Final Processed"]]

BUCKET_NAME_SUFFIX = 'DataLakeMockProjectPreBetaRelease'

CLIENT = boto3.client(
    service_name='s3', region_name=str(os.getenv('aws_region')),
    aws_access_key_id=str(os.getenv('aws_access_key_id')),
    aws_secret_access_key=str(os.getenv('aws_secret_access_key')))

bucketsList = CLIENT.list_buckets()

print(bucketsList)
