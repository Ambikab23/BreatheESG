# Breathe ESG Tech Intern Assignment

A Django REST + React prototype for ESG data ingestion, normalization, analyst review, and approval workflow.

## Features

- Upload CSV files
- Select source type: SAP, Utility, Travel
- Normalize uploaded records
- Categorize into Scope 1, Scope 2, Scope 3
- Detect suspicious records
- Analyst review dashboard
- Approve records
- Lock approved records for audit
- Maintain audit log

## Tech Stack

- Backend: Django
- Frontend: React
- Database: SQLite
- Data Processing: Pandas

## Run Backend

```bash
cd backend
source venv/bin/activate
python manage.py runserver