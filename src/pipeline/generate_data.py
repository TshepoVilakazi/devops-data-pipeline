from pathlib import Path
import random
from datetime import datetime, timedelta

import pandas as pd


# Reproducibility: the same seed produces the same sample data
random.seed(42)

# Resolve the project root relative to this script
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)


def generate_customers(n=1000):
    customers = []

    for customer_id in range(1, n + 1):
        customers.append({
            "customer_id": customer_id,
            "customer_name": f"Customer_{customer_id}",
            "city": random.choice([
                "Johannesburg",
                "Cape Town",
                "Durban",
                "Pretoria",
                "Bloemfontein",
            ]),
            "signup_date": (
                datetime(2024, 1, 1)
                + timedelta(days=random.randint(0, 900))
            ).date(),
        })

    return pd.DataFrame(customers)


def generate_products(n=100):
    products = []

    categories = [
        "Electronics",
        "Furniture",
        "Clothing",
        "Food",
        "Books",
    ]

    for product_id in range(1, n + 1):
        products.append({
            "product_id": product_id,
            "product_name": f"Product_{product_id}",
            "category": random.choice(categories),
            "unit_price": round(random.uniform(50, 5000), 2),
        })

    return pd.DataFrame(products)


def generate_sales(n=10000, customers=1000, products=100):
    sales = []

    start_date = datetime(2025, 1, 1)

    for transaction_id in range(1, n + 1):
        sales.append({
            "transaction_id": transaction_id,
            "customer_id": random.randint(1, customers),
            "product_id": random.randint(1, products),
            "quantity": random.randint(1, 10),
            "transaction_date": (
                start_date
                + timedelta(days=random.randint(0, 364))
            ).date(),
        })

    return pd.DataFrame(sales)


def main():
    customers = generate_customers()
    products = generate_products()
    sales = generate_sales()

    customers.to_csv(DATA_DIR / "customers.csv", index=False)
    products.to_csv(DATA_DIR / "products.csv", index=False)
    sales.to_csv(DATA_DIR / "sales.csv", index=False)

    print("Data generation completed.")
    print(f"Customers generated: {len(customers)}")
    print(f"Products generated: {len(products)}")
    print(f"Sales generated: {len(sales)}")
    print(f"Output directory: {DATA_DIR}")


if __name__ == "__main__":
    main()