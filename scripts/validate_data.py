import pandas as pd
from pathlib import Path


# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

CUSTOMERS_FILE = BASE_DIR / "data" / "clean" / "customers_clean.csv"
PRODUCTS_FILE = BASE_DIR / "data" / "clean" / "products_clean.csv"
SALES_FILE = BASE_DIR / "data" / "clean" / "sales_clean.csv"


def validate_table(df, table_name, id_column):
    print(f"\n========== {table_name} Validation ==========")

    print(f"Rows: {len(df):,}")
    print(f"Columns: {list(df.columns)}")

    # Missing values
    total_missing = df.isna().sum().sum()
    print(f"Missing Values: {total_missing}")

    if total_missing > 0:
        print("\nMissing Values by Column:")
        print(df.isna().sum()[df.isna().sum() > 0])

    # Duplicate full rows
    print(f"Duplicate Rows: {df.duplicated().sum()}")

    # Check ID column
    if id_column not in df.columns:
        print(f"ERROR: Column '{id_column}' does not exist")
        return

    print(f"Missing {id_column}: {df[id_column].isna().sum()}")
    print(f"Duplicate {id_column}: {df[id_column].duplicated().sum()}")

    # Display duplicate IDs if found
    duplicate_ids = df[
        df[id_column].duplicated(keep=False)
    ][id_column]

    if len(duplicate_ids) > 0:
        print(f"\nDuplicate {id_column} Values:")
        print(duplicate_ids.drop_duplicates().tolist())

    print(f"Unique {id_column}: {df[id_column].nunique():,}")


def validate_data():
    print("========== Full Data Validation Started ==========")

    # Read files
    customers = pd.read_csv(CUSTOMERS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)
    sales = pd.read_csv(SALES_FILE)

    # Validate individual tables
    validate_table(
        customers,
        "Customers",
        "CustomerID"
    )

    validate_table(
        products,
        "Products",
        "ProductID"
    )

    validate_table(
        sales,
        "Sales",
        "SaleID"
    )

    # Validate sales foreign keys
    print("\n========== Relationship Validation ==========")

    invalid_customer_ids = ~sales["CustomerID"].isin(
        customers["CustomerID"]
    )

    invalid_product_ids = ~sales["ProductID"].isin(
        products["ProductID"]
    )

    print(
        f"Sales with Invalid CustomerID: "
        f"{invalid_customer_ids.sum()}"
    )

    print(
        f"Sales with Invalid ProductID: "
        f"{invalid_product_ids.sum()}"
    )

    # Validate sales-specific rules
    print("\n========== Sales Rules Validation ==========")

    sales["OrderDate"] = pd.to_datetime(
        sales["OrderDate"],
        errors="coerce"
    )

    print(f"Invalid OrderDate: {sales['OrderDate'].isna().sum()}")
    print(f"Invalid Quantity: {(sales['Quantity'] <= 0).sum()}")
    print(f"Missing Quantity: {sales['Quantity'].isna().sum()}")

    # Final result
    all_checks = [
        customers.isna().sum().sum() == 0,
        customers.duplicated().sum() == 0,
        customers["CustomerID"].notna().all(),
        customers["CustomerID"].is_unique,

        products.isna().sum().sum() == 0,
        products.duplicated().sum() == 0,
        products["ProductID"].notna().all(),
        products["ProductID"].is_unique,

        sales.isna().sum().sum() == 0,
        sales.duplicated().sum() == 0,
        sales["SaleID"].is_unique,

        invalid_customer_ids.sum() == 0,
        invalid_product_ids.sum() == 0,
        sales["OrderDate"].notna().all(),
        (sales["Quantity"] > 0).all(),
    ]

    print("\n========== Final Validation Result ==========")

    if all(all_checks):
        print("Validation PASSED")
        print("All tables are clean and relationships are valid.")
    else:
        print("Validation FAILED")
        print("There are still data-quality issues to review.")

    print("\n========== Full Data Validation Finished ==========")


if __name__ == "__main__":
    validate_data()
