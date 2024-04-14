from elasticsearch import Elasticsearch
import json
import boto3
import base64

def lambda_handler(event, context):
    client = boto3.client('lex-runtime')
    user = "temp1"

    try:
        query = event['queryStringParameters']['q']
    except:
        query = "Give me photos of dogs"
    test = {'test': query}
    
    botMessage = "Please try again.";
    if query is None or len(query) < 1:
      return {
        'statusCode': 200,
        "headers": {
        "Access-Control-Allow-Headers" : "*",
        "Access-Control-Allow-Origin": "*", 
        "Access-Control-Allow-Methods": "*" 
        },
        'body': json.dumps(botMessage)
      }
    
    print("Reaching Here!")
    
    response = client.post_text(botName='getContexttwo',
                                botAlias='ConBot',
                                userId=user,
                                inputText=query)
    print("Reaching Here2!")
    print(response['slots']['X'])
    
    
    esDomain = "https://search-photos-ptdne3we6zyvg2gi2p6khaf5lq.aos.us-east-1.on.aws/"
    es_client = Elasticsearch(esDomain)
    lex_labels = []
    labels = []
    lex_labels.append(response['slots']['X'])
    for label in lex_labels:
      labels.append({"match":{"labels":label}})
    query = {"query": {"bool":{"must": labels}}}
    
    matched_photo_names= []
    try:
      response = es_client.search(
        index='photos', 
        body=query,
        headers={'Authorization': ''}
      )
      photos = response['hits']['hits']
      if len(photos) > 0:
        for photo in photos:
          matched_photo_names.append(photo['_source']['objectKey'])
      else:
        print('No photos found with given labels')
    except Exception as error:
      print('Error while searching ElasticSearch:', error)
      raise error
    
    print('matched_photo_names', matched_photo_names)
    
    images = []
    s3_client = boto3.client('s3')
    
    for matched_photo_name in matched_photo_names:
      try:
        obj = s3_client.get_object(Bucket="cloudasst3-b2", Key=matched_photo_name)
        images.append(obj["Body"].read().decode('utf-8'))
      except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error fetching image: {str(e)}"
        }
    return {
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
        },
        'statusCode': 200,
        'messages': json.dumps("This is Working!"),
        'images': images
    }