import pyodbc


connection_string = (
    "DRIVER={SQL Server};"
    "SERVER=localhost;"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
)


try:
    connection = pyodbc.connect(connection_string)

    result = connection.execute(
        "SELECT @@SERVERNAME, DB_NAME()"
    ).fetchone()

    print("Connection successful")
    print(f"Server: {result[0]}")
    print(f"Database: {result[1]}")

    connection.close()

except Exception as error:
    print("Connection failed")
    print(error)
