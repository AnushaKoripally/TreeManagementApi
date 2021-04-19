import boto3
import logging
import sys
import random
from s3_controller import list_files, upload_file, download_file
from botocore.exceptions import ClientError
from datetime import datetime
#from typing import Tuple, Any
sys.setrecursionlimit(10 ** 6)
BUCKET = "tm-photo-storage"
dynamo_client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")


def get_items():
    return dynamo_client.scan(
        TableName='Users'
    )


def insert_newevents(houseNumber, streetName, District, Issue, Priority, UtilityConflict, Notes, images, createdDate,
                     modifiedDate):
    eventId :str  = 'TS' + ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
    User: str = "Anusha"
    Status: str = "Created"
    photos = []

    photos = []
    logging.info('To insert new event')

    # if request contain photos
    if (images.length > 0):
        for p in images:
            s3_response = upload_file('C:\\Users\\Shobitha\\Desktop\\'+p, BUCKET, p ,eventId)
            s3_response = True
            if (s3_response):
                s3folder = {"S": eventId + '/' + p}
                photos.append(s3folder)
    else:
        photos = []
    print(photos)
    try:
        response = dynamo_client.put_item(
            TableName='Events',
            Item={
                'EventId': {'S': eventId},
                'CreatedDate': {'S': createdDate},
                'ModifiedDate': {'S': modifiedDate},
                'StreetName': {'S': streetName},
                'HouseNumber': {'S': houseNumber},
                'District': {'N': District},
                'User': {'S': User},
                'Issue': {'S': Issue},
                'UtilityConflict': {'BOOL': UtilityConflict},
                'Notes': {'S': Notes},
                'Status': {'S': Status},
                'Photos': {
                    'L': photos
                },
                'Priority': {'N': Priority},
            }
        )
        return '{} {} {}'.format(True, None, None)
    except Exception as e:
        logging.debug(e.response['Error']['Message'])
        error = 'Error while inserting record'
        print(error)
        print(e)
        return '{} {} {} {}'.format(False, None, error, e)


def get_event(id, cdate):
    try:
        response = dynamo_client.get_item(
            TableName='Events', Key={'EventId': {'S': id}, 'CreatedDate': {'N': cdate}})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']
