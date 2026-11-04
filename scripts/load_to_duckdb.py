from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "processed" / "retail_sales_cleaned.csv"
DATABASE_FILE = ROOT / "data" / "retail_sales.duckdb"

print("Starting database loading...")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Cleaned dataset not found: {INPUT_FILE}"
    )

# Read the cleaned CSV.
# Keep identifiers as strings so they aren't treated as numbers.
df = pd.read_csv(
    INPUT_FILE,
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "CustomerID": "string"
    },
    parse_dates=["InvoiceDate"]
)

print(f"Records read: {len(df):,}")

# Connect to DuckDB (creates the database if it doesn't exist).
connection = duckdb.connect(str(DATABASE_FILE))

try:
    # Register the Pandas DataFrame so DuckDB can access it.
    connection.register("retail_sales_df", df)

    # Create or replace the table.
    connection.execute("""
        CREATE OR REPLACE TABLE retail_sales AS
        SELECT * FROM retail_sales_df
    """)

    # Verify the table.
    row_count = connection.execute("""
        SELECT COUNT(*) FROM retail_sales
    """).fetchone()[0]

    total_revenue = connection.execute("""
        SELECT SUM(Revenue) FROM retail_sales
    """).fetchone()[0]

    print("\n========== DATABASE SUMMARY ==========")
    print(f"Records loaded: {row_count:,}")
    print(f"Total revenue: {total_revenue:,.2f}")

    print("\n========== TABLE STRUCTURE ==========")
    schema = connection.execute("""
        DESCRIBE retail_sales
    """).fetchdf()

    print(schema.to_string(index=False))

finally:
    connection.close()

print(f"\nDatabase saved at: {DATABASE_FILE}")
print("Database loading completed successfully!")