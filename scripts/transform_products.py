import pandas as pd
from pathlib import Path


# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "products.csv"
CLEAN_DIR = BASE_DIR / "data" / "clean"
CLEAN_FILE = CLEAN_DIR / "products_clean.csv"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# TRANSFORM
# ==========================================

def transform_products():

    print("========== Products Transform Started ==========")

    # Read raw data
    df = pd.read_csv(RAW_FILE)

    print(f"Original Rows: {len(df):,}")


    # ==========================================
    # 1. Remove duplicates
    # ==========================================

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print(f"Duplicates Removed: {before - after}")


    # ==========================================
    # 2. Clean ProductName
    # ==========================================

    df["ProductName"] = df["ProductName"].str.strip()


    # ==========================================
    # 3. Standardize Category
    # ==========================================

    df["Category"] = df["Category"].str.strip().str.title()


    # ==========================================
    # 4. Validate Price
    # ==========================================

    df["Price"] = pd.to_numeric(
        df["Price"],
        errors="coerce"
    )

    # Remove invalid prices
    df = df[df["Price"] > 0]


    # ==========================================
    # 5. Sort by ProductID
    # ==========================================

    df = df.sort_values("ProductID")


    # ==========================================
    # 6. Save Clean Data
    # ==========================================

    df.to_csv(
        CLEAN_FILE,
        index=False
    )


    print(f"Final Rows: {len(df):,}")

    print("\n========== Clean Data Preview ==========")

    print(df.head())

    print("\n========== Products Transform Finished ==========")

    print("\nClean file saved to:")
    print(CLEAN_FILE)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    transform_products()