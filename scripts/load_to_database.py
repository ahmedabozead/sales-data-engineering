import sqlite3
from pathlib import Path

import pandas as pd


# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input files
CUSTOMERS_FILE = BASE_DIR / "data" / "clean" / "customers_clean.csv"
PRODUCTS_FILE = BASE_DIR / "data" / "clean" / "products_clean.csv"
SALES_FILE = BASE_DIR / "data" / "clean" / "sales_clean.csv"

# Database file
DATABASE_DIR = BASE_DIR / "database"
DATABASE_FILE = DATABASE_DIR / "sales.db"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)


def load_to_database():
    print("========== Database Load Started ==========")

    # Read clean files
    customers = pd.read_csv(CUSTOMERS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)
    sales = pd.read_csv(SALES_FILE)

    # Ensure correct data types
    customers["CustomerID"] = customers["CustomerID"].astype("int64")
    products["ProductID"] = products["ProductID"].astype("int64")

    sales["SaleID"] = sales["SaleID"].astype("int64")
    sales["CustomerID"] = sales["CustomerID"].astype("int64")
    sales["ProductID"] = sales["ProductID"].astype("int64")
    sales["Quantity"] = sales["Quantity"].astype("int64")

    sales["OrderDate"] = pd.to_datetime(
        sales["OrderDate"],
        errors="raise"
    ).dt.strftime("%Y-%m-%d")

    # Connect to SQLite
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        # Enable foreign-key enforcement
        connection.execute("PRAGMA foreign_keys = ON")

        # Recreate tables for the first full load
        connection.executescript(
            """
            DROP TABLE IF EXISTS sales;
            DROP TABLE IF EXISTS products;
            DROP TABLE IF EXISTS customers;

            CREATE TABLE customers (
                CustomerID INTEGER PRIMARY KEY,
                CustomerName TEXT NOT NULL,
                City TEXT NOT NULL,
                Country TEXT NOT NULL
            );

            CREATE TABLE products (
                ProductID INTEGER PRIMARY KEY,
                ProductName TEXT NOT NULL,
                Category TEXT NOT NULL,
                Price REAL NOT NULL
            );

            CREATE TABLE sales (
                SaleID INTEGER PRIMARY KEY,
                OrderDate TEXT NOT NULL,
                CustomerID INTEGER NOT NULL,
                ProductID INTEGER NOT NULL,
                Quantity INTEGER NOT NULL CHECK (Quantity > 0),

                FOREIGN KEY (CustomerID)
                    REFERENCES customers(CustomerID),

                FOREIGN KEY (ProductID)
                    REFERENCES products(ProductID)
            );
            """
        )

        # Load data into database tables
        customers.to_sql(
            "customers",
            connection,
            if_exists="append",
            index=False
        )

        products.to_sql(
            "products",
            connection,
            if_exists="append",
            index=False
        )

        sales.to_sql(
            "sales",
            connection,
            if_exists="append",
            index=False
        )

        # Verify loaded row counts
        customers_count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

        products_count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        sales_count = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

        print("\n========== Load Summary ==========")
        print(f"Customers Loaded: {customers_count:,}")
        print(f"Products Loaded: {products_count:,}")
        print(f"Sales Loaded: {sales_count:,}")

        print("\nDatabase file saved to:")
        print(DATABASE_FILE)

    finally:
        connection.close()

    print("\n========== Database Load Finished ==========")


if __name__ == "__main__":
    load_to_database()
