import pyodbc
import pandas as pd
from pathlib import Path


# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

CUSTOMERS_FILE = BASE_DIR / "data" / "clean" / "customers_clean.csv"
PRODUCTS_FILE = BASE_DIR / "data" / "clean" / "products_clean.csv"
SALES_FILE = BASE_DIR / "data" / "clean" / "sales_clean.csv"


CONNECTION_STRING = (
    "DRIVER={SQL Server};"
    "SERVER=localhost;"
    "DATABASE=SalesDW;"
    "Trusted_Connection=yes;"
)


def load_to_sqlserver():
    print("========== SQL Server Load Started ==========")

    customers = pd.read_csv(CUSTOMERS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)
    sales = pd.read_csv(SALES_FILE)

    # Ensure correct data types
    customers["CustomerID"] = customers["CustomerID"].astype(int)

    products["ProductID"] = products["ProductID"].astype(int)
    products["Price"] = products["Price"].astype(float)

    sales["SaleID"] = sales["SaleID"].astype(int)
    sales["CustomerID"] = sales["CustomerID"].astype(int)
    sales["ProductID"] = sales["ProductID"].astype(int)
    sales["Quantity"] = sales["Quantity"].astype(int)

    sales["OrderDate"] = pd.to_datetime(
        sales["OrderDate"],
        errors="raise"
    ).dt.date

    connection = pyodbc.connect(CONNECTION_STRING)

    try:
        cursor = connection.cursor()
        cursor.fast_executemany = True

        # Recreate tables for a full load
        cursor.execute("""
            IF OBJECT_ID('dbo.Sales', 'U') IS NOT NULL
                DROP TABLE dbo.Sales;

            IF OBJECT_ID('dbo.Products', 'U') IS NOT NULL
                DROP TABLE dbo.Products;

            IF OBJECT_ID('dbo.Customers', 'U') IS NOT NULL
                DROP TABLE dbo.Customers;
        """)

        cursor.execute("""
            CREATE TABLE dbo.Customers (
                CustomerID INT NOT NULL PRIMARY KEY,
                CustomerName NVARCHAR(100) NOT NULL,
                City NVARCHAR(100) NOT NULL,
                Country NVARCHAR(100) NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE dbo.Products (
                ProductID INT NOT NULL PRIMARY KEY,
                ProductName NVARCHAR(100) NOT NULL,
                Category NVARCHAR(100) NOT NULL,
                Price DECIMAL(18, 2) NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE dbo.Sales (
                SaleID INT NOT NULL PRIMARY KEY,
                OrderDate DATE NOT NULL,
                CustomerID INT NOT NULL,
                ProductID INT NOT NULL,
                Quantity INT NOT NULL,

                CONSTRAINT CK_Sales_Quantity
                    CHECK (Quantity > 0),

                CONSTRAINT FK_Sales_Customers
                    FOREIGN KEY (CustomerID)
                    REFERENCES dbo.Customers(CustomerID),

                CONSTRAINT FK_Sales_Products
                    FOREIGN KEY (ProductID)
                    REFERENCES dbo.Products(ProductID)
            );
        """)

        # Load customers
        customer_rows = list(
            customers[
                [
                    "CustomerID",
                    "CustomerName",
                    "City",
                    "Country",
                ]
            ].itertuples(index=False, name=None)
        )

        cursor.executemany(
            """
            INSERT INTO dbo.Customers
            (
                CustomerID,
                CustomerName,
                City,
                Country
            )
            VALUES (?, ?, ?, ?)
            """,
            customer_rows,
        )

        # Load products
        product_rows = list(
            products[
                [
                    "ProductID",
                    "ProductName",
                    "Category",
                    "Price",
                ]
            ].itertuples(index=False, name=None)
        )

        cursor.executemany(
            """
            INSERT INTO dbo.Products
            (
                ProductID,
                ProductName,
                Category,
                Price
            )
            VALUES (?, ?, ?, ?)
            """,
            product_rows,
        )

        # Load sales
        sales_rows = list(
            sales[
                [
                    "SaleID",
                    "OrderDate",
                    "CustomerID",
                    "ProductID",
                    "Quantity",
                ]
            ].itertuples(index=False, name=None)
        )

        cursor.executemany(
            """
            INSERT INTO dbo.Sales
            (
                SaleID,
                OrderDate,
                CustomerID,
                ProductID,
                Quantity
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            sales_rows,
        )

        connection.commit()

        # Verify loaded row counts
        customers_count = cursor.execute(
            "SELECT COUNT(*) FROM dbo.Customers"
        ).fetchone()[0]

        products_count = cursor.execute(
            "SELECT COUNT(*) FROM dbo.Products"
        ).fetchone()[0]

        sales_count = cursor.execute(
            "SELECT COUNT(*) FROM dbo.Sales"
        ).fetchone()[0]

        print("\n========== SQL Server Load Summary ==========")
        print(f"Customers Loaded: {customers_count:,}")
        print(f"Products Loaded: {products_count:,}")
        print(f"Sales Loaded: {sales_count:,}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    print("\nDatabase: SalesDW")
    print("Schema: dbo")
    print("\n========== SQL Server Load Finished ==========")


if __name__ == "__main__":
    load_to_sqlserver()
