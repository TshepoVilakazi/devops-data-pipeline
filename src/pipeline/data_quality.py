
import pandas as pd


def validate_sales(sales):
    """Validate the quality of the transformed sales dataset."""

    errors = []

    # 1. Check for duplicate transaction IDs
    if sales["transaction_id"].duplicated().any():
        errors.append("Duplicate transaction IDs detected.")

    # 2. Check for missing values
    required_columns = [
        "transaction_id",
        "customer_id",
        "customer_name",
        "product_id",
        "product_name",
        "quantity",
        "unit_price",
        "total_amount",
        "transaction_date",
    ]

    if sales[required_columns].isnull().any().any():
        errors.append("Missing values detected in required columns.")

    # 3. Check for invalid quantities
    if (sales["quantity"] <= 0).any():
        errors.append("Invalid quantities detected.")

    # 4. Check for invalid prices
    if (sales["unit_price"] <= 0).any():
        errors.append("Invalid unit prices detected.")

    # 5. Check for negative transaction amounts
    if (sales["total_amount"] < 0).any():
        errors.append("Negative transaction amounts detected.")

    # 6. Check revenue calculation
    expected_amount = (
        sales["quantity"] * sales["unit_price"]
    ).round(2)

    if not sales["total_amount"].round(2).equals(expected_amount):
        errors.append("Revenue calculation mismatch detected.")

    if errors:
        raise ValueError("\n".join(errors))

    return {
        "status": "PASSED",
        "records_checked": len(sales),
        "duplicate_transactions": 0,
        "missing_required_values": 0,
        "invalid_quantities": 0,
        "invalid_prices": 0,
        "negative_amounts": 0,
    }
