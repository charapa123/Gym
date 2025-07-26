from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta, timezone
import json
import os
import sys
from googleapiclient.errors import HttpError

sheet_name = sys.argv[1]  # e.g., "Workout Form Responses"

# Load secrets securely
FORM_ID = os.getenv("FORM_ID")
SERVICE_ACCOUNT_FILE = "service_account.json"
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")

# Scopes for accessing Google Forms responses
SCOPES = ["https://www.googleapis.com/auth/forms.responses.readonly","https://www.googleapis.com/auth/forms.body.readonly","https://www.googleapis.com/auth/spreadsheets"]

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



data = []  # List to store filtered responses
# target_date = datetime(2024, 12, 31, tzinfo=timezone.utc).date()  # Set target date (UTC)
target_date = datetime.now(timezone.utc).date() - timedelta(days=1)

# Iterate over the responses
for item in result:
    # Parse the createTime field
    create_time = datetime.fromisoformat(item['createTime'].replace("Z", "+00:00")).date()
    
    # Check if the response matches the target date
    if create_time == target_date:
        data.append(item)  # Keep the response if it matches the target date

# print(f"Filtered responses for {target_date}:")

now = datetime.utcnow()


# Check if data is empty
if not data:
    print("No available data. Exiting.")
    sys.exit()  # Stops the script
else:
    print("Data found:")

def extract_flattened_answers(data):
    rows = []
    for response in data:
        insert_timestamp = datetime.now(timezone.utc).isoformat()
        response_id = response.get('responseId')
        create_time = response.get('createTime')
        respondent_email = response.get('respondentEmail')

        answers = response.get('answers', {})
        for question_id, val in answers.items():
            try:
                text_items = val['textAnswers']['answers']
                if text_items:
                    answer_value = text_items[0]['value'].strip()
                    rows.append({
                        'insert_timestamp': insert_timestamp,
                        'response_id': response_id,
                        'create_time': create_time,
                        'respondent_email': respondent_email,
                        'question_id': question_id,
                        'answer': answer_value
                    })
            except (KeyError, IndexError, TypeError):
                continue
    return pd.DataFrame(rows)

def extract_question_map(questions):
    qmap = {}
    for item in questions.get('items', []):
        try:
            title = item.get('title', '')
            if 'Exercises' in title:
                title = 'Exercises'
            question = item.get('questionItem', {}).get('question', {})
            question_id = question.get('questionId')
            if question_id:
                qmap[question_id] = title
        except Exception:
            continue
    return qmap

def pivot_with_pandas(flat_df, question_map):
    flat_df['question_title'] = flat_df['question_id'].map(question_map)

    # Keep only questions we care about
    filtered_df = flat_df[
        flat_df['question_title'].isin([
            'Which body part did you work out?',
            'How heavy was the weight?',
            'How many reps?',
            'Exercises'
        ])
    ]

    # Pivot
    pivot_df = filtered_df.pivot_table(
        index=['insert_timestamp', 'response_id', 'create_time', 'respondent_email'],
        columns='question_title',
        values='answer',
        aggfunc='first'  # Mimics MAX(... FILTER ...) in SQL
    ).reset_index()

    # Rename columns to match SQL output
    pivot_df = pivot_df.rename(columns={
        'Which body part did you work out?': 'Body_Part',
        'How heavy was the weight?': 'Weight',
        'How many reps?': 'Reps',
        'Exercises': 'Exercises'
    })

    return pivot_df

# Usage:
# form_answers = [...]  # raw_form_answers data
# form_questions = {...}  # raw_form_questions data

df_answers = extract_flattened_answers(data)
question_map = extract_question_map(result_question)
final_df = pivot_with_pandas(df_answers, question_map)
final_df['create_time'] = pd.to_datetime(final_df['create_time'], utc=True, format='mixed')
final_df = final_df.sort_values(by='create_time')


print(final_df)

service_sheets = build(
    "sheets", "v4", credentials=credentials)


# Now final_df is a pivoted DataFrame, similar to your final SQL SELECT result

def append_dataframe_to_sheets(df, spreadsheet_id, sheet_name, service_sheets):
    # Prepare data (convert DataFrame to list of lists)
    values = df.astype(str).values.tolist()

    body = {
        'values': values
    }

    try:
        result = service_sheets.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A1",  # Start range; Google Sheets will append automatically
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()

        updates = result.get('updates', {})
        print(f"{updates.get('updatedRows', 0)} rows appended to {sheet_name}")
    except Exception as error:
        print(f"Append failed: {error}")

    
append_dataframe_to_sheets(
    df=final_df,
    spreadsheet_id=GOOGLE_SHEETS_ID,
    sheet_name="Sheet1",
    service_sheets=service_sheets
)

# Now final_df is a pivoted DataFrame, similar to your final SQL SELECT result
