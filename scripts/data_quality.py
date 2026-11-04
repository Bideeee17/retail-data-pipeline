
from pathlib import Path
import pandas as pd
from logger_config import setup_logger

logger = setup_logger()

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "processed" / "retail_sales_cleaned.csv"


def run_quality_checks():
    print("\nSTARTING DATA QUALITY CHECKS")
    print("=" * 50)

    df = pd.read_csv(
    DATA_FILE,
    dtype={"InvoiceNo": "string"},
    low_memory=False
)

    checks = {}

    # Check 1: Missing required values
    required_columns = [
        "InvoiceNo",
        "StockCode",
        "InvoiceDate",
        "Quantity",
        "UnitPrice",
        "Revenue"
    ]

    missing_count = df[required_columns].isnull().sum().sum()
    checks["Missing required values"] = missing_count == 0

    # Check 2: Duplicate records
    duplicate_count = df.duplicated().sum()
    checks["No duplicate records"] = duplicate_count == 0

    # Check 3: Positive quantities
    checks["Positive quantities"] = (df["Quantity"] > 0).all()

    # Check 4: Positive unit prices
    checks["Positive unit prices"] = (df["UnitPrice"] > 0).all()

    # Check 5: Correct revenue calculations
    revenue_matches = (
        df["Revenue"].round(2)
        == (df["Quantity"] * df["UnitPrice"]).round(2)
    )

    checks["Correct revenue calculations"] = revenue_matches.all()

    # Display results
    for check_name, passed in checks.items():
        status = "PASSED" if passed else "FAILED"

        print(f"{check_name}: {status}")

        if passed:
            logger.info("Data quality check PASSED: %s", check_name)
        else:
            logger.error("Data quality check FAILED: %s", check_name)

    print("=" * 50)

    if all(checks.values()):
        print("ALL DATA QUALITY CHECKS PASSED!")
        logger.info("All data quality checks passed.")
    else:
        logger.error("One or more data quality checks failed.")
        raise ValueError("One or more data quality checks failed.")


if __name__ == "__main__":
    run_quality_checks()
