import requests
from flask import Flask, jsonify, request,Response,app
from db_controller import get_items
import db_controller
from json_controller import insert_newstreet, get_streetsanddistricts, delete_streetsanddistricts, insert_newIssue, \
    get_issuesandpriorities
from flask_cors import CORS, cross_origin
from flask_dynamo import Dynamo
import json
import boto3
import logging
import jwt
from operator import itemgetter
from botocore.exceptions import ClientError

from register import register, get_user, encode_auth_token
from flask import send_from_directory
app = Flask(__name__)
logging.basicConfig(filename='Application.log', level=logging.DEBUG)
app.config['SECRET_KEY'] = 'super-secret'
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

@app.route('/get-profile', methods=['POST'])
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
        if (temp_email['S'] == Email):
          temp_password = Items['Password']
          if (temp_password['S'] == Password):
              user = {
                  '_id': 'My App ID',
                  'Email': Email,
                  'FirstName': Items['FirstName'],
                  'LastName': Items['LastName']
              }

              # create JWToken
              jwtoken = encode_auth_token(user)
              response = requests.get('http://httpbin.org/get', jwtoken)
              return response.json()

@app.route('/registration/', methods=['POST', 'GET'])
def register():
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


@app.errorhandler(Exception)
def basic_error(e):
    # fetch some info about the user from the request object
    user_ip = request.remote_addr
    requested_path = request.path

    print("User with IP %s tried to access endpoint: %s" % (user_ip, requested_path))
    return "An error occurred: " + str(e)


if __name__ == '__main__':
    app.debug = True
    app.run( host="127.0.0.1", port=5000)

