import os
from os.path import join, dirname, realpath

import boto3
import logging
import sys
import random

from boto.gs import acl
from boto.s3.connection import S3Connection
from boto3.dynamodb.conditions import Key
from flask import jsonify
from werkzeug.utils import secure_filename

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


def insert_newevents(houseNumber, streetName, District, Issue, Priority, UtilityConflict, Notes, createdDate,
                     modifiedDate, assignee, user, status):
    eventId: str = 'TS' + ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])

    photos = []
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
        # send email to adminsif Priority = 1

        # if Priority == "1":
        #     admin_users = get_admin_users()
        #     print(admin_users)
        #     for u in admin_users:
        #         send_html_email(u, eventId, houseNumber, streetName, District, Issue, Notes)
        return eventId
    except Exception as e:
        logging.debug(e.response['Error']['Message'])
        error = 'Error while inserting record'
        print(error)
        print(e)
        response = {'Message': error}
        return jsonify(response)


def update_neweventimages(eventId, images):
    photos: any
    UPLOADS_PATH = join(dirname(realpath(__file__)), 'UPLOAD_FOLDER')
    #s3_client = boto3.client('s3')

    if (len(images) > 0):
     try:
        for p in images:
           try:
              file_path = os.path.join(UPLOADS_PATH, p.filename)  # path where file can be saved
              p.save(file_path)
              s3_response = upload_file(file_path, BUCKET, p.filename, eventId)
              s3_response = True
              response ="Success"
           except ClientError as e:
              logging.error(e)
              response = e
        return response
     except ClientError as e:
        logging.debug(e.response['Error']['Message'])
        error = 'Error while updating record'
        response = {'Message': error}
        return jsonify(response)
     finally:
         os.remove(file_path)


def update_newevents(Notes, status, eventId, createdDate):
    try:
        # table = dynamo_client.Table('Events')
        response = dynamo_client.update_item(
            TableName='Events',
            Key={
                'EventId': {'S': eventId},
                'CreatedDate': {'S': createdDate}
            },
            UpdateExpression="set #ts=:status, Notes=:Notes",

            ExpressionAttributeValues={
                ':status': {'S': status},
                ':Notes': {'S': Notes}
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


def get_admin_users():
    admin_users = []
    print(admin_users)
    try:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        table = dynamodb.Table('Users')
        response = table.query(
            # Add the name of the index
            IndexName="Roles",
            KeyConditionExpression=Key('UserRole').eq('Admin'),
        )

        print("The query returned the following items:")
        for item in response['Items']:
            admin_users.append(item['Email'])

        return admin_users
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


def verify_email_identity(email):
    ses_client = boto3.client("ses")
    response = ses_client.verify_email_identity(
        EmailAddress=email
    )
    print(email)
    print(response)


def send_html_email(adminUser, eventId, houseNumber, street, district, priority, Notes):
    ses_client = boto3.client("ses")
    CHARSET = "UTF-8"
    HTML_EMAIL_CONTENT = """
        <html>
            <head>
              <style>
               #heading { color: #FF0000; }
              </style></head>
            <h1 style='text-align:center' id=heading>Tree Management : P1 event """ + eventId + """ created. Requires immediate attention!!</h1>
            <p><strong>
            <br>Issue: """ + priority + """
            <br>House Number: """ + houseNumber + """
            <br>Street: """ + street + """
            <br>District: """ + district + """  
            <br>Notes: """ + Notes + """
            </strong>          
            </p>
            </body>
        </html>
    """
    try:
        response = ses_client.send_email(
            Destination={
                "ToAddresses": [
                    adminUser
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": HTML_EMAIL_CONTENT,
                    }
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": "Priority 1 event created",
                },
            },
            Source="testccsu@gmail.com",
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
