
import sys
from pathlib import Path

import pandas as pd
import pytest


# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_DIR = PROJECT_ROOT / "src" / "pipeline"

sys.path.insert(0, str(PIPELINE_DIR))

from data_quality import validate_sales


# --------------------------------------------------
# TEST DATA
# --------------------------------------------------

def create_valid_sales_data():
    """Create a small valid dataset for testing."""

    return pd.DataFrame({
        "transaction_id": [1, 2],
        "customer_id": [101, 102],
        "customer_name": ["Customer_101", "Customer_102"],
        "product_id": [10, 20],
        "product_name": ["Product_10", "Product_20"],
        "quantity": [2, 3],
        "unit_price": [100.00, 200.00],
        "total_amount": [200.00, 600.00],
        "transaction_date": ["2025-01-01", "2025-01-02"],
        "city": ["Johannesburg", "Durban"],
    })


# --------------------------------------------------
# TEST 1: VALID DATA
# --------------------------------------------------

def test_valid_sales_data_passes():

    sales = create_valid_sales_data()

    result = validate_sales(sales)

    assert result["status"] == "PASSED"
    assert result["records_checked"] == 2


# --------------------------------------------------
# TEST 2: DUPLICATE TRANSACTION IDs
# --------------------------------------------------

def test_duplicate_transaction_ids():

    sales = create_valid_sales_data()

    sales.loc[1, "transaction_id"] = 1

    with pytest.raises(
        ValueError,
        match="Duplicate transaction IDs"
    ):
        validate_sales(sales)


# --------------------------------------------------
# TEST 3: MISSING CUSTOMER INFORMATION
# --------------------------------------------------

def test_missing_customer_information():

    sales = create_valid_sales_data()

    sales.loc[0, "customer_name"] = None

    with pytest.raises(
        ValueError,
        match="Missing values"
    ):
        validate_sales(sales)


# --------------------------------------------------
# TEST 4: INVALID QUANTITY
# --------------------------------------------------

def test_invalid_quantity():

    sales = create_valid_sales_data()

    sales.loc[0, "quantity"] = 0

    with pytest.raises(
        ValueError,
        match="Invalid quantities"
    ):
        validate_sales(sales)


# --------------------------------------------------
# TEST 5: INVALID UNIT PRICE
# --------------------------------------------------

def test_invalid_unit_price():

    sales = create_valid_sales_data()

    sales.loc[0, "unit_price"] = -100

    with pytest.raises(
        ValueError,
        match="Invalid unit prices"
    ):
        validate_sales(sales)


# --------------------------------------------------
# TEST 6: INCORRECT REVENUE CALCULATION
# --------------------------------------------------

def test_incorrect_revenue_calculation():

    sales = create_valid_sales_data()

    sales.loc[0, "total_amount"] = 500

    with pytest.raises(
        ValueError,
        match="Revenue calculation mismatch"
    ):
        validate_sales(sales)
