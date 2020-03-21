from __future__ import print_function
import os
import json
import boto3
# from django_server.settings import (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


session = boto3.session.Session(
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key')
)

s3 = session.resource('s3')
# glue = session.resource("glue")
glue_client = boto3.client('glue', region_name=os.getenv('aws_region'))


def ResponseBuilder(statusCode=200, body=None, headers=None):
    print(body)
    return json.dumps({
        "body": body, "statusCode": statusCode, "headers": headers
    })


def createEventTrigger(event, context):
    print("Triggered on create object, starting Crawler now")

    glue_client.start_crawler(Name='rawdatacrawler')
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # response = s3.head_object(Bucket=bucket, Key=key)

        print('response', bucket, key)

    body = {"message": "This is the updatad dummy message in a JSON object."}
    return ResponseBuilder(body=json.dumps(body))
