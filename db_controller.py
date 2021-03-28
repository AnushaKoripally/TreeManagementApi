import boto3

dynamo_client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")

def get_items():
    return dynamo_client.scan(
        TableName='Users'
    )

