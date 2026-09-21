import pyodbc


connection_string = (
    "DRIVER={SQL Server};"
    "SERVER=localhost;"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
)


def create_database():
    connection = pyodbc.connect(connection_string)
    connection.autocommit = True

    try:
        database_exists = connection.execute(
            """
            SELECT DB_ID('SalesDW')
            """
        ).fetchone()[0]

        if database_exists is None:
            connection.execute(
                "CREATE DATABASE SalesDW"
            )
            print("Database SalesDW created successfully.")
        else:
            print("Database SalesDW already exists.")

    finally:
        connection.close()


if __name__ == "__main__":
    create_database()
