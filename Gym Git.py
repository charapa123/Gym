from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta, timezone

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