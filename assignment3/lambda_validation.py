import json
import datetime
import time
import os
import dateutil.parser
import logging

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


def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

def isvalid_city_location(city):
    valid_cities = ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix', 'san antonio',
                    'san diego', 'dallas', 'san jose', 'austin', 'jacksonville', 'san francisco', 'indianapolis',
                    'columbus', 'fort worth', 'charlotte', 'detroit', 'el paso', 'seattle', 'denver',
                    'washington dc', 'manhattan', 'queens', 'bay area',
                    'memphis', 'boston', 'nashville', 'baltimore', 'portland']
    return city.lower() in valid_cities

def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False

def isvalid_cuisine(cuisine_type):
    valid_cuisines = ['chinese','mexican','newamerican','halal','italian','japanese']
    return cuisine_type.lower() in valid_cuisines

def validate_dining(slots):
    location = try_ex(lambda: slots['Location'])
    cuisine_type = try_ex(lambda: slots['CuisineType'])
    num_people = safe_int(try_ex(lambda: slots['NumPeople']))
    dining_date = try_ex(lambda: slots['DiningDate'])
    dining_time = try_ex(lambda: slots['DiningTime'])
    email = try_ex(lambda: slots['Email'])

    if location and not isvalid_city_location(location):
        return build_validation_result(
            False,
            'Location',
            'We currently do not support {} as a valid destination. Can you try a different city/location?'.format(location)
        )

    if cuisine_type and not isvalid_cuisine(cuisine_type):
        return build_validation_result(
            False,
            'CuisineType',
            'We currently do not provide {} Cuisine.  Can you try a different Cuisine Type?'.format(cuisine_type)
        )
    if num_people:
        if num_people >= 8:
            return build_validation_result(False,'NumPeople','We currently can only hold < 8 people. Try with less people?')

    if dining_date is not None:
        if not isvalid_date(dining_date):
            return build_validation_result(False, 'DiningDate', 'Sorry. We don\'t recognize the date you entered. Can you enter again?')
        elif datetime.datetime.strptime(dining_date, '%Y-%m-%d').date() < datetime.date.today():
            return build_validation_result(False, 'DiningDate', 'You can reserve from today onwards. What day would you like to reserve?')

    if dining_time is not None:
        if datetime.datetime.strptime(dining_date, '%Y-%m-%d').date() == datetime.date.today():
            if datetime.datetime.strptime(dining_date + " " + dining_time, '%Y-%m-%d %H:%M') < (datetime.datetime.now()+ datetime.timedelta(hours=1)):
                return build_validation_result(False, 'DiningTime','Sorry. If you book today\'s resturant, you can only book 1 hours after current time. Can you enter again?')
        if len(dining_time) != 5:
            return build_validation_result(False, 'DiningTime','Sorry. We don\'t recognize the time you entered. Can you enter again?')


    return {'isValid': True}



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

    session_attributes['currentReservation'] = reservation

    # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
    validation_result = validate_dining(intent_request['currentIntent']['slots'])
    if not validation_result['isValid']:
        slots = intent_request['currentIntent']['slots']
        slots[validation_result['violatedSlot']] = None

        return elicit_slot(
            session_attributes,
            intent_request['currentIntent']['name'],
            slots,
            validation_result['violatedSlot'],
            validation_result['message']
        )


    return delegate(session_attributes, intent_request['currentIntent']['slots'])




# --- ThankYou Intent ---
def thankyou_intent(intent_request):
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'You\'re welcome.'
        }
    )
# --- greetIntents ---
def greet_intent(intent_request):
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    return elicit_intent(session_attributes, 'Hi there, how can I help?')

# --- Intents ---
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    if intent_name == "GreetingIntent":
        return greet_intent(intent_request)
    elif intent_name == "ThankYouIntent":
        return thankyou_intent(intent_request)
    elif intent_name == "DiningSuggestionsIntent":
        return diningsuggestions_intent(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


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
