import uuid
from typing import Tuple, Any

import boto3
import logging
import sys
import random

from botocore.exceptions import ClientError
from datetime import datetime

sys.setrecursionlimit(10 ** 6)

dynamo_client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")


def get_items():
    return dynamo_client.scan(
        TableName='Users'
    )


def insert_newevent1():
    return dynamo_client.scan(
        TableName='Events'
    )


def insert_newevents(houseNumber, streetName, District, Issue, Priority, UtilityConflict, Notes, images, createdDate,
                     modifiedDate):
    eventId :str  = 'TS' + ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
    # eventId = uuid.uuid4()
    User: str = "Anusha"
    Status: str = "Created"

    logging.info('To insert new event')
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
                'Priority': {'N': Priority},
            }
        )
        return '{} {} {}'.format(True, None, None)
    except ClientError as e:
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
