# FILE: agi_utils.py
# VERSION: v1.0.0-GODCORE
# NAME: AGIUtils
# AUTHOR: Brandon "iambandobandz" Emery x Victor (Fractal Architect Mode)
# PURPOSE: Logging, diagnostics, error reporting, runtime metrics

import logging
import sys
import traceback

class AGIUtils:
    @staticmethod
    def setup_logging(logfile="agi.log"):
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s][%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(logfile),
                logging.StreamHandler(sys.stdout)
            ]
        )

    @staticmethod
    def log(msg):
        logging.info(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)

    @staticmethod
    def exception(e):
        logging.error(f"Exception: {e}")
        traceback.print_exc()
