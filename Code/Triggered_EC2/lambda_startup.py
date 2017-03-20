# Python code for batch start lambda function
import boto3


def lambda_handler(event, context):
    # TODO implement
    # Connect to EC2
    ec2 = boto3.resource('ec2', region_name = 'us-east-1')

    # Use Boto to start an instance

    worker = ec2.Instance(id='i-0183024e345e93a4a')

    worker.start()

    return 'Started Job'
