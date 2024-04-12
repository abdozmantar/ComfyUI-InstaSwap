#----------------------------------------------#
# INSTASWAP FAST FACE SWAPPER NODE FOR COMFYUI #
#                                              #
#                         by abdozmantar       #
#                             2024             #
#                                              #
#         GNU GENERAL PUBLIC LICENSE           #
#----------------------------------------------#

import logging
import copy
import sys
from modules import shared
from instaswap_utils import addLoggingLevel

class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[0;36m",  # CYAN
        "JOB": "\u001b[32m",  # GREEN
        "INFO": "\033[0;32m",  # GREEN
        "WARNING": "\033[0;33m",  # ORANGE
        "ERROR": "\033[0;31m",  # RED
        "CRITICAL": "\033[0;37;41m",  # WHITE ON RED
        "RESET": "\033[0m",  # RESET COLOR
    }

    def format(self, record):
        colored_record = copy.copy(record)
        levelname = colored_record.levelname
        seq = self.COLORS.get(levelname, self.COLORS["RESET"])
        colored_record.levelname = f"{seq}{levelname}{self.COLORS['RESET']}"
        return super().format(colored_record)

# Create a new logger
logger = logging.getLogger("InstaSwap")
logger.propagate = False

# Add Custom Level
addLoggingLevel("JOB", logging.INFO + 5)

# Add handler if we don't have one.
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        ColoredFormatter("[%(name)s] %(asctime)s - %(levelname)s - %(message)s",datefmt="%H:%M:%S")
    )
    logger.addHandler(handler)

# Configure logger
loglevel_string = getattr(shared.cmd_opts, "instaswap_loglevel", "INFO")
loglevel = getattr(logging, loglevel_string.upper(), "info")
logger.setLevel(loglevel)
