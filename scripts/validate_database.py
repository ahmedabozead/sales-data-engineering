import sqlite3
from pathlib import Path


# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / "database" / "sales.db"


def validate_database():
    print("========== Database Validation Started ==========")

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        # Enable foreign-key checks
        connection.execute("PRAGMA foreign_keys = ON")

        # Check tables
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        table_names = [table[0] for table in tables]

        print(f"Tables Found: {table_names}")

        expected_tables = {"customers", "products", "sales"}
        missing_tables = expected_tables - set(table_names)

        if missing_tables:
            print(f"Missing Tables: {missing_tables}")
        else:
            print("All required tables exist.")

        # Count rows
        customers_count = connection.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

        products_count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        sales_count = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

        print("\n========== Row Counts ==========")
        print(f"Customers Rows: {customers_count:,}")
        print(f"Products Rows: {products_count:,}")
        print(f"Sales Rows: {sales_count:,}")

        # Check duplicate primary keys
        duplicate_customers = connection.execute(
            """
            SELECT CustomerID, COUNT(*)
            FROM customers
            GROUP BY CustomerID
            HAVING COUNT(*) > 1
            """
        ).fetchall()

        duplicate_products = connection.execute(
            """
            SELECT ProductID, COUNT(*)
            FROM products
            GROUP BY ProductID
            HAVING COUNT(*) > 1
            """
        ).fetchall()

        duplicate_sales = connection.execute(
            """
            SELECT SaleID, COUNT(*)
            FROM sales
            GROUP BY SaleID
            HAVING COUNT(*) > 1
            """
        ).fetchall()

        print("\n========== Primary Key Validation ==========")
        print(f"Duplicate CustomerID: {len(duplicate_customers)}")
        print(f"Duplicate ProductID: {len(duplicate_products)}")
        print(f"Duplicate SaleID: {len(duplicate_sales)}")

        # Check orphan records
        invalid_customers = connection.execute(
            """
            SELECT COUNT(*)
            FROM sales AS s
            LEFT JOIN customers AS c
                ON s.CustomerID = c.CustomerID
            WHERE c.CustomerID IS NULL
            """
        ).fetchone()[0]

        invalid_products = connection.execute(
            """
            SELECT COUNT(*)
            FROM sales AS s
            LEFT JOIN products AS p
                ON s.ProductID = p.ProductID
            WHERE p.ProductID IS NULL
            """
        ).fetchone()[0]

        print("\n========== Relationship Validation ==========")
        print(f"Sales Without Customer: {invalid_customers}")
        print(f"Sales Without Product: {invalid_products}")

        # Check business rules
        invalid_quantity = connection.execute(
            """
            SELECT COUNT(*)
            FROM sales
            WHERE Quantity <= 0
            """
        ).fetchone()[0]

        missing_values = connection.execute(
            """
            SELECT COUNT(*)
            FROM sales
            WHERE SaleID IS NULL
               OR OrderDate IS NULL
               OR CustomerID IS NULL
               OR ProductID IS NULL
               OR Quantity IS NULL
            """
        ).fetchone()[0]

        print("\n========== Sales Rules Validation ==========")
        print(f"Invalid Quantity: {invalid_quantity}")
        print(f"Missing Sales Values: {missing_values}")

        # Final result
        validation_passed = (
            not missing_tables
            and customers_count == 1000
            and products_count == 98
            and sales_count == 9774
            and len(duplicate_customers) == 0
            and len(duplicate_products) == 0
            and len(duplicate_sales) == 0
            and invalid_customers == 0
            and invalid_products == 0
            and invalid_quantity == 0
            and missing_values == 0
        )

        print("\n========== Final Database Validation ==========")

        if validation_passed:
            print("Database Validation PASSED")
            print("Database is ready for the next pipeline stage.")
        else:
            print("Database Validation FAILED")
            print("Review the validation results above.")

    finally:
        connection.close()

    print("\n========== Database Validation Finished ==========")


if __name__ == "__main__":
    validate_database()
