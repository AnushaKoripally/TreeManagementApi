import json
import logging


def insert_newstreet(key, value):
    try:
        with open('./streetsAndDistricts.json') as jsonFile:
            data = json.load(jsonFile)
            keys = data.keys()
            values = data.get(key)
            logging.info('Loaded Streets and Districts')
            if (key in keys) and (value not in values):
                data[key].append(value)
                with open('./streetsAndDistricts.json', 'w') as f:
                    json.dump(data, f)
                    logging.info('Appended ' + value + ' to ' + key + 'Streets and Districts')
                    return '{} {} {}'.format(True, None, None)
            else:
                logging.debug('key ' + key + ' doesnt exist or value already exists')
                error = 'key ' + key + ' doesnt exist or value already exists'
                return '{} {} {}'.format(False, None, error)
    except Exception as e:
        print(e)  # parent of IOError, OSError *and* WindowsError where available
        error = 'Error while inserting record'
        return '{} {} {} {}'.format(False, None, error, e)


def get_streetsanddistricts():
    try:
        with open('./streetsAndDistricts.json') as jsonFile:
            data = json.load(jsonFile)
            print(data.items())
            return data
    except Exception as e:
        print(e)  # parent of IOError, OSError *and* WindowsError where available
        error = 'Error while getting Streets And  Districts'
        return '{} {} {} {}'.format(False, None, error, e)


def delete_streetsanddistricts(key, value):
    try:
        with open('./streetsAndDistricts.json') as jsonFile:
            data = json.load(jsonFile)
            values = data.get(key)
            data.get(key).remove(value)
            print(data.get(key))
            with open('./streetsAndDistricts.json', 'w') as f:
                json.dump(data, f)
            return '{} {} {}'.format(True, None, None)
    except Exception as e:
        print(e)  # parent of IOError, OSError *and* WindowsError where available
        error = 'Error while Deleting Street'
        return '{} {} {} {}'.format(False, None, error, e)


def get_issuesandpriorities():
    try:
        with open('./IssuesAndPriority.json') as jsonFile:
            data = json.load(jsonFile)
            return '{} {} {}'.format(True, data.items(), None)
    except Exception as e:
        print(e)  # parent of IOError, OSError *and* WindowsError where available
        error = 'Error while getting Issues and Priorities'
        return '{} {} {} {}'.format(False, None, error, e)


def insert_newIssue(key, value):
    try:
        with open('./IssuesAndPriority.json') as jsonFile:
            data = json.load(jsonFile)
            keys = data.keys()
            logging.info('Loaded Issues and Priorities')
            if key in keys:
                values = data.get(key)
                if value not in values:
                    data[key].append(value)
                    with open('./IssuesAndPriority.json', 'w') as f:
                        json.dump(data, f)
                        logging.info('Appended ' + value + ' to ' + key + 'Issues and Priorities')
                        return '{} {} {}'.format(True, None, None)
                else:
                    logging.debug(value + 'already exists for ' + key)
                    error = value + 'already exists for ' + key
                    return '{} {} {}'.format(False, None, error)
            else:
                logging.debug('key ' + key + ' doesnt exist')
                error = 'key ' + key + ' doesnt exist'
                return '{} {} {}'.format(False, None, error)
    except Exception as e:
        print(e)  # parent of IOError, OSError *and* WindowsError where available
        error = 'Error while inserting record'
        return '{} {} {} {}'.format(False, None, error, e)
