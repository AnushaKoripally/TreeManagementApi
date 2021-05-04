import os
import pathlib
from datetime import datetime
from os.path import join, dirname, realpath
import io
from base64 import encodebytes
from PIL import Image
from boto import Config
from flask import jsonify
#from Face_extraction import face_extraction_v2
import boto3
import logging

import botocore
from botocore.exceptions import NoCredentialsError, ClientError


def upload_file(file_name, bucket,object_name,id):
    """
    Function to upload a file to an S3 bucket
    """
    #object_name = file_name
    print(file_name)
    s3_client = boto3.client('s3')
    try:
         response = s3_client.upload_file(file_name, bucket, id+'/{}'.format(object_name), ExtraArgs={'ACL': 'public-read'})
         print(response)
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

def append_file(file_name, bucket,object_name):
    """
    Function to upload a file to an S3 bucket
    """
    #object_name = file_name
    print(file_name)
    s3_client = boto3.client('s3')
    try:
         response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read'})
         print(response)
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

 downloadPath = join(dirname(realpath(__file__)), 'DOWNLOAD_FOLDER')
 s3 = boto3.resource('s3')
 my_bucket = s3.Bucket(bucket)
 filelist = []
 try:
   objects = my_bucket.objects.filter(Prefix=eventId+'/')
   for obj in objects:
      url = boto3.client('s3').generate_presigned_url(ClientMethod='get_object',Params={'Bucket': bucket, 'Key': obj.key},ExpiresIn=3600)
      #path, filename = os.path.split(obj.key)
      #my_bucket.download_file(obj.key, downloadPath+'\\'+filename)
      #k= pathlib.Path(downloadPath + '\\' + filename).resolve()
      #filelist.append(pathlib.Path(downloadPath+'\\'+filename).resolve().as_uri())
      filelist.append(url)
   return filelist
 except botocore.exceptions.ClientError as e:
     logging.debug(e.response['Error']['Message'])
     error = 'Error extracting file from S3'
     return '{} {} {} {}'.format(False, None, error, e)

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


