# Financial Management Dashboard

An internal financial dashboard built in Python (Dash + SQLAlchemy) that gives stakeholders a real-time, centralized view of expenses by cost center — replacing manual spreadsheet consolidation with role-based, self-service reporting.

## Features

- Role-based login: each cost center sees only its own data; an admin profile has consolidated access across all cost centers
- Dynamic filtering by year and month
- Automatic KPI summaries: total spend, number of entries, and monthly average
- Detailed expense breakdown by cost center, account, and description
- One-click export to Excel

## Tech stack

- **Python**
- **Dash** (analytics web application framework)
- **SQLAlchemy** (ORM / database connection)
- **Pandas** (data processing and transformation)
- **SQL Server** (data source, via ODBC Driver 18)

## Project structure

```
app.py                     # Application entry point
layout.py                  # Root layout
colunas.py                 # Column/field definitions
config/
  database.py              # Database engine configuration
services/
  auth_service.py          # Authentication and access control
  despesas_service.py      # Expense data retrieval and aggregation
layouts/
  login.py                 # Login screen layout
  main_layout.py           # Main dashboard layout
callbacks/
  login.py                 # Login callback logic
  filtros.py                # Year/month filter callbacks
  filtro_cc.py              # Cost-center filter callback
  kpis.py                   # KPI card callbacks
  tabela.py                 # Expense table callbacks
```

## Setup

This project **contains no hardcoded credentials**. All sensitive configuration is loaded from environment variables.

1. Copy `.env.example` to `.env` and fill in the real values (database connection, admin credentials, per-cost-center passwords).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

⚠️ The `.env` file should never be committed — it's already listed in `.gitignore`.

## Background

This project was built to replace a recurring, manual process: compiling and distributing cost-center expense reports by hand. It gives each department direct, secure, real-time access to its own numbers, while giving finance/admin a consolidated view across the whole organization.
