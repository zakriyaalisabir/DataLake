from __future__ import print_function
import os
import json
import boto3


session = boto3.session.Session(
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key')
)

glue_client = boto3.client('glue', region_name=os.getenv('aws_region'))


def initiateGlueJob(event, context):
    # TODO : Start Glue Job below
    try:
        if event and 'detail' in event and event['detail'] and 'crawlerName' in event['detail']:
            c_name = event['detail']['crawlerName']
            print('Received crawler_name from event -{0}'.format(str(c_name)))

            crawler = glue_client.get_crawler(Name=c_name)
            print('Received crawler from glue - {0}'.format(str(crawler)))

            database = crawler['Crawler']['DatabaseName']
            print('Received db from crawler - {0}'.format(str(database)))

    except Exception as e:
        print('Error handling events from crawler. Details - {0}'.format(e))
        raise e
