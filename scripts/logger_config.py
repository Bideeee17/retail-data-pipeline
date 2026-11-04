
import logging
from pathlib import Path

# Find the project root directory
ROOT = Path(__file__).resolve().parent.parent

# Create the logs folder if it doesn't exist
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Store log records in this file
LOG_FILE = LOG_DIR / "pipeline.log"


def setup_logger():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True
    )

    return logging.getLogger("retail_pipeline")
