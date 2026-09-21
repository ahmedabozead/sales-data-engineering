# Sales Data Engineering ETL Pipeline

An end-to-end batch ETL pipeline built with **Python, Pandas, and Microsoft SQL Server**. The project extracts synthetic customer, product, and sales CSV files, applies data-quality transformations, validates the cleaned datasets, loads them into a normalized SQL Server database, and validates the database load.

## Architecture

```text
Raw CSV files
    ↓
Transform with Pandas
    ↓
Clean CSV files
    ↓
Data-quality validation
    ↓
Load into SQL Server (SalesDW)
    ↓
SQL Server validation
    ↓
Pipeline logging and orchestration
```

## Implemented Features

- Removes duplicate records and required-field nulls.
- Validates customer and product reference keys.
- Removes invalid product references and non-positive quantities.
- Parses and validates order dates.
- Loads normalized `Customers`, `Products`, and `Sales` tables into SQL Server.
- Applies primary keys, foreign keys, `NOT NULL` constraints, and a `Quantity > 0` check constraint.
- Validates row counts, duplicate keys, missing values, orphan records, and business rules.
- Orchestrates the full pipeline with `subprocess` and writes execution logs.

## Pipeline Results

The current synthetic dataset successfully loads:

| Table | Rows |
|---|---:|
| `dbo.Customers` | 1,000 |
| `dbo.Products` | 98 |
| `dbo.Sales` | 9,774 |

## Project Structure

```text
Sales_Data_Engineering/
├── data/
│   ├── raw/                         # Synthetic source CSV files
│   └── clean/                       # Transformed CSV files
├── scripts/
│   ├── generate_data.py
│   ├── transform_customers.py
│   ├── transform_products.py
│   ├── transform_sales.py
│   ├── validate_data.py
│   ├── create_sqlserver_database.py
│   ├── load_to_sqlserver.py
│   ├── validate_sqlserver.py
│   ├── run_pipeline.py
│   └── test_sqlserver_connection.py
├── database/                        # Local database artifacts; ignored by Git
├── logs/                            # Runtime logs; ignored by Git
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Windows 10/11
- Python 3.11+
- Microsoft SQL Server (the project uses the default local instance `localhost`)
- SQL Server ODBC driver exposed as `SQL Server`
- Windows Authentication enabled for the SQL Server user running the pipeline

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Setup

1. Confirm that SQL Server is running.
2. Create the target database:

   ```powershell
   python scripts\create_sqlserver_database.py
   ```

3. Run the complete pipeline:

   ```powershell
   python scripts\run_pipeline.py
   ```

The pipeline runs these stages in order:

```text
transform_customers.py
transform_products.py
transform_sales.py
validate_data.py
load_to_sqlserver.py
validate_sqlserver.py
```

## Useful Commands

Run the source transformations individually:

```powershell
python scripts\transform_customers.py
python scripts\transform_products.py
python scripts\transform_sales.py
```

Validate the cleaned CSV datasets:

```powershell
python scripts\validate_data.py
```

Load and validate SQL Server directly:

```powershell
python scripts\load_to_sqlserver.py
python scripts\validate_sqlserver.py
```

## SQL Server Objects

The pipeline creates these tables in the `SalesDW` database:

- `dbo.Customers(CustomerID PRIMARY KEY)`
- `dbo.Products(ProductID PRIMARY KEY)`
- `dbo.Sales(SaleID PRIMARY KEY, CustomerID FOREIGN KEY, ProductID FOREIGN KEY)`

The current loader performs a full load by recreating the three target tables on each run. Incremental loading and scheduling are future enhancements.

## Notes

The included data is synthetic and intended for learning and portfolio demonstration. Do not commit real customer data, credentials, local virtual environments, generated database files, or runtime logs.
