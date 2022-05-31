# CSV-2DDB-AWS-Data-Pipeline

A simple CSV Data Pipeline using a combination of AWS tools. In this project I used AWS CloudFormation to generate a stack of resources including S3, Lambda, and DynamoDB. Additionally, I utilized a EC2 instance for uploading.

I wanted this project to serve as a learning experience, so I decided to attempt to automate each step of the process. 

> Note: This particular solution is entirely serverless if the DATA.csv file is manually uploaded to the S3 bucket.

### EC2

Although the CSV file, DATA.csv, was provided via email, I wanted to think about potential solutions for the "extraction" portion of the ETL pipeline, trying to address the following self-guided questions:

- Where is the CSV file being generated, and based on that location, what is a solution that would be both robust and efficient?
 - What are some solutions I could come up with to address the potential updating of the CSV without having to manually upload each time?
 - What are the negative consequences of utilizing EC2?

Through research, I found that it would be ideal to have a python script that runs upon the updating of the CSV. Potentially, based on how often the CSV is updated, a scheduler tool like Cronitor could be used. 

One negative consequence of a EC2 is that the static costs, depending on function, typically outweigh low-volume on-demand function triggers (will speak more on this later). 

### S3 - `csv-2ddb-bucket`

Amazon Simple Storage Service (Amazon S3) is an object storage service used in this project to store the CSV, `DATA.csv`. 

In this project, the S3 bucket used has a event trigger for a lambda function to upload directly to the DynamoDB, but only for the specified CSV file name. 

One main benefit of S3 in terms of automation are its Event Notifications which can be configured and utilized in AWS Lambda Functions. 

### AWS Lambda - `CSV-2DDB`

In this project, the Lambda function used is responsible for inserting directly into the DynamoDB table, `csv-2ddb-table`, upon the event trigger of a file upload to our S3 bucket, `csv-2ddb-bucket`. 

Assuming the CSV file is in the correct format, determined by the attribute definitions in the CloudFormation template developed, and the file name of the CSV matches the one assigned in the template, the lambda function will operate correctly and insert all of the data in batches into the DynamoDB.

The main benefit of AWS lambda is that it can be event driven. In this case, the lambda function used takes care of the "load" portion of the ETL pipeline. One thing to note, however, is that this lambda function could also take care of both load and transform, but for a scalable solution it would require another layer. 

I opted to pre-process in the EC2 instance because of the minimal transformation required for the specific dataset provided. 

###  DynamoDB - `csv-2ddb-table`
DynamoDB is a proprietary NoSQL database. Upon upload event-trigger, the AWS lambda function loads the data directly into the DynamoDB table. The partition key is located in the first column of the CSV file as prescribed in the CloudFormation template, and requires the first column to be named `uuid`. 

Once the data is loaded into the DynamoDB, data can be queried and mutated easily. One such option is via AWS's SDK, `boto3`. 

### Identity & Access Management

In order to upload via EC2 to the S3 bucket, a new user with S3 write permission was required to generate AWS user credentials necessary for Boto3. This was done by allowing a user, `test-user`, the `AmazonS3FullAccess` permission. Further research to restrict the permission should be done. 

Additionally, in order for the lambda function to work properly for the automatic loading of csv data into the DynamoDB, the following roles had to be assigned:
- S3ReadOnlyAccess : lambda function reading the csv file from S3
- AWSLambdaBasicExecutionRole : allow logs to be uploaded to CloudWatch for reference
- AWSLambdaInvocation-DynamoDB : provides reach access to DynamoDB streams

Select action policies were also added such as:
- dyanmodb:PutItem
- dynamodb:BatchWriteItem

## Steps
### Initial Setup:

 1. Navigate to https://aws.amazon.com/blogs/database/implementing-bulk-csv-ingestion-to-amazon-dynamodb/ and follow all listed steps
 2. Clone/Copy lambda function and replace existing code with the code provided, be sure to note and adjust directory for the line, `obj = s3.Object(bucket, "/home/ubuntu/pipeline/CSV-2DDB-AWS-Data-Pipeline/"+str(key)).get()['Body']`, as the environment variable does not explicitly contain the directory, just the file name and extension.
 3. Create an AWS user with `AmazonS3FullAccess` permission and be sure to save the access_key and secret_access_key.
 4. Clone this repository in a local or VM environment and in `secrets.py`, put your access_key and secret_access_key in the indicated variables. 
 5. In `secrets.py`, adjust the CSV's file location and S3 bucket name as needed.
 6. If all has been set up correctly, open a local terminal and use `python3 uploader.py` to upload the csv to the s3 bucket, which will automatically load the data into the DynamoDB.

#### Dependencies for Uploader
- pandas : `pip install pandas`
- boto3 : `pip install boto3`

#### Resources utilized
- https://aws.amazon.com/blogs/database/implementing-bulk-csv-ingestion-to-amazon-dynamodb/
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
- https://github.com/aws-samples/csv-to-dynamodb
