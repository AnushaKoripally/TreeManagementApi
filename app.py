from datetime import datetime
import uuid
from flask import Flask, jsonify, request
import db_controller
import json
from s3_controller import download_file
from json_controller import insert_newstreet, get_streetsanddistricts, delete_streetsanddistricts, insert_newIssue, \
    get_issuesandpriorities
from flask_cors import CORS
from fastapi import FastAPI
from fastapi import Request
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
