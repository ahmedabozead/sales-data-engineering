import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

SCRIPTS_DIR = BASE_DIR / "scripts"
LOGS_DIR = BASE_DIR / "logs"
LOG_FILE = LOGS_DIR / "pipeline.log"

LOGS_DIR.mkdir(parents=True, exist_ok=True)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)
PIPELINE_STEPS = [
    "transform_customers.py",
    "transform_products.py",
    "transform_sales.py",
    "validate_data.py",
    "load_to_sqlserver.py",
    "validate_sqlserver.py",
]



def run_step(script_name):
    script_path = SCRIPTS_DIR / script_name

    logger.info("Starting step: %s", script_name)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )

    if result.stdout:
        logger.info(
            "%s output:\n%s",
            script_name,
            result.stdout.strip(),
        )

    if result.stderr:
        logger.error(
            "%s errors:\n%s",
            script_name,
            result.stderr.strip(),
        )

    if result.returncode != 0:
        raise RuntimeError(
            f"Step failed: {script_name}"
        )

    logger.info("Completed step: %s", script_name)


def run_pipeline():
    start_time = datetime.now()

    logger.info("=" * 60)
    logger.info("PIPELINE STARTED")
    logger.info("Start time: %s", start_time)
    logger.info("=" * 60)

    try:
        for step in PIPELINE_STEPS:
            run_step(step)

        end_time = datetime.now()
        duration = end_time - start_time

        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("End time: %s", end_time)
        logger.info("Duration: %s", duration)
        logger.info("=" * 60)

    except Exception as error:
        end_time = datetime.now()

        logger.exception("PIPELINE FAILED")
        logger.error("Failure time: %s", end_time)
        logger.error("Error: %s", error)

        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()
