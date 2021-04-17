from datetime import datetime, timedelta
import boto3
import logging
import jwt
from botocore.exceptions import ClientError
import json
from flask import Response, request, jsonify, Flask, app
from flask_dynamo import Dynamo
from operator import itemgetter
import requests
import boto3
from botocore.exceptions import ClientError
from application import app
from db_controller import get_items

dynamo_client = boto3.client('dynamodb',endpoint_url = 'http://localhost:8000' )

def get_user():
    received_json_data = request.get_json()
    temp_data = json.dumps(received_json_data, indent=4)
    string_data = json.loads(temp_data)
    Email = string_data['email']
    Password = string_data['password']

    temp_json_data = get_items().get_json()
    temp_tab_data = json.dumps(temp_json_data, indent= 4)
    user_data = json.loads(temp_tab_data)
    for Items in user_data['Items']:
        temp_email = Items['Email']
        if (temp_email['S'] == Email):
          temp_password = Items['Password']
          if (temp_password['S'] == Password):
              user = {
                  '_id': 'My App ID',
                  'Email': Email,
                  'FirstName': Items['FirstName'],
                  'LastName': Items['LastName']
              }

              import datetime
              # create JWToken
              jwtoken = encode_auth_token(user)
              response = requests.get('http://httpbin.org/get', jwtoken)
              return response.json()


def register():
    received_json_data = request.get_json()
    temp_data = json.dumps(received_json_data, indent=4)
    string_data = json.loads(temp_data)

    FirstName = string_data['FirstName']
    LastName = string_data['LastName']
    Email = string_data['Email']
    Username = string_data['Username']
    Password = string_data['Password']
    Role = string_data['UserRole']
    temp_json_data = get_items().get_json()
    temp_tab_data = json.dumps(temp_json_data, indent=4)
    user_data = json.loads(temp_tab_data)
    for Items in user_data['Items']:
        temp_username = Items['Username']
        if temp_username['S'] != Username:
            temp_email = Items['Email']
            if temp_email['S'] != Email:
                dynamodb_client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")
                try:
                    response = dynamodb_client.put_item(
                        TableName='Users',
                        Item={
                            'FirstName': {'S': FirstName},
                            'LastName': {'S': LastName},
                            'Email': {'S': Email},
                            'Username': {'S': Username},
                            'Password': {'S': Password},
                            'UserRole': {'S': Role}
                        }
                    )
                    return '{} {} {}'.format(True, None, None)
                except ClientError as e:
                    logging.debug(e.response['Error']['Message'])
                    error = 'Error while inserting record'
                    return '{} {} {} {}'.format(False, None, error, e)


def encode_auth_token(user):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
            'iat': datetime.utcnow(),
            'sub': user

        }

        return jwt.encode(
            payload,
            key= 'SECRETE_KEY',

            # app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def get_profile():
    received_json_data = request.data.decode('UTF-8')
    #temp_data = json.dumps(received_json_data, indent=4)
    #string_data = json.loads(temp_data)
    string_data = received_json_data
    Email = string_data
    temp_json_data = get_items().get_json()
    temp_tab_data = json.dumps(temp_json_data, indent=4)
    user_data = json.loads(temp_tab_data)
    for Items in user_data['Items']:
        temp_email = Items['Email']
        if (temp_email['S'] == Email):
            user = {
                'Email': Email,
                'FirstName': Items['FirstName'],
                'LastName': Items['LastName']
            }
            response = json.dumps(user)
            return response


