
from pathlib import Path
import pandas as pd

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "processed" / "retail_sales.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "retail_sales_cleaned.csv"

print("Starting data transformation...")

# ==========================================
# 2. EXTRACT DATA
# ==========================================

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Input dataset not found: {INPUT_FILE}"
    )

df = pd.read_csv(INPUT_FILE)

initial_rows = len(df)

print(f"Initial records: {initial_rows}")

# ==========================================
# 3. STANDARDIZE COLUMN NAMES
# ==========================================

df.columns = df.columns.str.strip()

# ==========================================
# 4. HANDLE MISSING VALUES
# ==========================================

required_columns = [
    "InvoiceNo",
    "StockCode",
    "InvoiceDate",
    "Quantity",
    "UnitPrice"
]

df = df.dropna(subset=required_columns)

# Preserve transactions with unknown customer IDs.
df["CustomerID"] = (
    df["CustomerID"]
    .astype("string")
    .fillna("Unknown")
    .str.replace(r"\.0$", "", regex=True)
)

df["Description"] = (
    df["Description"]
    .fillna("Unknown Product")
    .astype(str)
    .str.strip()
)

# ==========================================
# 5. CONVERT DATA TYPES
# ==========================================

df["InvoiceNo"] = df["InvoiceNo"].astype(str)
df["StockCode"] = df["StockCode"].astype(str)

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

df["Quantity"] = pd.to_numeric(
    df["Quantity"],
    errors="coerce"
)

df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"],
    errors="coerce"
)

# Remove records with invalid converted values.
df = df.dropna(
    subset=["InvoiceDate", "Quantity", "UnitPrice"]
)

# ==========================================
# 6. REMOVE DUPLICATE RECORDS
# ==========================================

before_duplicates = len(df)

df = df.drop_duplicates()

duplicates_removed = before_duplicates - len(df)

# ==========================================
# 7. FILTER INVALID SALES
# ==========================================

before_filtering = len(df)

# Remove zero and negative quantities.
df = df[df["Quantity"] > 0]

# Remove zero and negative prices.
df = df[df["UnitPrice"] > 0]

# Exclude cancellation invoices.
df = df[
    ~df["InvoiceNo"].str.startswith("C", na=False)
]

invalid_records_removed = before_filtering - len(df)

# ==========================================
# 8. CREATE REVENUE COLUMN
# ==========================================

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# ==========================================
# 9. SAVE CLEANED DATA
# ==========================================

df.to_csv(OUTPUT_FILE, index=False)

# ==========================================
# 10. TRANSFORMATION SUMMARY
# ==========================================

final_rows = len(df)

print("\n========== TRANSFORMATION SUMMARY ==========")

print(f"Initial records: {initial_rows}")
print(f"Duplicate records removed: {duplicates_removed}")
print(f"Invalid sales records removed: {invalid_records_removed}")
print(f"Final records: {final_rows}")
print(f"Records removed overall: {initial_rows - final_rows}")

print(f"\nTotal revenue: {df['Revenue'].sum():,.2f}")

print(f"\nCleaned dataset saved to:")
print(OUTPUT_FILE)

print("\nData transformation completed!")
