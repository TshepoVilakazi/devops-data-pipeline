
import logging
from pathlib import Path

import pandas as pd

from data_quality import validate_sales


# ==================================================
# PROJECT CONFIGURATION
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"


# ==================================================
# LOGGING CONFIGURATION
# ==================================================

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "etl.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


# ==================================================
# EXTRACT
# ==================================================

def extract():

    logger.info("Starting data extraction...")

    customers = pd.read_csv(DATA_DIR / "customers.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")
    sales = pd.read_csv(DATA_DIR / "sales.csv")

    logger.info("Customers extracted: %s", len(customers))
    logger.info("Products extracted: %s", len(products))
    logger.info("Sales extracted: %s", len(sales))

    return customers, products, sales


# ==================================================
# TRANSFORM
# ==================================================

def transform(customers, products, sales):

    logger.info("Starting data transformation...")

    # Join sales with customer information
    transformed = sales.merge(
        customers[["customer_id", "customer_name", "city"]],
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    # Join sales with product information
    transformed = transformed.merge(
        products[["product_id", "product_name", "unit_price"]],
        on="product_id",
        how="left",
        validate="many_to_one"
    )

    # Calculate transaction revenue
    transformed["total_amount"] = (
        transformed["quantity"] * transformed["unit_price"]
    ).round(2)

    # Remove records without customer or product information
    transformed = transformed.dropna(
        subset=["customer_name", "product_name", "unit_price"]
    )

    # Select final output columns
    output_columns = [
        "transaction_id",
        "customer_id",
        "customer_name",
        "product_id",
        "product_name",
        "quantity",
        "unit_price",
        "total_amount",
        "transaction_date",
        "city"
    ]

    transformed = transformed[output_columns]

    logger.info("Data transformation completed.")
    logger.info("Transformed records: %s", len(transformed))

    return transformed


# ==================================================
# DATA QUALITY VALIDATION
# ==================================================

def validate(data):

    logger.info("Starting data quality validation...")

    validation_results = validate_sales(data)

    logger.info("Data quality validation passed.")
    logger.info("Validation results: %s", validation_results)

    return validation_results


# ==================================================
# LOAD
# ==================================================

def load(data):

    logger.info("Starting data loading...")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DIR / "processed_sales.csv"

    data.to_csv(output_path, index=False)

    logger.info("Data loading completed.")
    logger.info("Output file: %s", output_path)
    logger.info("Records loaded: %s", len(data))


# ==================================================
# MAIN ETL PIPELINE
# ==================================================

def main():

    logger.info("=" * 50)
    logger.info("SALES ETL PIPELINE STARTED")
    logger.info("=" * 50)

    try:

        # Step 1: Extract
        customers, products, sales = extract()

        # Step 2: Transform
        transformed_data = transform(
            customers,
            products,
            sales
        )

        # Step 3: Validate
        validate(transformed_data)

        # Step 4: Load
        load(transformed_data)

        logger.info("=" * 50)
        logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 50)

    except Exception:

        logger.exception("ETL PIPELINE FAILED.")
        raise


# ==================================================
# EXECUTION ENTRY POINT
# ==================================================

if __name__ == "__main__":
    main()
