"""! Config file to store all static data.
This file contains the logging system data, API constants.

@author WALL-O Team
@version 1.1.0
@since 10/01/2023
"""

import logging

# API part
API_NAME: str = "WALL-O API"
API_VERSION: str = "1.1.0"
# using 8081 instead of 8080 to avoid any conflict with any already running web servers
API_DEFAULT_PORT: int = 8081

DASHBOARD_URL: str = "https://wall-o.benjaminpmd.fr/dashboard"

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
