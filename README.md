# Retail Sales Data Engineering Pipeline

An end-to-end data engineering project that ingests, cleans, validates, stores, and analyzes retail sales data using Python, Pandas, DuckDB, and SQL.

## Project Overview

This project demonstrates a local data engineering pipeline built around the UCI Online Retail dataset. It automates the processing of raw retail transaction data into a cleaned analytical dataset and a DuckDB database for SQL-based analysis.

## Tech Stack

- **Python** – Pipeline scripting and automation
- **Pandas** – Data ingestion and transformation
- **DuckDB** – Analytical database
- **SQL** – Business analysis and reporting
- **Git & GitHub** – Version control and project hosting

## Pipeline Architecture

```text
Online Retail.xlsx
        |
        v
   Data Ingestion
        |
        v
   Raw CSV Output
        |
        v
 Data Transformation
        |
        v
 Cleaned CSV Output
        |
        v
 Data Quality Checks
        |
        v
  DuckDB Database
        |
        v
   SQL Analytics
        |
        v
  Analytical Results
```

## Project Structure

```text
retail-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   ├── ingest.py
│   ├── transform.py
│   ├── data_quality.py
│   ├── load_to_duckdb.py
│   ├── logger_config.py
│   ├── run_analysis.py
│   └── run_pipeline.py
├── sql/
│   └── analysis.sql
├── logs/
├── .gitignore
└── README.md
```

## Dataset

**Source:** UCI Machine Learning Repository – Online Retail

Dataset: [Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)

The dataset contains transactions from a UK-based online retail business between December 2010 and December 2011.

The original dataset contains 541,909 records.

## Data Transformation

The transformation process includes:

- Removing records with missing required fields
- Handling missing customer IDs and product descriptions
- Standardizing invoice and stock code types
- Converting invoice dates into datetime values
- Converting quantity and unit price into numeric values
- Removing invalid records and duplicates
- Excluding cancellation invoices
- Filtering non-positive quantities and unit prices
- Calculating revenue using quantity multiplied by unit price

**Revenue formula:**

`Revenue = Quantity × UnitPrice`

## Data Quality Checks

The pipeline validates the cleaned dataset through five checks:

1. Missing values in required columns
2. Duplicate records
3. Positive quantities
4. Positive unit prices
5. Correct revenue calculations

The pipeline stops if a data quality check fails.

## SQL Analytics

The project includes SQL queries for:

- Total transaction records
- Revenue by country
- Top 10 products by revenue
- Monthly revenue trends
- Top 10 customers by spending
- Average order value

## Pipeline Logging

Pipeline execution is recorded in `logs/pipeline.log`, including:

- Pipeline start and completion
- Individual stage execution
- Successful data quality checks
- Errors during execution

## Results

| Metric | Result |
|---|---:|
| Original records | 541,909 |
| Duplicate records removed | 5,268 |
| Invalid sales records removed | 11,763 |
| Cleaned records | 524,878 |
| Total revenue | 10,642,110.80 |
| Average order value | 533.17 |

*Revenue and order value are expressed in the dataset's currency (GBP).*

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Bideeee17/retail-data-pipeline.git
cd retail-data-pipeline
```

### 2. Download the dataset

Download `Online Retail.xlsx` from the [UCI Online Retail dataset page](https://archive.ics.uci.edu/dataset/352/online+retail).

Place the file inside:

```text
data/raw/Online Retail.xlsx
```

Create the `data/raw` directory if it does not exist.

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install pandas duckdb openpyxl
```

### 5. Run the pipeline

```bash
python scripts/run_pipeline.py
```

The pipeline automatically performs ingestion, transformation, data quality checks, database loading, and SQL analytics.

## Future Improvements

- Containerization using Docker
- Workflow orchestration using Apache Airflow
- Data modeling using dbt
- Visualization using Power BI
- Automated testing
- Incremental data processing

## Author

Developed as a hands-on Data Engineering portfolio project.
