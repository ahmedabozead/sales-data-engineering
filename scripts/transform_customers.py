import pandas as pd
from pathlib import Path


# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "customers.csv"
CLEAN_DIR = BASE_DIR / "data" / "clean"
CLEAN_FILE = CLEAN_DIR / "customers_clean.csv"


# Create clean folder if it doesn't exist
CLEAN_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# TRANSFORM
# ==========================================

def transform_customers():

    print("========== Customers Transform Started ==========")

    # Read raw data
    df = pd.read_csv(RAW_FILE)

    print(f"Original Rows: {len(df):,}")


    # ==========================================
    # 1. Remove duplicate rows
    # ==========================================

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print(f"Duplicates Removed: {before - after}")


    # ==========================================
    # 2. Clean CustomerName
    # ==========================================

    df["CustomerName"] = df["CustomerName"].fillna("Unknown Customer")

    df["CustomerName"] = df["CustomerName"].str.strip()


    # ==========================================
    # 3. Clean City
    # ==========================================

    df["City"] = df["City"].fillna("Unknown")

    df["City"] = df["City"].str.strip()

    df["City"] = df["City"].str.title()


    # ==========================================
    # 4. Clean Country
    # ==========================================

    df["Country"] = df["Country"].str.strip()

    df["Country"] = df["Country"].str.title()


    # ==========================================
    # 5. Check CustomerID
    # ==========================================

    df["CustomerID"] = pd.to_numeric(
        df["CustomerID"],
        errors="coerce"
    )

    df = df.dropna(subset=["CustomerID"])

    df["CustomerID"] = df["CustomerID"].astype(int)


    # ==========================================
    # 6. Sort by CustomerID
    # ==========================================

    df = df.sort_values("CustomerID")


    # ==========================================
    # 7. Save Clean Data
    # ==========================================

    df.to_csv(
        CLEAN_FILE,
        index=False
    )


    print(f"Final Rows: {len(df):,}")

    print("\n========== Clean Data Preview ==========")

    print(df.head())

    print("\n========== Customers Transform Finished ==========")

    print(f"\nClean file saved to:")
    print(CLEAN_FILE)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    transform_customers()