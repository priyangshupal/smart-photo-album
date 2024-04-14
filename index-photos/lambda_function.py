import boto3
import json
from datetime import datetime
from requests.auth import HTTPBasicAuth
import requests

def lambda_handler(event, context):
    print("event", event)

    bucketname = event["Records"][0]["s3"]["bucket"]["name"]
    filename = event["Records"][0]["s3"]["object"]["key"]

    s3_client = boto3.client("s3")
    s3_response = s3_client.head_object(Bucket=bucketname, Key=filename)
    print("s3_response", s3_response)

    rekognition_client = boto3.client("rekognition")
    rekognition_response = rekognition_client.detect_labels(
        Image={"S3Object": {"Bucket": bucketname, "Name": filename}},
        MaxLabels=3,
        MinConfidence=80,
    )

    print("Rekognition response: ", rekognition_response)
    labels = []
    for label in rekognition_response["Labels"]:
        labels.append(label['Name'])
    print('labels', labels)
    
    esDomain = "https://search-photos-ptdne3we6zyvg2gi2p6khaf5lq.aos.us-east-1.on.aws"
    headers = {"Content-Type": "application/json"}
    esDoc = {
        'objectKey': filename,
        'bucket': bucketname,
        'createdTimestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'labels': labels
    }
    print(esDoc)
    # response = requests.post(
    #     url, 
    #     data=json.dumps(body).encode("utf-8"), 
    #     headers=headers, 
    #     auth=HTTPBasicAuth('pp2833', 'ElasticSearch@123')
    # )
    
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}