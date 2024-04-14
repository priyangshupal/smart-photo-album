import boto3
import base64
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
    user_metadata = s3_response['Metadata']['customlabels'].replace('\'', '').split(',')
    print('user_metadata', user_metadata)
    
    image_object = s3_client.get_object(Bucket=bucketname, Key=filename)
    print('image_object', image_object)
    base64_image = image_object["Body"].read().decode('utf-8')
    
    rekognition_client = boto3.client("rekognition")
    decoded_image=base64.b64decode(base64_image)
    rekognition_response = rekognition_client.detect_labels(
        Image={'Bytes':decoded_image},
        MaxLabels=3,
        MinConfidence=80,
    )

    print("Rekognition response: ", rekognition_response)
    labels = user_metadata
    for label in rekognition_response["Labels"]:
        labels.append(label['Name'].lower())
    print('labels', labels)
    
    esUrl = "https://search-photos-ptdne3we6zyvg2gi2p6khaf5lq.aos.us-east-1.on.aws/photos/_doc"
    headers = {"Content-Type": "application/json"}
    esDoc = {
        'objectKey': filename,
        'bucket': bucketname,
        'createdTimestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'labels': labels
    }
    print(esDoc)
    response = requests.post(
        esUrl,
        data=json.dumps(esDoc).encode("utf-8"),
        headers=headers,
        auth=HTTPBasicAuth('pp2833', 'Elastic@123')
    )
    print("ESIndex response", response.json())
    
    return {"statusCode": 200, "body": json.dumps("Indexed ElasticSearch")}
