from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = ["https://www.googleapis.com/auth/forms.responses.readonly","https://www.googleapis.com/auth/forms.body.readonly"]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage("token.json")
creds = None
if not creds or creds.invalid:
  flow = client.flow_from_clientsecrets(r"user_account_json_credentials", SCOPES)
  creds = tools.run_flow(flow, store)
service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

# Prints the responses of your specified form:
form_id = "<formid>"
result = service.forms().responses().list(formId=form_id).execute()
result_question = service.forms().get(formId=form_id).execute()
print(result)
print(result_question)