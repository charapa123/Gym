# Development Process

## Overview

This project uses a lightweight branch-based development workflow.

The objective is to separate active development from stable code and reduce the chance of breaking working pipelines.

---

## Branch strategy

The development process follows this pattern:

```text
Development branch → Testing → Pull request → Main branch
```

New functionality and documentation changes are developed away from the stable branch before being merged.

---

## Validation before merge

Changes are validated before being merged into the main branch.

Validation may include:

- Running Python scripts locally
- Running GitHub Actions workflows manually
- Confirming PostgreSQL loads complete successfully
- Running `dbt debug`
- Running `dbt build`
- Reviewing dbt test results
- Checking generated documentation and diagrams

---

## Pull requests

Pull requests are used to merge changes into the stable branch.

This provides:

- Clear change history
- A controlled merge point
- Easier review of documentation and code changes
- Lower risk of breaking the public repository

---

## Main branch

The main branch represents the stable project state.

The README, documentation, workflows and dbt project should remain usable from this branch.

---

## Lessons learned

Using a branch workflow in a personal project adds structure and reduces accidental breakages.

It also mirrors the type of workflow commonly used in professional software and data engineering teams.
