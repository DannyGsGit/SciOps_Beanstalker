# Manually triggered and scheduled EC2 batch jobs

## Intuition
AWS Lambda functions are an enticing method of serverless compute to minimize the cost of EC2 instances when code is not running. Unfortunately, Lambda imposes a 50MB limit for all code and dependencies- this poses a problem for Python ML workloads where package dependencies alone will run over 50MB.

This template demonstrates a method to use Lambda functions to manage EC2 instances in a way that approximates the functionality of Lambda functions, but with the additional compute power and configuration options of a full EC2 instance. The trade-off for this additional flexibility is speed; whereas a Lambda function execution is instantaneous, the launcher/scheduler architecture requires an EC2 instance to boot before computation happens. This results in delays for 30 seconds, in addition to the time required to run computation. As such, it is useful to consider the launcher/scheduler an asynchronous batch process like the Worker role in the Elastic Beanstalk web service architecture.

The EC2 instance where computation will happen is fundamentally a standard EC2 instance that includes the code to be executed, and a CRON scheduler configured to run our code upon booting.

## EC2 Configuration
This template describes a launched/scheduler built on an EC2 image with the Ubuntu 14.04 LTS operating system, using *crontab* to schedule code execution at startup. The *boto* Python package is used to integrate EC2 to other AWS services like S3. It is important to note that *crontab* does not execute in the rich Bash CLI shell we interact with, and does not have access to environment variables we rely on in a typical Bash session.

In this template we will execute the *ride_pred.py* script, which uses *boto* to obtain a CSV from an S3 bucket, process the data, and write results to an output S3 bucket. To setup EC2:
* Place *ride_pred.py* in the /bin directory of the EC2 instance
* Install all system and Python dependencies at the system level- for simplicity, we will not use virtual environments in this example as the Virtual Env Wrapper environment is not setup to work with the sh CLI shell used by cron.
* Edit the cron scheduler with the following command:
```
$ sudo crontab -e
```
In the crontab file, add the following line:
```
@reboot python3 /bin/ride_pred.py &
```


## Lambda Startup Function
```
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
```

## Lambda Shutdown Function
```
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
```

## Design Consideration
In this example, we use Lambda to start and stop a single EC2 instance- the advantage of this is a relatively short startup time compared to *creating* and *terminating* EC2 instances. The flaw of this architecture is an inability to manage concurrent requests. In many cases, it is likely preferable to create/terminate instances so that Lambda can auto-provision as many EC2 instances as necessary to handle incoming requests.

Not covered in this template, but worth future consideration is a hybrid approach- pre-provisioning multiple instances to be used by Lambda for a "warm start", while including the ability to *create* new instances if we run out of paused instances.
