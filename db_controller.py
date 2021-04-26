import boto3
import logging
import sys
import random

from flask import jsonify

from s3_controller import list_files, upload_file, download_file
from botocore.exceptions import ClientError
from datetime import datetime

# from typing import Tuple, Any
sys.setrecursionlimit(10 ** 6)
BUCKET = "tm-photo-storage"
dynamo_client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")


def get_items():
    return dynamo_client.scan(
        TableName='Users'
    )


def insert_newevents(houseNumber, streetName, District, Issue, Priority, UtilityConflict, Notes, images, createdDate,
                     modifiedDate, assignee, user, status):
    eventId: str = 'TS' + ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

    photos = []
    logging.info('To insert new event')

    # # if request contain photos
    # if (images.length > 0):
    #     for p in images:
    #         s3_response = upload_file('C:\\Users\\Shobitha\\Desktop\\' + p, BUCKET, p, eventId)
    #         s3_response = True
    #         if (s3_response):
    #             s3folder = {"S": eventId + '/' + p}
    #             photos.append(s3folder)
    # else:
    #     photos = []
    # print(photos)
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
                'User': {'S': user},
                'Issue': {'S': Issue},
                'UtilityConflict': {'BOOL': UtilityConflict},
                'Notes': {'S': Notes},
                'Status': {'S': status},
                'Photos': {
                    'L': photos
                },
                'Priority': {'N': Priority},
                'Assignee': {'S': assignee}
            }
        )
        return '{} {} {}'.format(True, None, None)
    except Exception as e:
        logging.debug(e.response['Error']['Message'])
        error = 'Error while inserting record'
        print(error)
        print(e)
        return '{} {} {} {}'.format(False, None, error, e)


def update_newevents(Notes, status,eventId,createdDate):
    try:
                    #table = dynamo_client.Table('Events')
                    response = dynamo_client.update_item(
                    TableName='Events',
                    Key={
                        'EventId' :{'S': eventId },
                         'CreatedDate' : {'S': createdDate }
                    },
                    UpdateExpression = "set #ts=:status, Notes=:Notes",

                    ExpressionAttributeValues = {
                        ':status': {'S' :status},
                        ':Notes' : {'S' :Notes}
                        },
                    ExpressionAttributeNames={
                            "#ts": "Status"
                    },
                    ReturnValues="UPDATED_NEW",
                    )
                    return response
    except ClientError as e:
                    logging.debug(e.response['Error']['Message'])
                    error = 'Error while updating record'
                    response = {'Message': error}
                    return jsonify(response)



def get_event(id, cdate):
    try:
        response = dynamo_client.get_item(
            TableName='Events', Key={'EventId': {'S': id}, 'CreatedDate': {'N': cdate}})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


def get_allevents():
    try:
        response = dynamo_client.scan(TableName='Events')
        result = response['Items']
        idx = 0
        for item in result:
            for key in item:
                value = list(item[key].values())[0]
                result[idx][key] = value
            idx += 1
        while 'LastEvaluatedKey' in response:
            response = dynamo_client.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return result
