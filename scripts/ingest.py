from pathlib import Path
import pandas as pd

# Project paths
ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Locate dataset
source_file = RAW_DIR / "Online Retail.xlsx"

print("Starting data ingestion...")

# Extract
df = pd.read_excel(source_file)

print(f"Rows extracted: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Load to CSV
output_file = PROCESSED_DIR / "retail_sales.csv"

df.to_csv(output_file, index=False)

print(f"Data saved to: {output_file}")
print("Ingestion completed successfully!")