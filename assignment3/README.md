# Overview

This is the homework repository for COMS6998 Cloud Computing and Big Data at Columbia University.

# Important
- Please use `Chrome` browser for the below sign-up/sign-in link.
- We use email verification code in addtion to username/password sign up. You should
sign-up with your email address and fill in the verification code correctly.

# Sign-in username/password
If you don't want to sign up, use the following username/password:
- `username`: yyyy
- `password`: qqqqqq11

# Sign-up/link for cognito (first visit this link)
https://chatbottest.auth.us-east-2.amazoncognito.com/login?response_type=code&client_id=79qedpmlio35ll72il4b0mpmrq&redirect_uri=https://s3.us-east-2.amazonaws.com/yjctest/index.html


# Team member
- Danwen Yang (dy2349)
- Jiachen Yang (jy2865)
- Yu Wang (yw3025)
- Ke Yin (ky2372)

# Sample message

User: Hello

Bot: Hi there, how can I help?

User: I need some restaurant suggestions.

Bot: Great. I can help you with that. What city or city area are you looking to dine in?

User: Manhattan

Bot: Got it, Manhattan. What cuisine would you like to try?

User: Japanese

Bot: Ok, how many people are in your party?

User: Two

Bot: A few more to go. What date?

User: Today

Bot: What time?

User: 7 pm, please

Bot: Great. Lastly, I need your email address so I can send you my findings.

User: john.doe@columbia.edu

Bot: You’re all set. Expect my recommendations shortly! Have a good day.

User: Thank you!

Bot: You’re welcome.

(a few minutes later)

User gets the following email:

“Hello! Here are my Japanese restaurant suggestions for 2 people, for today at 7 pm: 1. Sushi Nakazawa, located at 23 Commerce St, 2. Jin Ramen, located at 3183 Broadway, 3. Nikko, located at 1280 Amsterdam Ave. Enjoy your meal!”



# Main Files
- `lamda_APIgateway.js`: Lambda function from assignment 1: edit it to call lex
- `lambda_validation.py`: initialization and validation for Lex.
- `lambda_fullfill.py`: push Lex result to SQS during fulfillment step.
- `lambda_2.js`:  1. Query ElasticSearch to get the IDs of the top 5 recommended restaurants based on
cuisine. 2. POST your Query to the Search API Use the collected restaurant IDs to query for the corresponding restaurants in DynamoDB. 2. pulling message from SQS every minute and recommending restaurants

# Data Files
- data/File{1,2,3}.csv: data file for assignment
- data/*.json: data file in json format for AWS
- data/*.py, *.ipynb: scripts for dealing with data

# Support Files
see files in assignment 1










