import logging
import sys

def setup_logging():
    # Setup basic structured-like logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("kalaconnect_ai")
    return logger

logger = setup_logging()
