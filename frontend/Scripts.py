# Random Changes to Lambda Function

#Around Line 15

try:
    if 'queryStringParameters' in event.keys():
        if 'q' in event['queryStringParameters'].keys():
            query = event['queryStringParameters']['q']
    elif 'params' in event.keys():
        if 'querystring' in event['params'].keys():
            query = event['params']['querystring']['q']
            
except:
    
    query = "Give me photos of dogs"


#After Getting Lex Response

first_term = None
second_term = None
if 'slots' in response.keys():
    if 'X' in response['slots']:
        first_term = response['slots']['X']
    if 'Y' in response['slots']:
        second_term = response['slots']['Y']

print(first_term)
print(second_term)


