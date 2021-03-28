from flask import Flask, jsonify, request
import db_controller
from json_controller import insert_newstreet, get_streetsanddistricts, delete_streetsanddistricts, insert_newIssue, \
    get_issuesandpriorities
from flask_cors import CORS, cross_origin
import logging

app = Flask(__name__)
logging.basicConfig(filename='Application.log', level=logging.DEBUG)
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


@app.errorhandler(Exception)
def basic_error(e):
    # fetch some info about the user from the request object
    user_ip = request.remote_addr
    requested_path = request.path

    print("User with IP %s tried to access endpoint: %s" % (user_ip, requested_path))
    return "An error occurred: " + str(e)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
