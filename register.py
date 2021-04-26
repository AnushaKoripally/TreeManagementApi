from datetime import datetime, timedelta
import boto3
import logging
import jwt
from botocore.exceptions import ClientError
import json
from flask import Response, request, jsonify, Flask, app
#from flask_dynamo import Dynamo
from operator import itemgetter
import requests
import boto3
from botocore.exceptions import ClientError
from db_controller import get_items
dynamo_client = boto3.client('dynamodb',endpoint_url = 'http://localhost:8000' )

def get_user():
        received_json_data = request.get_json()
        temp_data = json.dumps(received_json_data, indent=4)
        string_data = json.loads(temp_data)
        Email = string_data['email']
        Password = string_data['password']

        temp_json_data = get_items().get_json()
        temp_tab_data = json.dumps(temp_json_data, indent=4)
        user_data = json.loads(temp_tab_data)

        for Items in user_data['Items']:
            temp_email = Items['Email']
            try:
                if (temp_email['S'] == Email):
                    temp_password = Items['Password']
                    try:
                        if (temp_password['S'] == Password):
                            user = {
                                'Email': Email,
                                'FirstName': Items['FirstName']['S'],
                                'LastName': Items['LastName']['S'],
                                'UserRole': Items['UserRole']['S'],
                                'Username': Items['Username']['S'],
                                'Password': Items['Password']['S']
                            }

                            # create JWToken
                            #jwtoken = encode_auth_token(user)
                           # response = requests.get('http://httpbin.org/get', jwtoken)
                            #return response.json()
                            response = user
                            return jsonify(response)
                    except ClientError as e:
                        logging.debug(e.response['Error']['Message'])
                        error = 'Error Email and Password doesnot match.'
                        response = {'Message': error}
                        return jsonify(response)
            except ClientError as e:
                logging.debug(e.response['Error']['Message'])
                error = 'Error Email and Password doesnot match.'
                response = {'Message': error}
                return jsonify(response)


def register():
        entryFlag = 1;
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
            temp_email = Items['Email']
            if temp_username['S'] == Username:
                entryFlag = 0
                break
            elif temp_email['S'] == Email:
                entryFlag = 0
                break

        if entryFlag:
            dynamodb_client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")
            date = datetime.today().strftime('%Y-%m-%d')
            try:
                response = dynamodb_client.put_item(
                    TableName='Users',
                    Item={
                        'FirstName': {'S': FirstName},
                        'LastName': {'S': LastName},
                        'Email': {'S': Email},
                        'Username': {'S': Username},
                        'Password': {'S': Password},
                        'UserRole': {'S': Role},
                        'CreatedDate': {'S': date},
                        'ModifiedDate': {'S': date}
                    }
                )
                response = {'Message': 'Success'}
                return jsonify(response)
            except ClientError as e:
                logging.debug(e.response['Error']['Message'])
                error = 'Error while inserting record'
                response = {'Message': error}
                return jsonify(response)
        else:
            error = 'Email/Username already exists!'
            response = {'Message': error}
            return jsonify(response)


#def encode_auth_token(user):
#    """
#    Generates the Auth Token
#    :return: string
#    """
#    try:
#        payload = {
#            'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
#            'iat': datetime.utcnow(),
#            'sub': user
#
#        }
#
#        return jwt.encode(
#            payload,
#            key= 'SECRETE_KEY',
#
#            # app.config.get('SECRET_KEY'),
#            algorithm='HS256'
#        )
#    except Exception as e:
#        return e

def get_profile():
        received_json_data = request.data.decode('UTF-8')
        string_data = received_json_data
        Email = string_data
        temp_json_data = get_items().get_json()
        temp_tab_data = json.dumps(temp_json_data, indent=4)
        user_data = json.loads(temp_tab_data)
        for Items in user_data['Items']:
            temp_email = Items['Email']
            try:
                if (temp_email['S'] == Email):
                    user = {
                        'Email': Email,
                        'Password': Items['Password']['S'],
                        'FirstName': Items['FirstName']['S'],
                        'LastName': Items['LastName']['S'],
                        'UserRole': Items['UserRole']['S'],
                        'Username': Items['Username']['S']
                    }
                    response = json.dumps(user)
                    return response

            except ClientError as e:
                logging.debug(e.response['Error']['Message'])
                error = 'Error Email not found.'
                response = {'Message': error}
                return jsonify(response)

def update_user():
    entryFlag = 1;
    received_json_data=request.get_json()
    temp_data = json.dumps(received_json_data, indent=4)
    string_data = json.loads(temp_data)

    FirstName = string_data['FirstName']
    LastName = string_data['LastName']
    Email = string_data['Email']
    Username = string_data['Username']
    Password = string_data['Password']
    Role = string_data['UserRole']
    date = datetime.today().strftime('%Y-%m-%d')
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    try:
                    table = dynamodb.Table('Users')
                    response = table.update_item(
                    Key={
                        'Username': Username },
                    UpdateExpression = "set FirstName=:fn, LastName=:ln, Email=:em, Password=:pw, UserRole=:rl, ModifiedDate=:md",
                    ExpressionAttributeValues = {
                        ':fn': FirstName,
                        ':ln': LastName,
                        ':em': Email,
                        ':pw': Password,
                        ':rl': Role,
                        ':md': date
                        },
                    ReturnValues="UPDATED_NEW",
                    )
                    return response
    except ClientError as e:
                    logging.debug(e.response['Error']['Message'])
                    error = 'Error while updating record'
                    response = {'Message': error}
                    return jsonify(response)

