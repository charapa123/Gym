from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta, timezone
import psycopg2
import json

# Path to the service account JSON key file
SERVICE_ACCOUNT_FILE = r"<path_to_json_service_account_credentials>"

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
form_id = "<id>"

# Get the form responses
result = service.forms().responses().list(formId=form_id).execute()
result_question = service.forms().get(formId=form_id).execute()
print(result)
print(result_question)

#### This is for when the pipeline is built to update daily

data = []

for item1 in result['responses']:
    a = item1['createTime']
    data.append(a)

print(data)

a = result['responses'][0]['createTime']
print(a)

data = []  # List to store filtered responses
target_date = datetime(2024, 12, 31, tzinfo=timezone.utc).date()  # Set target date (UTC)

# Iterate over the responses
for item in result['responses']:
    # Parse the createTime field
    create_time = datetime.fromisoformat(item['createTime'].replace("Z", "+00:00")).date()
    
    # Check if the response matches the target date
    if create_time == target_date:
        data.append(item)  # Keep the response if it matches the target date

print(f"Filtered responses for {target_date}:")

now = datetime.utcnow()

df = pd.read_csv(r'path_to_logins.csv')
# print(df)
username = df['Username'][1]
password = df['Password'][1]


conn = psycopg2.connect(
    dbname = "gym",
    user = username,
    password = password,
    host = "localhost",
    port="5432"
)
cursor = conn.cursor()

# Insert data
insert_query = '''
SET search_path TO RAW;
INSERT INTO RAW_FORM_Questions (Questions,insert_timestamp)
VALUES (%s,%s);
'''
cursor.execute(insert_query, (json.dumps(result_question), now))
conn.commit()

cursor.close()
conn.close()