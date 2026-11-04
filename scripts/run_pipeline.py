
from pathlib import Path
import subprocess
import sys

from logger_config import setup_logger

ROOT = Path(__file__).resolve().parent.parent

# Initialize logger
logger = setup_logger()

pipeline_steps = [
    ("Data Ingestion", "ingest.py"),
    ("Data Transformation", "transform.py"),
    ("Data Quality Checks", "data_quality.py"),
    ("Database Loading", "load_to_duckdb.py"),
    ("SQL Analytics", "run_analysis.py"),
]

print("=" * 50)
print("STARTING RETAIL SALES DATA PIPELINE")
print("=" * 50, flush=True)

logger.info("Retail sales pipeline started.")

try:
    for step_number, (step_name, script_name) in enumerate(
        pipeline_steps, start=1
    ):
        script_path = ROOT / "scripts" / script_name

        print(f"\nSTEP {step_number}: {step_name}")
        print("-" * 50, flush=True)

        logger.info("Starting step %s: %s", step_number, step_name)

        subprocess.run(
            [sys.executable, str(script_path)],
            cwd=ROOT,
            check=True
        )

        print(f"\n{step_name} completed successfully!")
        logger.info("Step %s completed successfully: %s", step_number, step_name)

except subprocess.CalledProcessError as error:
    failed_script = Path(error.cmd[-1]).name

    print("\nPIPELINE FAILED!")
    print(f"Script that failed: {failed_script}")

    logger.exception("Pipeline failed while executing %s", failed_script)
    sys.exit(error.returncode)

except Exception:
    logger.exception("Unexpected pipeline error")
    raise

else:
    print("\n" + "=" * 50)
    print("RETAIL SALES DATA PIPELINE COMPLETED!")
    print("=" * 50)

    logger.info("Retail sales pipeline completed successfully.")
