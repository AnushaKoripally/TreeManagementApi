import os
from datetime import datetime

import boto3
import logging

import botocore
from botocore.exceptions import NoCredentialsError, ClientError


def upload_file(file_name, bucket,object_name,id):
    """
    Function to upload a file to an S3 bucket
    """
    #object_name = file_name

    s3_client = boto3.client('s3')
    try:
         s3_client.upload_file(file_name, bucket, id+'/{}'.format(object_name), ExtraArgs={'ACL': 'public-read'})
         return True
    except FileNotFoundError as e:
         print(e.response)
         logging.debug(e.response['Error']['Message'])
         error = 'The file was not found'
         print(error)
         return '{} {} {} {}'.format(False, None, error, e)
    except NoCredentialsError as e:
         print(e.response)
         logging.debug(e.response['Error']['Message'])
         error = 'Credentials not available"'
         print(error)
         return '{} {} {} {}'.format(False, None, error, e)
    except ClientError as e:
        print(e.response)
        logging.debug(e.response['Error']['Message'])
        error = "Error while adding file to S3"
        print(error)
        return '{} {} {} {}'.format(False, None, error, e)
    except Exception as e:
        logging.debug(e.response['Error']['Message'])
        error = 'Error while adding file to S3'
        print(error)
        return '{} {} {} {}'.format(False, None, error, e)



def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    try:
     for item in s3.list_objects(bucket):
        print(item)
    except ClientError as e:
        error = 'Error in retrieval'
        return '{} {} {} {}'.format(False, None, error, e)

def download_file(eventId, bucket):

 s3 = boto3.resource('s3')
 my_bucket = s3.Bucket(bucket)
 try:
  objects = my_bucket.objects.filter(Prefix=eventId+'/')
  for obj in objects:
     path, filename = os.path.split(obj.key)
     my_bucket.download_file(obj.key, filename)
 except botocore.exceptions.ClientError as e:
     logging.debug(e.response['Error']['Message'])
     error = 'Error extracting file from S3'
     return '{} {} {} {}'.format(False, None, error, e)



