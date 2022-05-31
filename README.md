# CSV-2DDB-AWS-Data-Pipeline

A simple CSV Data Pipeline using a combination of AWS tools. In this project I used AWS CloudFormation generate a stack of resources including S3, Lambda, and DynamoDB. Additionally, I utilized a EC2 instance for uploading.

I wanted this project to serve as a learning experience, so I decided to attempt to automate each step of the process. 


### EC2

Although the CSV file, DATA.csv, was provided via email, I wanted to think about potential solutions for the "extraction" portion of the ETL pipeline, trying to address the following self-guided questions:

- Where is the CSV file being generated, and based on that location, what is a solution that would be both robust and efficient?
 - What are some solutions I could come up with to address the potential updating of the CSV without having to manually upload each time?
 - What are the negative consequences of utilizing EC2?

Through research, I found that it would be ideal to have a python script that runs upon the updating of the CSV. Potentially, based on how often the CSV is updated, a scheduler tool like Cronitor could potentially be used. 

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
#### Resources utilized
- https://aws.amazon.com/blogs/database/implementing-bulk-csv-ingestion-to-amazon-dynamodb/
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
