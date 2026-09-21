import pandas as pd
from pathlib import Path


# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Input files
RAW_FILE = BASE_DIR / "data" / "raw" / "sales.csv"
CUSTOMERS_FILE = BASE_DIR / "data" / "clean" / "customers_clean.csv"
PRODUCTS_FILE = BASE_DIR / "data" / "clean" / "products_clean.csv"


# Output file
CLEAN_DIR = BASE_DIR / "data" / "clean"
CLEAN_FILE = CLEAN_DIR / "sales_clean.csv"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)


def transform_sales():

    print("========== Sales Transform Started ==========")

    # Read raw sales data
    df = pd.read_csv(RAW_FILE)

    print(f"Original Rows: {len(df):,}")

    # Remove duplicate records
    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print(f"Duplicates Removed: {before - after}")

    # Handle missing values
    before = len(df)

    df = df.dropna(subset=["OrderDate", "CustomerID"])

    after = len(df)

    print(f"Rows Removed Due to Missing Values: {before - after}")


    # Load reference data
    customers = pd.read_csv(CUSTOMERS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)

    # Validate CustomerID
    invalid_customers = ~df["CustomerID"].isin(
        customers["CustomerID"]
    )

    print(
        f"Invalid CustomerID Records: "
        f"{invalid_customers.sum()}"
    )

    # Validate ProductID
    invalid_products = ~df["ProductID"].isin(
        products["ProductID"]
    )

    print(
        f"Invalid ProductID Records: "
        f"{invalid_products.sum()}"
    )

    # Remove sales with invalid ProductID
    before = len(df)

    df = df[
        df["ProductID"].isin(products["ProductID"])
    ]

    after = len(df)

    print(
        f"Invalid ProductID Rows Removed: "
        f"{before - after}"
    )

    # Validate Quantity
    invalid_quantity = df[df["Quantity"] <= 0]

    print(
        f"Invalid Quantity Records: "
        f"{len(invalid_quantity)}"
    )

    if len(invalid_quantity) > 0:

        print("\n---------- Invalid Quantities ----------")

        print(
            invalid_quantity[
                ["SaleID", "ProductID", "Quantity"]
            ]
        )

    # Remove invalid quantities
    before = len(df)

    df = df[df["Quantity"] > 0]

    after = len(df)

    print(
        f"Invalid Quantity Rows Removed: "
        f"{before - after}"
    )

    # Convert OrderDate to datetime
    df["OrderDate"] = pd.to_datetime(
        df["OrderDate"],
        errors="coerce"
    )

    # Remove rows with invalid dates
    before = len(df)

    df = df.dropna(subset=["OrderDate"])

    after = len(df)

    print(
        f"Invalid Date Rows Removed: "
        f"{before - after}"
    )

    # Sort data by SaleID
    df = df.sort_values("SaleID")

    # Save clean data
    df.to_csv(
        CLEAN_FILE,
        index=False
    )

    print(f"Final Rows: {len(df):,}")

    print("\n========== Clean Data Preview ==========")
    print(df.head())

    print("\n========== Sales Transform Finished ==========")

    print("\nClean file saved to:")
    print(CLEAN_FILE)


if __name__ == "__main__":
    transform_sales()