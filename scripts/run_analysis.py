from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent

DATABASE_FILE = ROOT / "data" / "retail_sales.duckdb"
SQL_FILE = ROOT / "sql" / "analysis.sql"

if not DATABASE_FILE.exists():
    raise FileNotFoundError("DuckDB database not found.")

if not SQL_FILE.exists():
    raise FileNotFoundError("SQL analysis file not found.")

connection = duckdb.connect(str(DATABASE_FILE), read_only=True)

try:
    sql_content = SQL_FILE.read_text(encoding="utf-8")

    # Separate the SQL file into individual queries.
    queries = [
        query.strip()
        for query in sql_content.split(";")
        if query.strip()
    ]

    for index, query in enumerate(queries, start=1):
        print(f"\n========== QUERY {index} ==========")

        result = connection.execute(query).fetchdf()

        print(result.to_string(index=False))

finally:
    connection.close()

print("\nSQL analysis completed successfully!")