# API part
import logging


API_NAME: str = "WALL-O API"
API_VERSION: str = "0.9.0"
API_DEFAULT_PORT: int = 8080

# Network part

# logging

# logging configuration
LOGGING_FILE: str = "debug.log"

# level of the logging saved in the file
LOGGING_LEVEL: int = logging.INFO

logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        level=LOGGING_LEVEL,
        handlers=[
            logging.FileHandler(LOGGING_FILE),
            logging.StreamHandler()
        ]
    )