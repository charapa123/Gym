from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta, timezone
import psycopg2
import json
import os
import sys

sheet_name = sys.argv[1]  # e.g., "Workout Form Responses"

# Load secrets securely
FORM_ID = os.getenv("FORM_ID")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SERVICE_ACCOUNT_FILE = "service_account.json"
SCHEMA = os.getenv("SCHEMA")
DB_NAME = os.getenv("DB_NAME")

# Now you can connect securely using these values




# Scopes for accessing Google Forms responses
SCOPES = ["https://www.googleapis.com/auth/forms.responses.readonly","https://www.googleapis.com/auth/forms.body.readonly"]

# Load the service account credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build the Google Forms API service
service = build(
    "forms", "v1", credentials=credentials, discoveryServiceUrl="https://forms.googleapis.com/$discovery/rest?version=v1"
)

# # Form ID to retrieve responses
form_id = FORM_ID

# Get the form responses
# result = service.forms().responses().list(formId=form_id).execute()
result_question = service.forms().get(formId=form_id).execute()
# print(result)
# print(result_question)

result = []
page_token = None

while True:
    request = service.forms().responses().list(
        formId=form_id,
        pageSize=100,  # Max is 1000
        pageToken=page_token
    )
    response = request.execute()

    result.extend(response.get("responses", []))

    page_token = response.get("nextPageToken")
    if not page_token:
        break



conn = psycopg2.connect(
    dbname = DB_NAME,
    user = USERNAME,
    password = PASSWORD,
    host = "localhost",
    port="5432"
)

cursor = conn.cursor()

cursor.execute(
    '''
set search_path to pres;

SELECT max(date(create_time))
FROM "GYM_RESPONSE"
'''
)
posgres_result = cursor.fetchone()   # returns a tuple
max_date = posgres_result[0]         # extract the value

print(max_date)



data = []  # List to store filtered responses 

# Iterate over the responses
for item in result:
    # Parse the createTime field
    create_time = datetime.fromisoformat(item['createTime'].replace("Z", "+00:00")).date()
    
    # Check if the response matches the target date
    if create_time > max_date:
        data.append(item)  # Keep the response if the data doesn't already exist in database

now = datetime.utcnow()

#Insert data
insert_query = '''
SET search_path TO RAW;
INSERT INTO RAW_FORM_ANSWERS (ANSWERS,INSERT_TIMESTAMP)
VALUES (%s,%s);
'''

for item in data:
    # cur.execute(insert_query, (json.dumps(item), now))
    cursor.execute(insert_query, (json.dumps(item), now))

# cursor.execute("TRUNCATE TABLE raw.raw_form_questions;")

insert_question = '''
SET search_path TO RAW;
INSERT INTO RAW_FORM_QUESTIONS (QUESTIONS,INSERT_TIMESTAMP)
VALUES (%s,%s);
'''
cursor.execute(insert_question, (json.dumps(result_question), now))

conn.commit()
cursor.close()
conn.close()

