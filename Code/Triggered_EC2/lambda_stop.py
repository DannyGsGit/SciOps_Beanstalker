# Python code to stop batch job

## NOTE: Extend the timeout configuration to ~30 seconds. Default of 3 seconds is too short
##  for all events to properly trigger.

import boto3


def lambda_handler(event, context):
    # TODO implement
    # Delete inbox contents
    s3_conn = boto3.resource('s3', region_name = 'us-east-1')
    bucket_name = 'sciops-inbox'
    bucket = s3_conn.Bucket(bucket_name)
    for obj in bucket.objects.all():
        obj.delete()

    # Connect to EC2
    ec2 = boto3.resource('ec2', region_name = 'us-east-1')

    # Use Boto to stop an instance
    worker = ec2.Instance(id='i-0183024e345e93a4a')
    worker.stop()


    return 'Stopped Job'
