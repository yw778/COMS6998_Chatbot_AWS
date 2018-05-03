import json
import datetime
import time
import os
import dateutil.parser
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# --- Helpers that build all of the responses ---
def elicit_intent(session_attributes, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitIntent',
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# --- Helper Functions ---
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def safe_int(n):
    """
    Safely convert n value to int.
    """
    if n is not None:
        return int(n)
    return n

def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None

# --- DiningSuggestionsIntent ---
def diningsuggestions_intent(intent_request):
    location = try_ex(lambda: intent_request['currentIntent']['slots']['Location'])
    cuisine_Type = try_ex(lambda: intent_request['currentIntent']['slots']['CuisineType'])
    num_people = safe_int(try_ex(lambda: intent_request['currentIntent']['slots']['NumPeople']))
    dining_date = try_ex(lambda: intent_request['currentIntent']['slots']['DiningDate'])
    dining_time = try_ex(lambda: intent_request['currentIntent']['slots']['DiningTime'])
    Email = try_ex(lambda: intent_request['currentIntent']['slots']['Email'])
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}


    # Load confirmation history and track the current reservation.
    reservation = json.dumps({
        'ReservationType': 'Dining',
        'Location':location,
        'CuisineType': cuisine_Type,
        'NumPeople': num_people,
        'DiningDate': dining_date,
        'DiningTime': dining_time,
        'email': Email,
    })
    
    
    open_at = time.mktime(datetime.datetime.strptime(dining_date + " " + dining_time ,"%Y-%m-%d %H:%M").timetuple())
    query_information = json.dumps({
        'term': "restaurants",
        'location':location,
        'categories': cuisine_Type,
        'NumPeople': num_people,
        'open_at': int(open_at),
        'email': Email,
    }) 

    
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='lexTest')
    response = queue.send_message(MessageBody=query_information)


    session_attributes['currentReservation'] = reservation
    session_attributes['lastConfirmedReservation'] = reservation

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'You\'re all set. Expect my recommendations shortly! Have a good day.'
        }
    )

# --- Intents ---
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
    return diningsuggestions_intent(intent_request)



# --- Main handler ---
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)