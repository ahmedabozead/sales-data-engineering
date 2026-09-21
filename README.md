# Sales Data Engineering ETL Pipeline

An end-to-end batch **Extract, Transform, Load (ETL)** pipeline for sales data engineering. The project uses Python and Pandas to generate or ingest CSV data, apply data-quality rules, validate business constraints, and load the curated datasets into SQLite or Microsoft SQL Server.

The repository is designed as a practical portfolio project that demonstrates a complete data pipeline rather than a single transformation script.

## Project Overview

The pipeline processes three related entities:

- **Customers** — customer master data.
- **Products** — product master data.
- **Sales** — transactional order data linked to customers and products.

The transformation layer produces curated CSV files that can be validated independently or loaded into a relational database. The SQL Server path creates normalized tables with primary keys, foreign keys, `NOT NULL` constraints, and business-rule checks.

## Architecture

```text
Raw CSV files
      |
      v
Pandas transformations
      |
      v
Curated CSV files
      |
      v
Data-quality validation
      |
      +----------------------+
      |                      |
      v                      v
SQLite database       SQL Server database
      |                      |
      +----------+-----------+
                 v
       Database validation and logs
```

## Data-Quality Rules

The sales transformation applies the following controls:

1. Removes duplicate records.
2. Removes rows with required missing values.
3. Verifies that each `CustomerID` exists in the customer master data.
4. Verifies that each `ProductID` exists in the product master data.
5. Removes records with non-positive quantities.
6. Parses `OrderDate` and removes invalid dates.
7. Writes the cleaned dataset to `data/clean/sales_clean.csv`.

The validation scripts also check missing values, duplicate keys, orphan records, and core business rules after transformation.

## Pipeline Results

The current synthetic sales dataset contains **10,003 source rows**. After the quality rules are applied, the resulting curated file contains **9,774 valid rows**.

| Quality check | Rows affected |
|---|---:|
| Duplicate records removed | 3 |
| Rows removed for missing values | 2 |
| Invalid product references removed | 220 |
| Invalid quantities removed | 2 |
| Invalid dates removed | 2 |
| Final curated sales rows | **9,774** |

## Repository Structure

```text
sales-data-engineering/
├── data/
│   ├── raw/                         # Source CSV datasets
│   └── clean/                       # Curated datasets produced by transformations
├── scripts/
│   ├── generate_data.py             # Generates the synthetic source data
│   ├── transform_customers.py       # Cleans customer data
│   ├── transform_products.py        # Cleans product data
│   ├── transform_sales.py           # Cleans and validates sales data
│   ├── validate_data.py             # Validates curated CSV files
│   ├── load_to_database.py          # Loads curated data into SQLite
│   ├── validate_database.py         # Validates the SQLite database
│   ├── create_sqlserver_database.py # Creates the SQL Server target database
│   ├── load_to_sqlserver.py         # Loads curated data into SQL Server
│   ├── validate_sqlserver.py        # Validates the SQL Server database
│   ├── run_pipeline.py              # Orchestrates the SQL Server pipeline
│   └── profile_data.py              # Profiles the source and curated data
├── database/                        # Local database artifacts; ignored by Git
├── logs/                            # Runtime logs; ignored by Git
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python **3.10 or later**
- Pandas
- `pyodbc` when using the SQL Server scripts
- Microsoft SQL Server and a compatible ODBC driver when using the SQL Server path

SQLite is included with Python and does not require a separate database server.

## Installation

Create and activate a virtual environment from the repository root:

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

### 1. Generate source data (optional)

Use this step only when you want to regenerate the synthetic input files:

```bash
python scripts/generate_data.py
```

### 2. Run the transformations

```bash
python scripts/transform_customers.py
python scripts/transform_products.py
python scripts/transform_sales.py
```

### 3. Validate the curated CSV files

```bash
python scripts/validate_data.py
```

### 4. Load and validate SQLite

```bash
python scripts/load_to_database.py
python scripts/validate_database.py
```

The SQLite database is created at `database/sales.db`. This generated artifact is intentionally excluded from version control.

### 5. Run the SQL Server pipeline

Before running these commands, confirm that SQL Server is available on the local machine and that the required ODBC driver is installed.

```bash
python scripts/create_sqlserver_database.py
python scripts/run_pipeline.py
```

The orchestrated pipeline executes the transformation, validation, SQL Server loading, and SQL Server validation stages. Runtime output is written to `logs/pipeline.log`.

## Design Notes

The transformation scripts resolve paths relative to the repository root. They can therefore be executed from any working directory as long as the repository structure remains unchanged.

The repository contains synthetic sample data for demonstration purposes. Do not commit production data, credentials, connection strings, local database files, or runtime logs. The included `.gitignore` excludes virtual environments, generated database files, logs, and local configuration files.

## Future Enhancements

Potential next steps include adding automated tests with `pytest`, introducing a configuration file for database connections, adding incremental loading by date, creating a dimensional warehouse model, and publishing KPI dashboards for revenue and quantity analysis.

## License

No license has been specified yet. Add a `LICENSE` file before distributing or reusing this project publicly.

## References

[1]: https://docs.python.org/3/library/venv.html "Python virtual environments"
[2]: https://pandas.pydata.org/docs/ "Pandas documentation"
[3]: https://docs.python.org/3/library/sqlite3.html "Python SQLite interface"
[4]: https://github.com/mkleehammer/pyodbc "pyodbc project"
