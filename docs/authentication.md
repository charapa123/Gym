# Authentication and Secrets Management

## Overview

The project uses Google APIs for Google Forms and Google Sheets. The authentication approach evolved during development from OAuth 2.0 to a Google Cloud Service Account.

This change was made so the pipeline could run automatically in GitHub Actions without requiring manual login.

---

## Initial OAuth approach

The original approach used an OAuth Client ID and Client Secret.

This worked for local development, but it required interactive authentication when the script ran.

That made it unsuitable for scheduled execution because GitHub Actions workflows need to run without manual user approval.

---

## Service Account migration

The final implementation uses a Google Cloud Service Account.

A Service Account is better suited to this project because the pipeline is a server-to-server process rather than an interactive user application.

Benefits:

- No manual login required
- Suitable for scheduled execution
- Works inside GitHub Actions
- Separates pipeline identity from a personal Google login

---

## Google API scopes

The PostgreSQL pipeline uses Google Forms scopes:

```python
SCOPES = [
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/forms.body.readonly"
]
```

The Google Sheets reporting pipeline also includes the Sheets scope:

```python
SCOPES = [
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/spreadsheets"
]
```

---

## Service Account setup

The setup process was:

1. Create a Google Cloud project
2. Enable the Google Forms API
3. Enable the Google Sheets API
4. Create a Service Account
5. Generate a Service Account JSON key
6. Share the Google Form with the Service Account email
7. Share the Google Sheet with the Service Account email
8. Store the encoded key in GitHub Secrets

The Service Account behaves like its own Google identity. Authentication alone is not enough; the Form and Sheet also need to be shared with the Service Account so it is authorised to access them.

---

## Runtime authentication

Both scripts load credentials from a runtime-generated JSON file:

```python
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)
```

The file is not committed to GitHub. It is created during workflow execution from a GitHub Secret.

---

## GitHub Secrets

Sensitive values are stored in GitHub Secrets and injected at runtime.

Secrets used by the project include:

| Secret | Purpose |
|---|---|
| `SERVICE_ACCOUNT_FILE` | Base64-encoded Service Account JSON key |
| `FORM_ID` | Google Form identifier |
| `GOOGLE_SHEETS_ID` | Google Sheet identifier for the reporting pipeline |
| `USERNAME` | PostgreSQL username |
| `PASSWORD` | PostgreSQL password |
| `SCHEMA` | PostgreSQL/dbt target schema |
| `DB_NAME` | PostgreSQL database name |

The dbt profile also uses environment variables:

```yaml
user: "{{ env_var('DBT_USER') }}"
password: "{{ env_var('DBT_PASSWORD') }}"
dbname: "{{ env_var('DBT_DBNAME') }}"
schema: "{{ env_var('DBT_SCHEMA') }}"
```

---

## Credential decoding in GitHub Actions

The reporting workflow runs on a GitHub-hosted Ubuntu runner and decodes the Service Account JSON using Bash:

```yaml
- name: Decode service account JSON (bash)
  shell: bash
  run: |
    echo "${{ secrets.SERVICE_ACCOUNT_FILE }}" | base64 -d > service_account.json
```

The analytics workflow runs on a self-hosted Windows runner and decodes the same secret using PowerShell:

```yaml
- name: Decode service account JSON (Windows PowerShell)
  shell: powershell
  run: |
    $decoded = [System.Text.Encoding]::UTF8.GetString(
      [System.Convert]::FromBase64String("${{ secrets.SERVICE_ACCOUNT_FILE }}")
    )
    Set-Content -Path "service_account.json" -Value $decoded
```

---

## Authentication vs authorisation

Authentication answers:

```text
Who is running the pipeline?
```

Authorisation answers:

```text
What resources can that identity access?
```

The Service Account authenticates the pipeline, but access to the Google Form and Google Sheet is granted by sharing those resources with the Service Account email.

---

## Security considerations

- Service Account keys are not committed to source control
- Database credentials are injected through GitHub Secrets
- dbt credentials are configured through environment variables
- The local PostgreSQL database is not exposed publicly
- Generated credential files are created at runtime only
