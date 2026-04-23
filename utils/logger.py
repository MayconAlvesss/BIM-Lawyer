import logging
import sys
from pathlib import Path

def setup_logging(log_file: str = "logs/bim_lawyer.log"):
    """
    Standardizes logging across the enterprise system.
    Outputs to both console and file.
    """
    # Create logs directory if not exists
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file)
        ]
    )

    logger = logging.getLogger("BIM-Lawyer")
    logger.info("Logging system initialized.")
    return logger

logger = setup_logging()
