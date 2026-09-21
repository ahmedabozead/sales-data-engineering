import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

DATA_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)


# ==========================================
# 1. CUSTOMERS
# ==========================================

customers = []

cities = [
    "Cairo",
    "cairo",
    " Cairo ",
    "Giza",
    "Alexandria",
    "alexandria"
]

for i in range(1, 1001):

    customers.append({
        "CustomerID": i,
        "CustomerName": f"Customer_{i}",
        "City": random.choice(cities),
        "Country": "Egypt"
    })

customers_df = pd.DataFrame(customers)

# Add missing values
customers_df.loc[10, "City"] = None
customers_df.loc[25, "CustomerName"] = None

# Add duplicate rows
customers_df = pd.concat(
    [customers_df, customers_df.iloc[[10, 20]]],
    ignore_index=True
)

customers_df.to_csv(
    DATA_DIR / "customers.csv",
    index=False
)


# ==========================================
# 2. PRODUCTS
# ==========================================

products = []

categories = [
    "Laptop",
    "Mouse",
    "Keyboard",
    "Monitor",
    "Headphones"
]

for i in range(1, 101):

    price = round(random.uniform(100, 20000), 2)

    products.append({
        "ProductID": i,
        "ProductName": f"Product_{i}",
        "Category": random.choice(categories),
        "Price": price
    })

products_df = pd.DataFrame(products)

# Add invalid prices
products_df.loc[5, "Price"] = -500
products_df.loc[15, "Price"] = 0

# Add duplicate
products_df = pd.concat(
    [products_df, products_df.iloc[[5]]],
    ignore_index=True
)

products_df.to_csv(
    DATA_DIR / "products.csv",
    index=False
)


# ==========================================
# 3. SALES
# ==========================================

sales = []

start_date = datetime(2026, 1, 1)

for i in range(1, 10001):

    order_date = start_date + timedelta(
        days=random.randint(0, 240)
    )

    quantity = random.randint(1, 10)

    sales.append({
        "SaleID": i,
        "OrderDate": order_date.strftime("%Y-%m-%d"),
        "CustomerID": random.randint(1, 1000),
        "ProductID": random.randint(1, 100),
        "Quantity": quantity
    })

sales_df = pd.DataFrame(sales)

# Different date format
sales_df.loc[10, "OrderDate"] = "15/03/2026"
sales_df.loc[20, "OrderDate"] = "2026/04/20"

# Missing date
sales_df.loc[30, "OrderDate"] = None

# Invalid quantity
sales_df.loc[40, "Quantity"] = -3
sales_df.loc[50, "Quantity"] = 0

# Missing CustomerID
sales_df.loc[60, "CustomerID"] = None

# Duplicate sales
sales_df = pd.concat(
    [sales_df, sales_df.iloc[[100, 200, 300]]],
    ignore_index=True
)

sales_df.to_csv(
    DATA_DIR / "sales.csv",
    index=False
)


print("====================================")
print("✅ DATA GENERATION COMPLETED")
print("====================================")

print(f"Customers: {len(customers_df):,}")
print(f"Products: {len(products_df):,}")
print(f"Sales: {len(sales_df):,}")

print("\nFiles saved in:")
print(DATA_DIR)