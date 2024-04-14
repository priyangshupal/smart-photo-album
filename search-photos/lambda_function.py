from elasticsearch import Elasticsearch
import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('lex-runtime')
    user = "temp1"
    query = event['queryStringParameters']['q']
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
    client = Elasticsearch(esDomain)
    lex_labels = []
    labels = []
    lex_labels.append(response['slots']['X'])
    for label in lex_labels:
      labels.append({"match":{"labels":label}})
    query = {"bool":{"must": labels}}
    
    response = client.search(index="photos", query=query)
    print(response)
    # if response.status_code == 200:
    #   photos = response.json()['hits']['hits']
    #   if len(photos) > 0:
    #     print('Photos found')
    #   else:
    #     print('No photos found')
    # else:
    #   print('Error while calling Elastic Search')