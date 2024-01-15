import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import time


def check_bucket_exists(s3_bucket_name):
    s3_client = boto3.client('s3')

    try:
        s3_client.head_bucket(Bucket=s3_bucket_name)
        return True
    except ClientError as e:
        # The bucket does not exist or you have no access.
        return False


def create_bucket(s3_bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=s3_bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=s3_bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        print(e)
        return False
    return True


def upload_to_aws(local_file_name, s3_bucket_name, s3_file_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file
        s3.upload_file(local_file_name, s3_bucket_name, s3_file_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def start_job(s3_bucket_name, s3_file_name):
    # Create a Textract client
    client = boto3.client('textract')

    # Start the asynchronous job
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3_bucket_name,
                'Name': s3_file_name
            }
        })

    return response["JobId"]


def is_job_complete(job_id):
    # Create a Textract client
    client = boto3.client('textract')

    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]

    return status


def get_job_results(job_id):
    pages = []

    # Create a Textract client
    client = boto3.client('textract')

    response = client.get_document_text_detection(JobId=job_id)

    pages.append(response)

    # Handle pagination
    next_token = None
    if 'NextToken' in response:
        next_token = response['NextToken']

    while next_token:
        response = client.get_document_text_detection(JobId=job_id, NextToken=next_token)

        pages.append(response)
        next_token = None
        if 'NextToken' in response:
            next_token = response['NextToken']

    return pages


def delete_file(bucket_name, file_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Delete the file
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        print(f"File {file_name} deleted successfully from bucket {bucket_name}.")
    except ClientError as e:
        return False
    return True


def ocr_pdf(local_file_name):
    s3_bucket_name = 'investmentevaluator-ocr-2024-01-16'
    s3_file_name = local_file_name

    bucket_exists = check_bucket_exists(s3_bucket_name)
    if not bucket_exists:
        bucket_created = create_bucket(s3_bucket_name)

    uploaded = upload_to_aws(local_file_name, s3_bucket_name, s3_file_name)

    job_id = start_job(s3_bucket_name, s3_file_name)
    print(f"Started job with id: {job_id}")

    # Wait for the job to complete
    while is_job_complete(job_id) == "IN_PROGRESS":
        time.sleep(5)

    # Get the results
    response_pages = get_job_results(job_id)

    # Parse and print the results
    text = ''
    for response in response_pages:
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                text += item["Text"] + '\n'

    # Delete the file
    file_deleted = delete_file(s3_bucket_name, s3_file_name)

    return text
