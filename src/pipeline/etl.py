
from pathlib import Path

import pandas as pd

from data_quality import validate_sales


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"


# --------------------------------------------------
# 2. EXTRACT
# --------------------------------------------------

def extract():
    """Extract source data from CSV files."""

    print("Starting data extraction...")

    customers = pd.read_csv(DATA_DIR / "customers.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")
    sales = pd.read_csv(DATA_DIR / "sales.csv")

    print(f"Customers extracted: {len(customers)}")
    print(f"Products extracted: {len(products)}")
    print(f"Sales extracted: {len(sales)}")

    return customers, products, sales


# --------------------------------------------------
# 3. TRANSFORM
# --------------------------------------------------

def transform(customers, products, sales):
    """Join datasets, enrich transactions and calculate revenue."""

    print("Starting data transformation...")

    # Join sales with customer information
    sales = sales.merge(
        customers,
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    # Join sales with product information
    sales = sales.merge(
        products,
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    # Calculate transaction revenue
    sales["total_amount"] = (
        sales["quantity"] * sales["unit_price"]
    ).round(2)

    # Remove records without customer or product information
    sales = sales.dropna(
        subset=["customer_name", "product_name"]
    )

    # Select final output columns
    sales = sales[
        [
            "transaction_id",
            "customer_id",
            "customer_name",
            "product_id",
            "product_name",
            "category",
            "quantity",
            "unit_price",
            "total_amount",
            "transaction_date",
            "city",
        ]
    ]

    print("Data transformation completed.")

    return sales


# --------------------------------------------------
# 4. DATA QUALITY VALIDATION
# --------------------------------------------------

def validate(sales):
    """Validate the transformed sales dataset."""

    print("Starting data quality validation...")

    validation_result = validate_sales(sales)

    print("Data quality validation passed.")
    print(f"Validation results: {validation_result}")

    return validation_result


# --------------------------------------------------
# 5. LOAD
# --------------------------------------------------

def load(sales):
    """Load validated data into processed storage."""

    print("Starting data loading...")

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = PROCESSED_DIR / "processed_sales.csv"

    sales.to_csv(
        output_file,
        index=False,
    )

    print("Data loading completed.")
    print(f"Output file: {output_file}")
    print(f"Records loaded: {len(sales)}")


# --------------------------------------------------
# 6. PIPELINE ORCHESTRATION
# --------------------------------------------------

def main():
    """Execute the complete ETL pipeline."""

    print("=" * 50)
    print("SALES ETL PIPELINE")
    print("=" * 50)

    try:
        # Extract
        customers, products, sales = extract()

        # Transform
        transformed_sales = transform(
            customers,
            products,
            sales,
        )

        # Validate
        validate(transformed_sales)

        # Load
        load(transformed_sales)

        print("=" * 50)
        print("ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 50)

    except Exception as error:
        print("=" * 50)
        print("ETL PIPELINE FAILED")
        print(f"Error: {error}")
        print("=" * 50)

        raise


# --------------------------------------------------
# 7. APPLICATION ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()
