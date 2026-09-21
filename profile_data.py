import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


def profile_dataset(file_name):

    print("\n" + "=" * 70)
    print(f"DATASET: {file_name}")
    print("=" * 70)

    file_path = RAW_DIR / file_name

    df = pd.read_csv(file_path)

    # Rows and columns
    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # Column names
    print("\n---------- Columns ----------")
    print(list(df.columns))

    # Data types
    print("\n---------- Data Types ----------")
    print(df.dtypes)

    # Missing values
    print("\n---------- Missing Values ----------")

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    if len(missing) == 0:
        print("No missing values")
    else:
        print(missing)

    # Duplicates
    print("\n---------- Duplicate Rows ----------")
    print(df.duplicated().sum())

    # First rows
    print("\n---------- First 5 Rows ----------")
    print(df.head())


def main():

    print("🚀 DATA PROFILING STARTED")

    files = [
        "customers.csv",
        "products.csv",
        "sales.csv"
    ]

    for file_name in files:
        profile_dataset(file_name)

    print("\n🎉 DATA PROFILING FINISHED")


if __name__ == "__main__":
    main()