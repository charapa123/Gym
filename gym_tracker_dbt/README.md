# Gym Tracker Data Pipeline

![Architecture Diagram](docs\images\Architecture_diagram.png)

## Overview

This project explores two approaches to delivering analytics from Google Forms workout data.

The first pipeline extracts workout responses from the Google Forms API and publishes them to Google Sheets through a scheduled GitHub Actions workflow. This provides a lightweight reporting layer for future Tableau Public dashboards.

The second pipeline follows a modern analytics engineering workflow. Google Forms responses are loaded into PostgreSQL, transformed with dbt, tested, and modelled into an analytics-ready dataset.

The project was built to practise and demonstrate:

- API ingestion
- Exercise-set data modelling
- Dynamic metadata handling
- Incremental loading
- Cloud authentication
- GitHub Actions orchestration
- PostgreSQL loading
- dbt modelling, testing and freshness checks

---

## Architecture

The solution has two delivery paths built from the same Google Forms source.

### Reporting pipeline

Google Forms → Python ETL → Google Sheets → Tableau Public

### Analytics engineering pipeline

Google Forms → Python ETL → PostgreSQL → dbt → Analytics dataset

Detailed architecture notes are available in [`docs/architecture.md`](docs/architecture.md).

---

## Engineering highlights

### 1. Exercise-set data grain

The pipeline is designed around a clear analytical grain: **one Google Form response equals one completed exercise set**.

Each response captures:

```text
Body Part → Exercise → Weight → Reps
```

This design informed the Google Form structure, Python extraction logic, PostgreSQL raw tables and final dbt presentation model.

### 2. Dynamic exercise metadata

Exercise options are extracted from Google Forms metadata rather than being hardcoded.

The form was intentionally designed so exercise-selection questions include `Exercises` in the title. This allows new exercises to be added through the form interface without changing the Python ingestion scripts or dbt models.

### 3. Incremental loading

The PostgreSQL pipeline checks the latest processed response in the presentation model and only inserts newer responses.

This reduces unnecessary processing and helps prevent duplicate records.

### 4. Automated authentication

The project initially used OAuth 2.0 authentication, but this required interactive login and was unsuitable for automation.

The final implementation uses a Google Cloud Service Account stored securely through GitHub Secrets, enabling automated execution in GitHub Actions.

### 5. Workflow orchestration

Two GitHub Actions workflows are used:

- `Daily Gym Data Pipeline Google Sheets` runs on a scheduled GitHub-hosted runner.
- `Gym Data Pipeline` runs manually on a self-hosted runner so it can connect to local PostgreSQL.

### 6. Data quality and reliability

The dbt project includes tests and source freshness monitoring. The analytics workflow runs `dbt debug` and `dbt build`, executing models and validations as part of the pipeline.

---

## Technology stack

| Layer | Technology |
|---|---|
| Language | Python |
| Source system | Google Forms API |
| Reporting layer | Google Sheets |
| Database | PostgreSQL |
| Transformation | dbt |
| Orchestration | GitHub Actions |
| Authentication | GCP Service Account |
| Dashboarding | Tableau Public |

---

## Repository structure

```text
Gym/
├── .github/workflows/
│   ├── Google_sheet_action.yml
│   └── actions.yml
├── gym_tracker_dbt/
│   ├── models/example/Staging/
│   ├── models/example/Gym_final/
│   ├── dbt_project.yml
│   └── profiles.yml
├── docs/
│   ├── architecture.md
│   ├── authentication.md
│   ├── dbt.md
│   ├── orchestration.md
│   ├── development-process.md
│   └── references.md
├── Gym Git.py
├── Gym to google sheets.py
├── requirements.txt
└── README.md
```

---

## Documentation

- [Architecture overview](docs/architecture.md)
- [Authentication and secrets management](docs/authentication.md)
- [dbt design and data quality](docs/dbt.md)
- [Workflow orchestration](docs/orchestration.md)
- [Development process](docs/development-process.md)
- [References](docs/references.md)

---

## Future enhancements

- Build the Tableau Public dashboard once more workout history has been collected
- Add additional workout KPIs such as volume, personal bests and progression trends
- Move PostgreSQL from a local environment to a cloud-hosted database
- Containerise the project with Docker
- Expand dbt tests and documentation
- Add alerting for failed workflow runs
