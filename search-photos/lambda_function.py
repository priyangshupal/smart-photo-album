from elasticsearch import Elasticsearch
import json
import boto3
import base64

def lambda_handler(event, context):
    client = boto3.client('lex-runtime')
    user = "temp1"
    print(event)
    query = ''
    try:
      if 'queryStringParameters' in event.keys():
        if 'q' in event['queryStringParameters'].keys():
            query = event['queryStringParameters']['q']
      elif 'params' in event.keys():
        if 'querystring' in event['params'].keys():
            query = event['params']['querystring']['q']
    except:
      query = "Give me photos of dogs"
    print('query', query)
    if query is None or len(query) < 1:
      return {
        'statusCode': 200,
        "headers": {
        "Access-Control-Allow-Headers" : "*",
        "Access-Control-Allow-Origin": "*", 
        "Access-Control-Allow-Methods": "*" 
        },
        'body': json.dumps("Please try again.")
      }
    
    print("Reaching Here!")
    
    response = client.post_text(botName='getContexttwo',
                                botAlias='ConBot',
                                userId=user,
                                inputText=query)
    print("Reaching Here2!")
    
    first_term = None
    second_term = None
    if 'slots' in response.keys():
      if 'X' in response['slots']:
          first_term = response['slots']['X']
      if 'Y' in response['slots']:
          second_term = response['slots']['Y']
    print(first_term, second_term)
    esDomain = "https://search-photos-ptdne3we6zyvg2gi2p6khaf5lq.aos.us-east-1.on.aws/"
    es_client = Elasticsearch(esDomain)
    lex_labels = []
    if (first_term is not None):
      lex_labels.append(first_term)
    if (second_term is not None):
      lex_labels.append(second_term)
    labels = []
    for label in lex_labels:
      labels.append({"match":{"labels":label}})
    query = {"query": {"bool":{"must": labels}}}
    
    matched_photo_names= []
    try:
      response = es_client.search(
        index='photos', 
        body=query,
        headers={'Authorization': 'Basic cHAyODMzOkVsYXN0aWNAMTIz'}
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