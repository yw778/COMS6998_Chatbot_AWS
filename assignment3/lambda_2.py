import boto3
import json,datetime,os,time
from botocore.vendored import requests

headers = {
    'Content-Type': "application/json",
}

def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='lexTest')
    response = queue.receive_messages(MaxNumberOfMessages=1)
    
    if len(response) == 0:
        return "hello world"
    
    for SQS_R in response:
        r_data = json.loads(SQS_R.body)
    
        body = { "sort": [
            {
              "Score": {
                "order": "desc"
              }
            }
          ],
          "query": {
            "term": {
              "Cuisine": r_data['categories']
            }
          },
          "size": 5
        }
        url = "https://search-movies-wyrw3iyi3rnqu3ajemf6skplua.us-east-1.es.amazonaws.com/predictions/Prediction/_search?"
        r = requests.post(url, data = json.dumps(body), headers = headers)
        content = r.json()["hits"]["hits"]
        restaurant_ids = []
        for i in range(len(content)):
            restaurant_ids.append(content[i]["_source"]["RestaurantID"])
        
        dynamodbTable = boto3.resource('dynamodb').Table('yelp-restaurants')
        
        items = []
        for i in range(len(restaurant_ids)):
            result = dynamodbTable.get_item(
                Key={
                    'RestaurantId': restaurant_ids[i]
                }
            )
        
            # create a response
            items.append(result['Item'])
        
        start_text = "Hello! Here are my %s restaurant suggestions for %d people, for %s. "%(r_data['categories'].capitalize(),r_data['NumPeople'],datetime.datetime.fromtimestamp(r_data['open_at']).strftime('%Y-%m-%d at %H:%M:%S'))
        for i in range(len(items)):
            temp_res = "%d. %s, located at %s. "%(i+1,items[i]['name'],items[i]['address'])
            start_text += temp_res
        start_text += "Enjoy your meal!"
        
        SENDER = "hope2008yang@gmail.com"
        RECIPIENT = r_data['email']
        
        AWS_REGION = "us-east-1"
        
        SUBJECT = "Your recommendation for restaurants"
        
        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = start_text
                    
        CHARSET = "UTF-8"
        
        client = boto3.client('ses',region_name=AWS_REGION)
        
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
        
        SQS_R.delete()
        print start_text
