import json
import logging
import os


def insert_newstreet(key, value):
    try:
        with open(os.path.join(os.path.dirname(__file__), 'streetsAndDistricts.json'), 'r') as jsonFile:
            data = json.load(jsonFile)
            keys = data.keys()
            values = data.get(key)
            logging.info('Loaded Streets and Districts')
            if (key in keys) and (value not in values):
                data[key].append(value)
                with open(os.path.join(os.path.dirname(__file__), 'streetsAndDistricts.json'), 'w') as f:
                    json.dump(data, f)
                    logging.info('Appended ' + value + ' to ' + key + 'Streets and Districts')
                    return 'Success'
            else:
                logging.debug('key ' + key + ' doesnt exist or value already exists')
                return 'key ' + key + ' doesnt exist or value already exists'
    except Exception as e:
        print(e)  # parent of IOError, OSError *and* WindowsError where available
        return 'Error while inserting record ' + e


def get_streetsanddistricts():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'streetsAndDistricts.json'), 'r') as jsonFile:
            data = json.load(jsonFile)
            print(data.items())
            return data
    except Exception as e:
        print(e)  # parent of IOError, OSError *and* WindowsError where available
        return 'Error while getting Streets And  Districts ' + e;


def delete_streetsanddistricts(key, value):
    try:
        with open(os.path.join(os.path.dirname(__file__), 'streetsAndDistricts.json'), 'r') as jsonFile:
            data = json.load(jsonFile)
            values = data.get(key)
            data.get(key).remove(value)
            print(data.get(key))
            with open(os.path.join(os.path.dirname(__file__), 'streetsAndDistricts.json'), 'w') as f:
                json.dump(data, f)
            return 'Success'
    except Exception as e:
        print(e)  # parent of IOError, OSError *and* WindowsError where available
        return 'Error while Deleting Street ' + e


def get_issuesandpriorities():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'IssuesAndPriority.json'), 'r') as jsonFile:
            data = json.load(jsonFile)
            return data
    except Exception as e:
        print(e)  # parent of IOError, OSError *and* WindowsError where available
        error = 'Error while getting Issues and Priorities'
        return 'Error while getting Issues and Priorities ' + e


def insert_newIssue(key, value):
    try:
        with open(os.path.join(os.path.dirname(__file__), 'IssuesAndPriority.json'), 'r') as jsonFile:
            data = json.load(jsonFile)
            keys = data.keys()
            logging.info('Loaded Issues and Priorities')
            if key in keys:
                values = data.get(key)
                if value not in values:
                    data[key].append(value)
                    with open(os.path.join(os.path.dirname(__file__), 'IssuesAndPriority.json'), 'w') as f:
                        json.dump(data, f)
                        logging.info('Appended ' + value + ' to ' + key + 'Issues and Priorities')
                        return 'Success'
                else:
                    logging.debug(value + 'already exists for ' + key)
                    return value + 'already exists for ' + key
            else:
                logging.debug('key ' + key + ' doesnt exist')
                return 'key ' + key + ' doesnt exist'
    except Exception as e:
        print(e)  # parent of IOError, OSError *and* WindowsError where available
        error = 'Error while inserting record'
        return 'Error while inserting record ' + e
