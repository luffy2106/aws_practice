# Retrieve the list of existing buckets

import logging
import boto3
from botocore.exceptions import ClientError



ACCESS_KEY = "your access key"
SECRET_KEY = "your secret key"


client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
    # aws_session_token=SESSION_TOKEN
)

# client_ec2 = boto3.client('ec2', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
# response_ec2 = client_ec2.describe_instances()
# print(response_ec2)

# s3 = boto3.client('s3')
response = client.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

