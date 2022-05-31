from secrets import file_, bucket, SECRET_ACCESS_KEY, ACCESS_KEY

import boto3
from botocore.exceptions import ClientError
import pandas as pd

#Read, Transform, and Write locally
def transform(file_):
    #Read in locally stored file into a dataframe
    df = pd.read_csv(file_)

    #replace the first column label with 'uuid', necessary formatting for DynamoDB
    df = df.rename(columns={df.columns[0]:'uuid'})

    #write to local csv file
    df.to_csv(file_, index=False)

#Upload to S3 bucket
def upload(client, file_, bucket):
    try:
        response = client.upload_file(file_, bucket, file_)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    transform(file_)
    client = boto3.client('s3', aws_access_key_id = ACCESS_KEY,
                                aws_secret_access_key = SECRET_ACCESS_KEY)
    upload(client, file_, bucket)