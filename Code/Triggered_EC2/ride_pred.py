import boto3
import pandas as pd
from io import StringIO
import datetime

# Connect to S3
s3_conn = boto3.resource('s3')
bucket_name = 'sciops-inbox'
bucket = s3_conn.Bucket(bucket_name)

# Get contents
df = None
for obj in bucket.objects.all():
    file = obj.get()['Body']
    if df is None:
        df = pd.read_csv(file)
    else:
        temp = pd.read_csv(file)
        df = df.append(temp)

# Add a calculated column
col_list = ['weathersit', 'weekday']
df['pred'] = df[col_list].sum(axis = 1)

# Connect to write bucket
write_bucket = 'sciops-outbox'
out_bucket = s3_conn.Bucket(write_bucket)

# Generate unique filename
base_name = "ridepred_"
ts = datetime.datetime.now().strftime("%d_%m_%Y_%H%M%S")
file_name = base_name + ts + '.csv'

# Write results to bucket
csv_buffer = StringIO()
df.to_csv(csv_buffer)
s3_conn.Object(write_bucket, file_name).put(Body=csv_buffer.getvalue())
