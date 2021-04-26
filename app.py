from datetime import datetime
import uuid

import boto3
import requests
from flask import Flask, jsonify,  request
import db_controller
import json
from s3_controller import download_file
from json_controller import insert_newstreet, get_streetsanddistricts, delete_streetsanddistricts, insert_newIssue, \
    get_issuesandpriorities
from flask_cors import CORS
from fastapi import FastAPI
from fastapi import Request

from datetime import datetime, timedelta, time
import jwt
#from register import register, get_user, encode_auth_token
from register import register, get_user
from botocore.exceptions import ClientError

import logging
BUCKET = "tm-photo-storage"
app = Flask(__name__)
#logging.basicConfig(filename='./Application.log', level=logging.DEBUG)
CORS(app)


@app.route('/')
def index():
    return "This is the main page."


@app.route('/get-items')
def get_items():
    return jsonify(db_controller.get_items())


@app.route('/insert-newstreet', methods=['GET', 'POST'])
def insert_newstreets():
    return insert_newstreet("1", "AbC")


@app.route('/get-streetsanddistricts', methods=['GET'])
def get_streets():
    return get_streetsanddistricts()


@app.route('/delete-street', methods=['GET', 'POST'])
def delete_street():
    return delete_streetsanddistricts("1", "AbC")


@app.route('/insert-issue', methods=['GET', 'POST'])
def insert_issue():
    return insert_newIssue("4", "Widowmaker")


@app.route('/get-issueandpriority', methods=['GET'])
def get_issueandpriority():
    return get_issuesandpriorities()


@app.route('/insert-newevent', methods=['GET', 'POST'])
def insert_newevent():
    post = json.loads(request.data)
    houseNumber = post.get('houseNumber')
    street = post.get('street')[0]
    distict = str(post.get('district'))
    utilityConflict = post.get('utilityConflict')
    issue = post.get('issue')[0]
    priority = str(post.get('priority'))
    notes = post.get('notes')
    eventimages = post.get('eventimages')
    createdDate = post.get('createdDate')
    modifiedDate = post.get('modifiedDate')
    return jsonify( db_controller.insert_newevents(houseNumber, street, distict, issue, priority,utilityConflict, notes, eventimages,createdDate,modifiedDate))

@app.route('/download', methods=['GET'])
def downloadS3File():
    post = json.loads(request.data)
    eventId = post.get('eventId')
    return download_file(eventId, BUCKET)

@app.route('/get-event', methods=['GET'])
def get_event():
    return jsonify(db_controller.get_event('tm0k001', '03302021'))


@app.route('/get-profile', methods=['POST', 'GET'])
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

@app.route('/get-user', methods=['POST', 'GET'])
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
              #response = requests.get('http://httpbin.org/get', jwtoken)

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

@app.route('/registration/', methods=['POST', 'GET'])
def register():
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
                    response = {'Message':'Success'}
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

@app.route('/update-user/', methods=['POST', 'GET'])
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

@app.errorhandler(Exception)
def basic_error(e):
    # fetch some info about the user from the request object
    user_ip = request.remote_addr
    requested_path = request.path

    print("User with IP %s tried to access endpoint: %s" % (user_ip, requested_path))
    return "An error occurred: " + str(e)


if __name__ == '__main__':
    # host =
    app.run("127.0.0.1", port=5000)
