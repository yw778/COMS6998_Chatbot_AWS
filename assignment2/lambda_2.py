import boto3
import json,datetime,os,time
from botocore.vendored import requests


api_key = "zOwmRhh3WILXF6lFGWubbllp17HrSlmwoLO_m0l64srirR9Rw8i28iGBJw-NKSdCPO5MuB0yA5aO2Xtc0rE7vxY3n3oHwIJ_2y2DNvOtMcG4XU3IYEbP70_DCWPFWnYx"

headers = {
    'Authorization': 'Bearer %s' % api_key,
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
        data = {
            "term":"restaurants",
            "location": r_data['location'],
            "categories": r_data['categories'],
            "limit": 3,
            "open_at":r_data["open_at"] - 14400
        }
        
        r = requests.get("https://api.yelp.com/v3/businesses/search", params=data,headers = headers)
    
        text = json.loads(r.text)["businesses"]
    
        start_text = "Hello! Here are your %s restaurant suggestions for %d people, for %s. %s "%(r_data['categories'].capitalize(),r_data['NumPeople'],datetime.datetime.fromtimestamp(r_data['open_at']).strftime('%Y-%m-%d %H:%M:%S'),r_data['categories'].capitalize())
        print start_text
        for i,t in enumerate(text):
            print(t)
            #  = [t['name'],' '.join(t['location']['display_address'])]
            temp_res = '''Restaurant %d: %s, located at %s, price as %s.'''%(i+1,t['name'],t['location']['address1'],t['price'])
            start_text += temp_res
        
        sns = boto3.client('sns')
        number = r_data["Phone number"]
        sns.publish(PhoneNumber = '+1'+str(number), Message=start_text)
        
        SQS_R.delete()
    
    return 'Hello from Lambda'
