import pyodbc


CONNECTION_STRING = (
    "DRIVER={SQL Server};"
    "SERVER=localhost;"
    "DATABASE=SalesDW;"
    "Trusted_Connection=yes;"
)


def validate_sqlserver():
    print("========== SQL Server Validation Started ==========")

    connection = pyodbc.connect(CONNECTION_STRING)

    try:
        cursor = connection.cursor()

        # Check tables
        tables = cursor.execute(
            """
            SELECT TABLE_SCHEMA, TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
              AND TABLE_SCHEMA = 'dbo'
            ORDER BY TABLE_NAME
            """
        ).fetchall()

        print("\n========== Tables ==========")
        for schema, table in tables:
            print(f"{schema}.{table}")

        # Row counts
        customers_count = cursor.execute(
            "SELECT COUNT(*) FROM dbo.Customers"
        ).fetchone()[0]

        products_count = cursor.execute(
            "SELECT COUNT(*) FROM dbo.Products"
        ).fetchone()[0]

        sales_count = cursor.execute(
            "SELECT COUNT(*) FROM dbo.Sales"
        ).fetchone()[0]

        print("\n========== Row Counts ==========")
        print(f"Customers: {customers_count:,}")
        print(f"Products: {products_count:,}")
        print(f"Sales: {sales_count:,}")

        # Duplicate primary keys
        duplicate_customers = cursor.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT CustomerID
                FROM dbo.Customers
                GROUP BY CustomerID
                HAVING COUNT(*) > 1
            ) AS duplicates
            """
        ).fetchone()[0]

        duplicate_products = cursor.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT ProductID
                FROM dbo.Products
                GROUP BY ProductID
                HAVING COUNT(*) > 1
            ) AS duplicates
            """
        ).fetchone()[0]

        duplicate_sales = cursor.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT SaleID
                FROM dbo.Sales
                GROUP BY SaleID
                HAVING COUNT(*) > 1
            ) AS duplicates
            """
        ).fetchone()[0]

        print("\n========== Primary Key Validation ==========")
        print(f"Duplicate CustomerID: {duplicate_customers}")
        print(f"Duplicate ProductID: {duplicate_products}")
        print(f"Duplicate SaleID: {duplicate_sales}")

        # Foreign-key relationships
        invalid_customers = cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.Sales AS s
            LEFT JOIN dbo.Customers AS c
                ON s.CustomerID = c.CustomerID
            WHERE c.CustomerID IS NULL
            """
        ).fetchone()[0]

        invalid_products = cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.Sales AS s
            LEFT JOIN dbo.Products AS p
                ON s.ProductID = p.ProductID
            WHERE p.ProductID IS NULL
            """
        ).fetchone()[0]

        print("\n========== Relationship Validation ==========")
        print(f"Sales Without Customer: {invalid_customers}")
        print(f"Sales Without Product: {invalid_products}")

        # Sales rules
        invalid_quantity = cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.Sales
            WHERE Quantity <= 0
            """
        ).fetchone()[0]

        missing_values = cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.Sales
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

        validation_passed = (
            customers_count == 1000
            and products_count == 98
            and sales_count == 9774
            and duplicate_customers == 0
            and duplicate_products == 0
            and duplicate_sales == 0
            and invalid_customers == 0
            and invalid_products == 0
            and invalid_quantity == 0
            and missing_values == 0
        )

        print("\n========== Final SQL Server Validation ==========")

        if validation_passed:
            print("SQL Server Validation PASSED")
            print("SalesDW is valid and ready.")
        else:
            print("SQL Server Validation FAILED")
            print("Review the results above.")

    finally:
        connection.close()

    print("\n========== SQL Server Validation Finished ==========")


if __name__ == "__main__":
    validate_sqlserver()
